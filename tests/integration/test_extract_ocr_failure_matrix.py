"""Integration matrix for OCR provider failures (auth/timeout/provider-down)."""

from __future__ import annotations

import base64

import pytest
from fastapi.testclient import TestClient

from adapters.ocr.common import normalize_provider_error
from api.main import app

client = TestClient(app)


def _request_body(provider: str, model: str) -> dict:
    document = base64.b64encode(b"invoice_number: INV-1").decode("utf-8")
    return {
        "document": document,
        "engine_config": {
            "provider": provider,
            "model": model,
            "api_keys": {},
        },
        "extraction_target": {"document_type": "invoice"},
    }


@pytest.mark.parametrize(
    ("provider", "model", "patch_target", "error_text", "expected_substring"),
    [
        (
            "aws",
            "textract",
            "adapters.ocr.aws.AWSTextractAdapter._call_textract",
            "credential missing",
            "aws authentication error",
        ),
        (
            "aws",
            "textract",
            "adapters.ocr.aws.AWSTextractAdapter._call_textract",
            "timeout while connecting",
            "aws timeout error",
        ),
        (
            "aws",
            "textract",
            "adapters.ocr.aws.AWSTextractAdapter._call_textract",
            "service unavailable",
            "aws provider error",
        ),
        (
            "gcp",
            "docai",
            "adapters.ocr.gcp.GCPDocumentAIAdapter._call_document_ai",
            "credential rejected",
            "gcp authentication error",
        ),
        (
            "gcp",
            "docai",
            "adapters.ocr.gcp.GCPDocumentAIAdapter._call_document_ai",
            "timeout reached",
            "gcp timeout error",
        ),
        (
            "gcp",
            "docai",
            "adapters.ocr.gcp.GCPDocumentAIAdapter._call_document_ai",
            "upstream unavailable",
            "gcp provider error",
        ),
        (
            "azure",
            "prebuilt-invoice",
            "adapters.ocr.azure.AzureDocIntelligenceAdapter._call_document_intelligence",
            "token invalid",
            "azure authentication error",
        ),
        (
            "azure",
            "prebuilt-invoice",
            "adapters.ocr.azure.AzureDocIntelligenceAdapter._call_document_intelligence",
            "timeout waiting",
            "azure timeout error",
        ),
        (
            "azure",
            "prebuilt-invoice",
            "adapters.ocr.azure.AzureDocIntelligenceAdapter._call_document_intelligence",
            "provider unavailable",
            "azure provider error",
        ),
    ],
)
def test_extract_ocr_provider_failure_matrix(
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
    model: str,
    patch_target: str,
    error_text: str,
    expected_substring: str,
):
    def _raise_error(_request):
        raise normalize_provider_error(provider, Exception(error_text))

    monkeypatch.setattr(patch_target, staticmethod(_raise_error))

    response = client.post("/extract", json=_request_body(provider, model))

    assert response.status_code == 502
    assert expected_substring in response.json()["detail"].lower()
