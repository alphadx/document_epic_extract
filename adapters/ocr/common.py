"""Shared helpers for OCR cloud adapters."""

from __future__ import annotations

import base64
import json
from typing import Any

import httpx

from api.core.exceptions import ExtractionError
from api.schemas.request import ExtractionRequest
from api.schemas.response import BoundingBox


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def polygon_to_bbox(points: list[dict[str, float]] | None) -> BoundingBox | None:
    if not points:
        return None
    xs = [p.get("x", 0.0) for p in points]
    ys = [p.get("y", 0.0) for p in points]
    return BoundingBox(x0=clamp01(min(xs)), y0=clamp01(min(ys)), x1=clamp01(max(xs)), y1=clamp01(max(ys)))


def try_load_mock_payload(request: ExtractionRequest, provider_label: str) -> dict[str, Any] | None:
    """Try loading provider payload from mock/inlined JSON. Return None when absent."""
    raw = request.engine_config.api_keys.get("mock_response_json")
    if raw:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ExtractionError(f"Invalid mock_response_json for {provider_label}: {exc}") from exc
        if isinstance(payload, dict):
            return payload
        raise ExtractionError(f"mock_response_json for {provider_label} must decode to an object.")

    doc = request.document.strip()

    if doc.startswith("{") and doc.endswith("}"):
        try:
            payload = json.loads(doc)
        except json.JSONDecodeError as exc:
            raise ExtractionError(f"Invalid inline JSON document for {provider_label}: {exc}") from exc
        if isinstance(payload, dict):
            return payload

    try:
        decoded = base64.b64decode(doc, validate=True).decode("utf-8")
        if decoded.startswith("{") and decoded.endswith("}"):
            payload = json.loads(decoded)
            if isinstance(payload, dict):
                return payload
    except Exception:
        pass

    return None


def get_document_bytes(request: ExtractionRequest, provider_label: str) -> bytes:
    """Decode request document as bytes from base64 or URL."""
    doc = request.document.strip()
    if doc.startswith("http://") or doc.startswith("https://"):
        try:
            resp = httpx.get(doc, timeout=20.0)
            resp.raise_for_status()
            return resp.content
        except Exception as exc:
            raise ExtractionError(f"Unable to download document for {provider_label}: {exc}") from exc

    try:
        return base64.b64decode(doc, validate=True)
    except Exception as exc:
        raise ExtractionError(
            f"{provider_label} adapter needs base64 document or URL when mock_response_json is not provided."
        ) from exc


def fail_missing_payload(provider_label: str) -> ExtractionError:
    return ExtractionError(
        f"{provider_label} adapter requires a provider payload or valid SDK configuration. "
        "Provide engine_config.api_keys.mock_response_json for local tests."
    )


def normalize_provider_error(provider_label: str, exc: Exception) -> ExtractionError:
    msg = str(exc)
    if isinstance(exc, ImportError):
        return ExtractionError(
            f"{provider_label} SDK is not installed. Install provider extras or use mock_response_json."
        )
    if "credential" in msg.lower() or "auth" in msg.lower() or "token" in msg.lower():
        return ExtractionError(f"{provider_label} authentication error: {msg}")
    if "timeout" in msg.lower():
        return ExtractionError(f"{provider_label} timeout error: {msg}")
    return ExtractionError(f"{provider_label} provider error: {msg}")
