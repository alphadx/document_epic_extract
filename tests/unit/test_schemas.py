"""Unit tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from api.schemas.request import EngineConfig, ExtractionRequest, ExtractionTarget
from api.schemas.response import (
    BoundingBox,
    ExtractedField,
    ExtractedTable,
    StandardizedExtraction,
    TableCell,
)


class TestBoundingBox:
    def test_valid(self):
        bb = BoundingBox(x0=0.0, y0=0.0, x1=0.5, y1=0.5)
        assert bb.x1 == 0.5

    def test_out_of_range(self):
        with pytest.raises(ValidationError):
            BoundingBox(x0=-0.1, y0=0.0, x1=1.0, y1=1.0)


class TestExtractionRequest:
    def test_valid_llm_router(self):
        req = ExtractionRequest(
            document="base64data",
            engine_config=EngineConfig(
                provider="llm_router",
                model="claude-3-5-sonnet-20241022",
                api_keys={"anthropic": "sk-ant-test"},
            ),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )
        assert req.engine_config.provider == "llm_router"

    def test_invalid_provider(self):
        with pytest.raises(ValidationError):
            ExtractionRequest(
                document="base64data",
                engine_config=EngineConfig(
                    provider="unsupported_provider",
                    model="some-model",
                ),
                extraction_target=ExtractionTarget(document_type="invoice"),
            )

    def test_custom_fields(self):
        req = ExtractionRequest(
            document="base64data",
            engine_config=EngineConfig(provider="aws", model="textract"),
            extraction_target=ExtractionTarget(
                document_type="free",
                custom_fields=["patente_vehiculo", "fecha_siniestro"],
            ),
        )
        assert "patente_vehiculo" in req.extraction_target.custom_fields


class TestStandardizedExtraction:
    def test_minimal(self):
        result = StandardizedExtraction(engine_used="test-engine")
        assert result.raw_text == ""
        assert result.fields == []
        assert result.tables == []

    def test_with_fields(self):
        result = StandardizedExtraction(
            raw_text="Invoice #001",
            fields=[
                ExtractedField(
                    key="invoice_number",
                    value="001",
                    confidence=0.99,
                    bounding_box=BoundingBox(x0=0.6, y0=0.05, x1=0.95, y1=0.10),
                )
            ],
            engine_used="claude-3-5-sonnet-20241022",
        )
        assert result.fields[0].key == "invoice_number"
        assert result.fields[0].bounding_box.x0 == 0.6

    def test_invalid_confidence(self):
        with pytest.raises(ValidationError):
            ExtractedField(key="k", value="v", confidence=1.5)
