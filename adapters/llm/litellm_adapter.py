"""LiteLLM Vision adapter — routes LLM requests and parses structured output."""

from __future__ import annotations

import asyncio
from typing import Any

from fastapi import HTTPException

from adapters.base import BaseAdapter
from adapters.llm.parsing import (
    build_system_prompt,
    extract_message_content,
    parse_standardized_extraction,
    resolve_document_url,
    resolve_required_fields,
    safe_api_kwargs,
)
from adapters.llm.resilience import circuit_breaker_store, circuit_breaker_telemetry
from api.core.config import settings
from api.core.exceptions import ExtractionError
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction
from api.services.prebuilt_service import load_prebuilt


def _litellm_acompletion():
    """Lazy-import litellm to keep startup lightweight."""
    try:
        from litellm import acompletion
    except Exception as exc:  # noqa: BLE001
        raise ExtractionError(
            "LiteLLM is not installed. Install API extras with 'pip install .[api]'."
        ) from exc
    return acompletion


class LiteLLMVisionAdapter(BaseAdapter):
    """Adapter for LLM-based extraction via LiteLLM."""

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        try:
            prebuilt = await load_prebuilt(request.extraction_target.document_type)
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ExtractionError("Failed to load prebuilt template.") from exc

        required_fields = resolve_required_fields(request, prebuilt)
        system_prompt = build_system_prompt(prebuilt, required_fields)

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the document and respond with JSON only."},
                    {
                        "type": "image_url",
                        "image_url": {"url": resolve_document_url(request.document.strip())},
                    },
                ],
            },
        ]

        completion_kwargs: dict[str, Any] = {
            "model": request.engine_config.model,
            "messages": messages,
            "temperature": 0,
            "timeout": settings.http_timeout,
            "max_tokens": settings.llm_max_tokens,
            "response_format": {"type": "json_object"},
        }
        completion_kwargs.update(safe_api_kwargs(request.engine_config.api_keys))
        if request.engine_config.custom_endpoint:
            completion_kwargs["api_base"] = request.engine_config.custom_endpoint

        model_key = f"llm_router:{request.engine_config.model}"
        state_before_guard = circuit_breaker_store.get_state(model_key)
        if circuit_breaker_store.is_open(model_key):
            circuit_breaker_telemetry.increment_reject(model_key)
            circuit_breaker_telemetry.set_state(model_key, "open")
            raise ExtractionError("Provider temporarily unavailable (circuit open).")
        state_after_guard = circuit_breaker_store.get_state(model_key)
        is_half_open_probe = state_after_guard == "half_open"

        acompletion = _litellm_acompletion()
        response = None
        last_exc: Exception | None = None
        total_attempts = max(1, settings.llm_max_retries)
        for attempt in range(total_attempts):
            try:
                response = await acompletion(**completion_kwargs)
                last_exc = None
                break
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                previous_state = circuit_breaker_store.get_state(model_key)
                circuit_breaker_store.record_failure(
                    model_key,
                    threshold=settings.llm_circuit_breaker_threshold,
                    cooldown_ms=settings.llm_circuit_breaker_cooldown_ms,
                )
                new_state = circuit_breaker_store.get_state(model_key)
                circuit_breaker_telemetry.set_state(model_key, new_state)
                if previous_state != "open" and new_state == "open":
                    circuit_breaker_telemetry.increment_open(model_key)
                    circuit_breaker_telemetry.emit_transition_log(
                        key=model_key,
                        from_state=previous_state,
                        to_state="open",
                        reason="provider_error",
                        cooldown_ms=settings.llm_circuit_breaker_cooldown_ms,
                        failures=None,
                    )
                if previous_state == "half_open" or is_half_open_probe:
                    circuit_breaker_telemetry.increment_half_open_probe(model_key, "failure")
                if attempt < total_attempts - 1 and settings.llm_retry_backoff_ms > 0:
                    await asyncio.sleep(settings.llm_retry_backoff_ms / 1000)

        if last_exc is not None:
            raise ExtractionError("Provider call failed for llm_router.") from last_exc

        circuit_breaker_store.reset(model_key)
        circuit_breaker_telemetry.set_state(model_key, "closed")
        if state_before_guard in {"open", "half_open"} or state_after_guard in {"open", "half_open"}:
            circuit_breaker_telemetry.emit_transition_log(
                key=model_key,
                from_state=state_after_guard,
                to_state="closed",
                reason="success",
                cooldown_ms=None,
                failures=0,
            )
        if is_half_open_probe:
            circuit_breaker_telemetry.increment_half_open_probe(model_key, "success")

        try:
            content = extract_message_content(response)
            return parse_standardized_extraction(
                content=content,
                engine_used=f"llm_router:{request.engine_config.model}",
            )
        except ExtractionError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ExtractionError("Failed to parse LLM response.") from exc
