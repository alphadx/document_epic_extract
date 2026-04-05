"""Unit tests for local Worker app contract."""

from __future__ import annotations

import base64

from fastapi.testclient import TestClient

from adapters.local.worker_app import app

client = TestClient(app)


def test_worker_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_worker_infer_returns_contract_result():
    text_payload = "invoice_number: INV-44\ntotal_amount: 89.10"
    document = base64.b64encode(text_payload.encode("utf-8")).decode("utf-8")
    body = {
        "document": document,
        "engine_config": {"provider": "local", "model": "smolvlm2-2.2b-instruct"},
        "extraction_target": {"document_type": "invoice"},
    }

    resp = client.post("/infer", json=body)
    assert resp.status_code == 200
    payload = resp.json()

    assert payload["backend"] in {"heuristic", "smolvlm2"}
    assert "device" in payload
    assert payload["result"]["engine_used"] == "local_worker:smolvlm2-2.2b-instruct"
    assert payload["result"]["fields"][0]["key"] == "invoice_number"
