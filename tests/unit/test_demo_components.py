"""Unit tests for demo helpers/components."""

from __future__ import annotations

from io import BytesIO

import httpx
from PIL import Image

from demo.components.api_client import build_extract_payload, call_extract
from demo.components.bbox_renderer import render_bboxes
from demo.components.comparison_panel import _format_confidence


class DummyResponse:
    """Simple stand-in for `httpx.Response` in unit tests."""

    def __init__(self, status_code: int, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


def test_build_extract_payload_includes_engine_and_target():
    payload = build_extract_payload(
        document_b64="abc123",
        provider="aws",
        model="textract-v1",
        api_key="secret",
        document_type="invoice",
        custom_fields=["invoice_number"],
    )

    assert payload["document"] == "abc123"
    assert payload["engine_config"]["provider"] == "aws"
    assert payload["engine_config"]["api_keys"] == {"aws": "secret"}
    assert payload["extraction_target"]["custom_fields"] == ["invoice_number"]


def test_call_extract_returns_guided_message_for_422(monkeypatch):
    def fake_post(*args, **kwargs):
        return DummyResponse(422, {"detail": "invalid request"})

    monkeypatch.setattr("demo.components.api_client.httpx.post", fake_post)
    response = call_extract("http://localhost:8000", payload={"document": "abc"})

    assert response.ok is False
    assert response.status_code == 422
    assert "Next step" in response.error
    assert "review request schema" in response.error


def test_call_extract_wraps_timeout(monkeypatch):
    def fake_post(*args, **kwargs):
        raise httpx.TimeoutException("timeout")

    monkeypatch.setattr("demo.components.api_client.httpx.post", fake_post)
    response = call_extract("http://localhost:8000", payload={})

    assert response.ok is False
    assert "timeout" in (response.error or "")


def test_format_confidence_handles_none_and_zero():
    assert _format_confidence(None) == "—"
    assert _format_confidence(0.0) == "0%"
    assert _format_confidence(0.42) == "42%"


def test_render_bboxes_handles_non_image_bytes(monkeypatch):
    captured: list[str] = []

    def fake_info(msg: str):
        captured.append(msg)

    monkeypatch.setattr("demo.components.bbox_renderer.st.info", fake_info)
    render_bboxes(b"%PDF-1.7\n...", fields=[])

    assert captured
    assert "Preview no disponible" in captured[0]


def test_render_bboxes_draws_image(monkeypatch):
    img = Image.new("RGB", (10, 10), color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    called = {"image": False}

    def fake_image(*args, **kwargs):
        called["image"] = True

    monkeypatch.setattr("demo.components.bbox_renderer.st.image", fake_image)
    render_bboxes(
        buffer.getvalue(),
        fields=[{"key": "total", "bounding_box": {"x0": 0.1, "y0": 0.1, "x1": 0.5, "y1": 0.5}}],
    )

    assert called["image"] is True
