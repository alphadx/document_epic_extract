"""Unit tests for OCR cloud adapters."""

from __future__ import annotations

import json

import pytest

from adapters.ocr.aws import AWSTextractAdapter
from adapters.ocr.azure import AzureDocIntelligenceAdapter
from adapters.ocr.gcp import GCPDocumentAIAdapter
from api.core.exceptions import ExtractionError
from api.schemas.request import EngineConfig, ExtractionRequest, ExtractionTarget


@pytest.mark.asyncio
async def test_aws_adapter_maps_blocks_to_standardized_extraction():
    payload = {
        "Blocks": [
            {"Id": "l1", "BlockType": "LINE", "Text": "Invoice #123"},
            {
                "Id": "k1",
                "BlockType": "KEY_VALUE_SET",
                "EntityTypes": ["KEY"],
                "Confidence": 99.0,
                "Geometry": {"BoundingBox": {"Left": 0.1, "Top": 0.1, "Width": 0.2, "Height": 0.1}},
                "Relationships": [
                    {"Type": "CHILD", "Ids": ["w1"]},
                    {"Type": "VALUE", "Ids": ["v1"]},
                ],
            },
            {"Id": "w1", "BlockType": "WORD", "Text": "invoice_number"},
            {
                "Id": "v1",
                "BlockType": "KEY_VALUE_SET",
                "EntityTypes": ["VALUE"],
                "Relationships": [{"Type": "CHILD", "Ids": ["w2"]}],
            },
            {"Id": "w2", "BlockType": "WORD", "Text": "123"},
            {"Id": "t1", "BlockType": "TABLE", "Relationships": [{"Type": "CHILD", "Ids": ["c1"]}]},
            {
                "Id": "c1",
                "BlockType": "CELL",
                "RowIndex": 1,
                "ColumnIndex": 1,
                "Relationships": [{"Type": "CHILD", "Ids": ["w3"]}],
            },
            {"Id": "w3", "BlockType": "WORD", "Text": "item"},
        ]
    }

    req = ExtractionRequest(
        document="ignored",
        engine_config=EngineConfig(
            provider="aws", model="textract", api_keys={"mock_response_json": json.dumps(payload)}
        ),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    result = await AWSTextractAdapter().extract(req)

    assert result.raw_text == "Invoice #123"
    assert result.fields[0].key == "invoice_number"
    assert result.fields[0].value == "123"
    assert result.tables[0].rows == 1
    assert result.tables[0].cols == 1


@pytest.mark.asyncio
async def test_azure_adapter_maps_fields_and_tables():
    payload = {
        "analyzeResult": {
            "content": "Total: 10",
            "keyValuePairs": [
                {
                    "key": {"content": "total"},
                    "value": {"content": "10"},
                    "confidence": 0.95,
                }
            ],
            "tables": [
                {
                    "rowCount": 1,
                    "columnCount": 1,
                    "cells": [{"rowIndex": 0, "columnIndex": 0, "content": "header"}],
                }
            ],
        }
    }

    req = ExtractionRequest(
        document="ignored",
        engine_config=EngineConfig(
            provider="azure",
            model="prebuilt-invoice",
            api_keys={"mock_response_json": json.dumps(payload)},
        ),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    result = await AzureDocIntelligenceAdapter().extract(req)

    assert result.raw_text == "Total: 10"
    assert result.fields[0].key == "total"
    assert result.fields[0].value == "10"
    assert result.tables[0].cells[0].value == "header"


@pytest.mark.asyncio
async def test_gcp_adapter_maps_entities_and_tables():
    payload = {
        "document": {
            "text": "item value",
            "entities": [{"type": "item", "mentionText": "value", "confidence": 0.88}],
            "pages": [
                {
                    "tables": [
                        {
                            "headerRows": [
                                {
                                    "cells": [
                                        {
                                            "layout": {
                                                "textAnchor": {
                                                    "textSegments": [{"startIndex": 0, "endIndex": 4}]
                                                }
                                            }
                                        }
                                    ]
                                }
                            ],
                            "bodyRows": [],
                        }
                    ]
                }
            ],
        }
    }

    req = ExtractionRequest(
        document="ignored",
        engine_config=EngineConfig(
            provider="gcp",
            model="docai",
            api_keys={"mock_response_json": json.dumps(payload)},
        ),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    result = await GCPDocumentAIAdapter().extract(req)

    assert result.raw_text == "item value"
    assert result.fields[0].key == "item"
    assert result.tables[0].cells[0].value == "item"


@pytest.mark.asyncio
async def test_adapter_raises_extraction_error_without_payload():
    req = ExtractionRequest(
        document="not-json",
        engine_config=EngineConfig(provider="aws", model="textract", api_keys={}),
        extraction_target=ExtractionTarget(document_type="invoice"),
    )

    with pytest.raises(ExtractionError):
        await AWSTextractAdapter().extract(req)
