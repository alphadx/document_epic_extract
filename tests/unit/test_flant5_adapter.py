"""Unit tests for FLAN-T5 local adapter."""

from __future__ import annotations

import json

import pytest

from adapters.local.flant5 import FlanT5Adapter
from api.core.exceptions import ExtractionError
from api.schemas.request import EngineConfig, ExtractionRequest, ExtractionTarget


@pytest.mark.asyncio
async def test_extract_uses_mock_payload_and_defaults_engine_used():
    adapter = FlanT5Adapter()
    request = ExtractionRequest(
        document="base64-text",
        engine_config=EngineConfig(
            provider="local",
            model="flan-t5-base",
            api_keys={
                "mock_response_json": json.dumps(
                    {
                        "raw_text": "invoice_number: INV-909",
                        "fields": [{"key": "invoice_number", "value": "INV-909"}],
                        "tables": [],
                    }
                )
            },
        ),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    result = await adapter.extract(request)

    assert result.raw_text == "invoice_number: INV-909"
    assert result.engine_used == "local:flan-t5-base"


@pytest.mark.asyncio
async def test_extract_rejects_invalid_mock_payload():
    adapter = FlanT5Adapter()
    request = ExtractionRequest(
        document="base64-text",
        engine_config=EngineConfig(
            provider="local",
            model="flan-t5-mini",
            api_keys={"mock_response_json": "{invalid-json"},
        ),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    with pytest.raises(ExtractionError, match="Invalid local mock payload JSON"):
        await adapter.extract(request)
