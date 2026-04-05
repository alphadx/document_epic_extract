"""Unit tests for SmolVLM2 local adapter."""

from __future__ import annotations

import json

import httpx
import pytest

from adapters.local.smolvlm2 import SmolVLM2Adapter
from api.core.exceptions import ExtractionError
from api.schemas.request import EngineConfig, ExtractionRequest, ExtractionTarget


def _request_with_mock(mock_payload: dict | str) -> ExtractionRequest:
    if isinstance(mock_payload, dict):
        mock_payload = json.dumps(mock_payload)
    return ExtractionRequest(
        document="base64-image",
        engine_config=EngineConfig(
            provider="local",
            model="smolvlm2-2.2b-instruct",
            api_keys={"mock_response_json": mock_payload},
        ),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )


@pytest.mark.asyncio
async def test_extract_uses_mock_payload_and_defaults_engine_used():
    adapter = SmolVLM2Adapter()
    request = _request_with_mock(
        {
            "raw_text": "Factura local",
            "fields": [{"key": "invoice_number", "value": "INV-1"}],
            "tables": [],
        }
    )

    result = await adapter.extract(request)

    assert result.raw_text == "Factura local"
    assert result.fields[0].key == "invoice_number"
    assert result.engine_used == "local:smolvlm2-2.2b-instruct"


@pytest.mark.asyncio
async def test_extract_reads_nested_result_payload():
    adapter = SmolVLM2Adapter()
    request = _request_with_mock(
        {
            "result": {
                "raw_text": "Documento local",
                "fields": [],
                "tables": [],
                "engine_used": "worker:smolvlm2",
            }
        }
    )

    result = await adapter.extract(request)

    assert result.raw_text == "Documento local"
    assert result.engine_used == "worker:smolvlm2"


@pytest.mark.asyncio
async def test_extract_rejects_invalid_mock_payload():
    adapter = SmolVLM2Adapter()
    request = _request_with_mock("{invalid-json")

    with pytest.raises(ExtractionError, match="Invalid local mock payload JSON"):
        await adapter.extract(request)


@pytest.mark.asyncio
async def test_extract_wraps_request_errors(monkeypatch):
    adapter = SmolVLM2Adapter()
    request = ExtractionRequest(
        document="base64-image",
        engine_config=EngineConfig(provider="local", model="smolvlm2-2.2b-instruct"),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    class FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, *args, **kwargs):  # noqa: ANN002, ANN003
            req = httpx.Request("POST", "http://worker:8001/infer")
            raise httpx.ConnectError("boom", request=req)

    monkeypatch.setattr("adapters.local.smolvlm2.httpx.AsyncClient", lambda **kwargs: FakeAsyncClient())

    with pytest.raises(ExtractionError, match="Local worker request failed"):
        await adapter.extract(request)
