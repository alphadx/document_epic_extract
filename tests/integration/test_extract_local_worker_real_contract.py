"""Integration test for API local provider against Worker app contract (no mock payload)."""

from __future__ import annotations

import base64

import httpx
from fastapi.testclient import TestClient

from adapters.local.worker_app import app as worker_app
from api.main import app as api_app


def test_extract_local_calls_worker_contract_without_mock(monkeypatch):
    transport = httpx.ASGITransport(app=worker_app)
    real_async_client = httpx.AsyncClient

    class WorkerBackedAsyncClient:
        def __init__(self, timeout=None):  # noqa: ANN001
            self._client = real_async_client(transport=transport, base_url="http://worker", timeout=timeout)

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            await self._client.aclose()
            return None

        async def post(self, url, json):  # noqa: ANN001
            return await self._client.post("/infer", json=json)

    monkeypatch.setattr(
        "adapters.local.smolvlm2.httpx.AsyncClient",
        lambda timeout: WorkerBackedAsyncClient(timeout=timeout),
    )

    encoded_text = base64.b64encode(b"invoice_number: INV-77\ntotal_amount: 120.00").decode("utf-8")
    body = {
        "document": encoded_text,
        "engine_config": {
            "provider": "local",
            "model": "smolvlm2-2.2b-instruct",
            "api_keys": {},
        },
        "extraction_target": {"document_type": "invoice"},
    }

    client = TestClient(api_app)
    resp = client.post("/extract", json=body)

    assert resp.status_code == 200
    payload = resp.json()
    assert payload["engine_used"] == "local_worker:smolvlm2-2.2b-instruct"
    assert payload["fields"][0]["key"] == "invoice_number"
    assert payload["fields"][1]["value"] == "120.00"
