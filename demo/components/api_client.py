"""HTTP helper utilities for Streamlit demo -> API Gateway calls."""

from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass
class ExtractResponse:
    """Container for extraction call outcome."""

    ok: bool
    payload: dict | None = None
    error: str | None = None
    status_code: int | None = None


def build_extract_payload(
    document_b64: str,
    provider: str,
    model: str,
    api_key: str,
    document_type: str,
    custom_fields: list[str] | None,
) -> dict:
    """Build a `POST /extract` payload aligned with API schema."""
    return {
        "document": document_b64,
        "engine_config": {
            "provider": provider,
            "model": model,
            "api_keys": {provider: api_key} if api_key else {},
        },
        "extraction_target": {
            "document_type": document_type,
            "custom_fields": custom_fields,
        },
    }


def _guidance_for_status(status_code: int) -> str:
    """Return actionable guidance per common API failure status."""
    if status_code == 401:
        return "check API key presence/validity for selected provider"
    if status_code == 403:
        return "check credentials permissions/quota/allowed model"
    if status_code == 422:
        return "review request schema (document base64, provider/model, and extraction_target)"
    if status_code == 429:
        return "provider rate limit hit; retry later or reduce request frequency"
    return "review API logs for full error context"


def call_extract(api_url: str, payload: dict, timeout: int = 60) -> ExtractResponse:
    """Execute extraction call and normalize error handling for UI."""
    url = f"{api_url.rstrip('/')}/extract"

    try:
        response = httpx.post(url, json=payload, timeout=timeout)
    except httpx.TimeoutException:
        return ExtractResponse(ok=False, error="timeout contacting API Gateway")
    except httpx.RequestError as exc:
        return ExtractResponse(ok=False, error=f"connection error contacting API Gateway: {exc}")

    try:
        body = response.json()
    except ValueError:
        body = {}

    if response.status_code >= 400:
        detail = body.get("detail") if isinstance(body, dict) else None
        if isinstance(detail, list):
            detail = "; ".join(str(item) for item in detail)
        if isinstance(detail, dict):
            detail = str(detail)
        detail = detail or "no detail provided"
        guidance = _guidance_for_status(response.status_code)
        return ExtractResponse(
            ok=False,
            error=f"HTTP {response.status_code}: {detail}. Next step: {guidance}.",
            status_code=response.status_code,
        )

    if not isinstance(body, dict):
        return ExtractResponse(ok=False, error="invalid JSON response from API Gateway")

    return ExtractResponse(ok=True, payload=body, status_code=response.status_code)
