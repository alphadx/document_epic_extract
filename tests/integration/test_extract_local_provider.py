"""Integration tests for POST /extract with local provider."""

from __future__ import annotations

import json

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_extract_local_with_mock_payload_returns_standardized_response():
    mock_payload = {
        "raw_text": "Comprobante local",
        "fields": [{"key": "total", "value": "125.00"}],
        "tables": [],
    }
    body = {
        "document": "ignored-in-mock-mode",
        "engine_config": {
            "provider": "local",
            "model": "smolvlm2-2.2b-instruct",
            "api_keys": {"mock_response_json": json.dumps(mock_payload)},
        },
        "extraction_target": {"document_type": "invoice"},
    }

    resp = client.post("/extract", json=body)

    assert resp.status_code == 200
    payload = resp.json()
    assert payload["raw_text"] == "Comprobante local"
    assert payload["fields"][0]["key"] == "total"
    assert payload["engine_used"] == "local:smolvlm2-2.2b-instruct"
    assert isinstance(payload["processing_time_ms"], float)


def test_extract_local_returns_502_for_invalid_mock_payload():
    body = {
        "document": "ignored-in-mock-mode",
        "engine_config": {
            "provider": "local",
            "model": "smolvlm2-2.2b-instruct",
            "api_keys": {"mock_response_json": "{invalid-json"},
        },
        "extraction_target": {"document_type": "invoice"},
    }

    resp = client.post("/extract", json=body)

    assert resp.status_code == 502
    assert "Invalid local mock payload JSON" in resp.json()["detail"]
