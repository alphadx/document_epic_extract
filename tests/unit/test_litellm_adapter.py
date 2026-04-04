"""Unit tests for LiteLLM vision adapter orchestration."""

from __future__ import annotations

import pytest

from adapters.llm import litellm_adapter
from adapters.llm.litellm_adapter import LiteLLMVisionAdapter
from adapters.llm.resilience import circuit_breaker_store
from api.core.config import settings
from api.core.exceptions import ExtractionError
from api.schemas.request import EngineConfig, ExtractionRequest, ExtractionTarget


class TestLiteLLMVisionAdapter:
    @pytest.mark.asyncio
    async def test_extract_success_with_custom_fields(self, monkeypatch: pytest.MonkeyPatch):
        async def fake_load_prebuilt(document_type: str):
            assert document_type == "invoice"
            return {
                "id": "invoice",
                "system_prompt": "Extract fields",
                "required_fields": ["invoice_number"],
            }

        async def fake_acompletion(**kwargs):
            assert kwargs["model"] == "gpt-4o"
            assert kwargs["temperature"] == 0
            assert kwargs["timeout"] == settings.http_timeout
            assert kwargs["max_tokens"] == settings.llm_max_tokens
            assert kwargs["response_format"] == {"type": "json_object"}
            assert "- total_amount" in kwargs["messages"][0]["content"]
            return {
                "choices": [
                    {
                        "message": {
                            "content": (
                                '{"raw_text":"ok","fields":[],"tables":[],'
                                '"engine_used":"llm_router:gpt-4o"}'
                            )
                        }
                    }
                ]
            }

        monkeypatch.setattr(litellm_adapter, "load_prebuilt", fake_load_prebuilt)
        monkeypatch.setattr(litellm_adapter, "_litellm_acompletion", lambda: fake_acompletion)

        adapter = LiteLLMVisionAdapter()
        req = ExtractionRequest(
            document="ZmFrZV9pbWFnZQ==",
            engine_config=EngineConfig(
                provider="llm_router",
                model="gpt-4o",
                api_keys={"model": "do-not-override", "api_key": "secret"},
            ),
            extraction_target=ExtractionTarget(
                document_type="invoice", custom_fields=["invoice_number", "total_amount"]
            ),
        )

        result = await adapter.extract(req)
        assert result.raw_text == "ok"
        assert result.engine_used == "llm_router:gpt-4o"

    @pytest.mark.asyncio
    async def test_extract_wraps_provider_errors(self, monkeypatch: pytest.MonkeyPatch):
        async def fake_load_prebuilt(document_type: str):
            return {
                "id": document_type,
                "system_prompt": "Extract fields",
                "required_fields": [],
            }

        async def fake_acompletion(**kwargs):
            raise RuntimeError("provider down")

        monkeypatch.setattr(litellm_adapter, "load_prebuilt", fake_load_prebuilt)
        monkeypatch.setattr(litellm_adapter, "_litellm_acompletion", lambda: fake_acompletion)

        adapter = LiteLLMVisionAdapter()
        req = ExtractionRequest(
            document="https://example.com/invoice.png",
            engine_config=EngineConfig(provider="llm_router", model="gpt-4o"),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )

        with pytest.raises(ExtractionError, match="Provider call failed for llm_router"):
            await adapter.extract(req)

    @pytest.mark.asyncio
    async def test_extract_retries_provider_call(self, monkeypatch: pytest.MonkeyPatch):
        attempts = {"n": 0}

        async def fake_load_prebuilt(document_type: str):
            return {
                "id": document_type,
                "system_prompt": "Extract fields",
                "required_fields": [],
            }

        async def flaky_acompletion(**kwargs):
            attempts["n"] += 1
            if attempts["n"] < 2:
                raise RuntimeError("transient")
            return {
                "choices": [
                    {
                        "message": {
                            "content": (
                                '{"raw_text":"ok","fields":[],"tables":[],'
                                '"engine_used":"llm_router:gpt-4o"}'
                            )
                        }
                    }
                ]
            }

        monkeypatch.setattr(litellm_adapter, "load_prebuilt", fake_load_prebuilt)
        monkeypatch.setattr(litellm_adapter, "_litellm_acompletion", lambda: flaky_acompletion)
        monkeypatch.setattr(settings, "llm_max_retries", 2)
        monkeypatch.setattr(settings, "llm_retry_backoff_ms", 0)

        adapter = LiteLLMVisionAdapter()
        req = ExtractionRequest(
            document="https://example.com/invoice.png",
            engine_config=EngineConfig(provider="llm_router", model="gpt-4o"),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )

        result = await adapter.extract(req)
        assert result.raw_text == "ok"
        assert attempts["n"] == 2

    @pytest.mark.asyncio
    async def test_extract_retries_exhausted(self, monkeypatch: pytest.MonkeyPatch):
        attempts = {"n": 0}

        async def fake_load_prebuilt(document_type: str):
            return {
                "id": document_type,
                "system_prompt": "Extract fields",
                "required_fields": [],
            }

        async def always_fails(**kwargs):
            attempts["n"] += 1
            raise RuntimeError("still failing")

        monkeypatch.setattr(litellm_adapter, "load_prebuilt", fake_load_prebuilt)
        monkeypatch.setattr(litellm_adapter, "_litellm_acompletion", lambda: always_fails)
        monkeypatch.setattr(settings, "llm_max_retries", 3)
        monkeypatch.setattr(settings, "llm_retry_backoff_ms", 0)

        adapter = LiteLLMVisionAdapter()
        req = ExtractionRequest(
            document="https://example.com/invoice.png",
            engine_config=EngineConfig(provider="llm_router", model="gpt-4o"),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )

        with pytest.raises(ExtractionError, match="Provider call failed for llm_router"):
            await adapter.extract(req)

        assert attempts["n"] == 3

    @pytest.mark.asyncio
    async def test_extract_circuit_breaker_opens_after_failures(self, monkeypatch: pytest.MonkeyPatch):
        attempts = {"n": 0}

        async def fake_load_prebuilt(document_type: str):
            return {
                "id": document_type,
                "system_prompt": "Extract fields",
                "required_fields": [],
            }

        async def always_fails(**kwargs):
            attempts["n"] += 1
            raise RuntimeError("down")

        circuit_breaker_store.clear()
        monkeypatch.setattr(litellm_adapter, "load_prebuilt", fake_load_prebuilt)
        monkeypatch.setattr(litellm_adapter, "_litellm_acompletion", lambda: always_fails)
        monkeypatch.setattr(settings, "llm_max_retries", 1)
        monkeypatch.setattr(settings, "llm_retry_backoff_ms", 0)
        monkeypatch.setattr(settings, "llm_circuit_breaker_threshold", 1)
        monkeypatch.setattr(settings, "llm_circuit_breaker_cooldown_ms", 60_000)

        adapter = LiteLLMVisionAdapter()
        req = ExtractionRequest(
            document="https://example.com/invoice.png",
            engine_config=EngineConfig(provider="llm_router", model="gpt-4o"),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )

        with pytest.raises(ExtractionError, match="Provider call failed for llm_router"):
            await adapter.extract(req)

        with pytest.raises(ExtractionError, match="circuit open"):
            await adapter.extract(req)

        assert attempts["n"] == 1

    @pytest.mark.asyncio
    async def test_extract_wraps_prebuilt_load_errors(self, monkeypatch: pytest.MonkeyPatch):
        async def broken_prebuilt(_: str):
            raise RuntimeError("disk issue")

        monkeypatch.setattr(litellm_adapter, "load_prebuilt", broken_prebuilt)

        adapter = LiteLLMVisionAdapter()
        req = ExtractionRequest(
            document="https://example.com/invoice.png",
            engine_config=EngineConfig(provider="llm_router", model="gpt-4o"),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )

        with pytest.raises(ExtractionError, match="Failed to load prebuilt template"):
            await adapter.extract(req)
