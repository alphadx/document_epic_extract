"""Integration tests for POST /extract with OCR cloud providers (mock payload mode)."""

from __future__ import annotations

import json

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def _request_body(provider: str, model: str, payload: dict) -> dict:
    return {
        "document": "ignored",
        "engine_config": {
            "provider": provider,
            "model": model,
            "api_keys": {"mock_response_json": json.dumps(payload)},
        },
        "extraction_target": {"document_type": "invoice"},
    }


def test_extract_aws_with_mock_payload_returns_standardized_response():
    payload = {
        "Blocks": [
            {"Id": "l1", "BlockType": "LINE", "Text": "Factura 100"},
            {
                "Id": "k1",
                "BlockType": "KEY_VALUE_SET",
                "EntityTypes": ["KEY"],
                "Confidence": 96.0,
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
            {"Id": "w2", "BlockType": "WORD", "Text": "100"},
        ]
    }

    resp = client.post("/extract", json=_request_body("aws", "textract", payload))

    assert resp.status_code == 200
    data = resp.json()
    assert data["raw_text"] == "Factura 100"
    assert data["fields"][0]["key"] == "invoice_number"
    assert data["engine_used"] == "textract"
    assert data["processing_time_ms"] is not None


def test_extract_azure_with_mock_payload_returns_standardized_response():
    payload = {
        "analyzeResult": {
            "content": "Total 250",
            "keyValuePairs": [
                {
                    "key": {"content": "total"},
                    "value": {"content": "250"},
                    "confidence": 0.91,
                }
            ],
            "tables": [
                {
                    "rowCount": 1,
                    "columnCount": 1,
                    "cells": [{"rowIndex": 0, "columnIndex": 0, "content": "item"}],
                }
            ],
        }
    }

    resp = client.post("/extract", json=_request_body("azure", "prebuilt-invoice", payload))

    assert resp.status_code == 200
    data = resp.json()
    assert data["raw_text"] == "Total 250"
    assert data["fields"][0]["key"] == "total"
    assert data["tables"][0]["rows"] == 1


def test_extract_gcp_with_mock_payload_returns_standardized_response():
    payload = {
        "document": {
            "text": "id 999",
            "entities": [{"type": "doc_id", "mentionText": "999", "confidence": 0.77}],
            "pages": [],
        }
    }

    resp = client.post("/extract", json=_request_body("gcp", "docai", payload))

    assert resp.status_code == 200
    data = resp.json()
    assert data["raw_text"] == "id 999"
    assert data["fields"][0]["key"] == "doc_id"
    assert data["fields"][0]["value"] == "999"


def test_extract_returns_502_when_payload_is_missing():
    body = {
        "document": "not-json",
        "engine_config": {"provider": "aws", "model": "textract", "api_keys": {}},
        "extraction_target": {"document_type": "invoice"},
    }

    resp = client.post("/extract", json=body)

    assert resp.status_code == 502
    assert "Extraction failed" in resp.json()["detail"]
