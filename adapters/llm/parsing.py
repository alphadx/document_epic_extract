"""Parsing and prompt-construction helpers for LiteLLM adapter."""

from __future__ import annotations

import json
from typing import Any

from api.core.exceptions import ExtractionError
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction

_RESERVED_LITELLM_KEYS = {"model", "messages", "temperature", "timeout", "max_tokens", "api_base"}


def extract_message_content(raw_response: Any) -> str:
    """Extract message content from LiteLLM response objects/dicts."""
    choices = getattr(raw_response, "choices", None)
    if choices is None and isinstance(raw_response, dict):
        choices = raw_response.get("choices")

    if not choices:
        raise ExtractionError("LLM response did not include choices.")

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    if message is None and isinstance(first_choice, dict):
        message = first_choice.get("message", {})

    content = getattr(message, "content", None)
    if content is None and isinstance(message, dict):
        content = message.get("content", "")

    if isinstance(content, list):
        chunks = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                chunks.append(str(part.get("text", "")))
            else:
                chunks.append(str(part))
        return "\n".join(chunks).strip()

    return str(content or "").strip()


def _iter_json_object_candidates(payload: str):
    in_string = False
    escape = False
    depth = 0
    start_idx: int | None = None

    for idx, ch in enumerate(payload):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == '{':
            if depth == 0:
                start_idx = idx
            depth += 1
        elif ch == '}':
            if depth == 0:
                continue
            depth -= 1
            if depth == 0 and start_idx is not None:
                yield payload[start_idx : idx + 1]
                start_idx = None


def extract_json_substring(payload: str) -> str:
    """Extract best-effort JSON object from mixed text output."""
    for marker in ("```json", "```"):
        if marker in payload:
            segments = payload.split(marker)
            for segment in segments[1:]:
                candidate = segment.strip().strip("`").strip()
                for obj in _iter_json_object_candidates(candidate):
                    try:
                        json.loads(obj)
                        return obj
                    except Exception:
                        continue

    for obj in _iter_json_object_candidates(payload):
        try:
            json.loads(obj)
            return obj
        except Exception:
            continue

    raise ExtractionError("LLM did not return JSON content.")


def _normalize_standardized_payload(data: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(data)
    if isinstance(normalized.get("fields"), dict):
        normalized["fields"] = [
            {"key": str(k), "value": str(v)} for k, v in normalized["fields"].items()
        ]
    return normalized


def parse_standardized_extraction(content: str, engine_used: str) -> StandardizedExtraction:
    """Parse model content into unified schema with graceful fallbacks."""
    if not content:
        raise ExtractionError("Empty response content from LLM.")

    try:
        parsed = StandardizedExtraction.model_validate_json(content)
    except Exception:
        try:
            extracted = extract_json_substring(content)
            data = json.loads(extracted)
        except Exception as exc:  # noqa: BLE001
            raise ExtractionError("Invalid JSON returned by LLM.") from exc

        if isinstance(data, dict) and "standardized_extraction" in data and isinstance(
            data["standardized_extraction"], dict
        ):
            data = data["standardized_extraction"]

        if not isinstance(data, dict):
            raise ExtractionError("Invalid JSON object returned by LLM.") from None

        data = _normalize_standardized_payload(data)
        data.setdefault("engine_used", engine_used)
        parsed = StandardizedExtraction.model_validate(data)

    if not parsed.engine_used:
        parsed.engine_used = engine_used

    return parsed


def resolve_required_fields(request: ExtractionRequest, prebuilt: dict[str, Any]) -> list[str]:
    if request.extraction_target.custom_fields:
        return request.extraction_target.custom_fields
    fields = prebuilt.get("required_fields", [])
    return fields if isinstance(fields, list) else []


def build_system_prompt(prebuilt: dict[str, Any], required_fields: list[str]) -> str:
    base_prompt = str(prebuilt.get("system_prompt", "")).strip()
    required_fields_text = "\n".join(f"- {field}" for field in required_fields) or "- none"
    return (
        f"{base_prompt}\n\n"
        "Return only valid JSON that conforms to StandardizedExtraction.\n"
        f"Required fields:\n{required_fields_text}"
    ).strip()


def resolve_document_url(document_input: str) -> str:
    if document_input.startswith(("http://", "https://", "data:")):
        return document_input
    return f"data:image/png;base64,{document_input}"


def safe_api_kwargs(api_keys: dict[str, str]) -> dict[str, str]:
    return {k: v for k, v in api_keys.items() if k not in _RESERVED_LITELLM_KEYS}
