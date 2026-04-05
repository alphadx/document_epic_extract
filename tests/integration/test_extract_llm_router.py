"""Integration tests for POST /extract with llm_router provider."""

from __future__ import annotations

from fastapi.testclient import TestClient

from adapters.llm import litellm_adapter
from api.main import app


def test_extract_with_llm_router_success(monkeypatch):
    captured_kwargs = {}

    async def fake_load_prebuilt(document_type: str):
        assert document_type == "invoice"
        return {
            "id": "invoice",
            "system_prompt": "Extract all fields",
            "required_fields": ["invoice_number", "total_amount"],
        }

    async def fake_acompletion(**kwargs):
        captured_kwargs.update(kwargs)
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"raw_text":"invoice text","fields":[],"tables":[],'
                            '"engine_used":"llm_router:gpt-4o"}'
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr(litellm_adapter, "load_prebuilt", fake_load_prebuilt)
    monkeypatch.setattr(litellm_adapter, "_litellm_acompletion", lambda: fake_acompletion)

    client = TestClient(app)
    response = client.post(
        "/extract",
        json={
            "document": "ZmFrZV9pbWFnZQ==",
            "engine_config": {
                "provider": "llm_router",
                "model": "gpt-4o",
                "api_keys": {"model": "do-not-override", "api_key": "secret"},
            },
            "extraction_target": {
                "document_type": "invoice",
                "custom_fields": ["invoice_number", "total_amount"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["raw_text"] == "invoice text"
    assert payload["engine_used"] == "llm_router:gpt-4o"
    assert isinstance(payload["processing_time_ms"], float)
    assert captured_kwargs["model"] == "gpt-4o"
    assert captured_kwargs["response_format"] == {"type": "json_object"}
