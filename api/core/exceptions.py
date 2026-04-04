"""Custom HTTP exceptions for OmniExtract Gateway."""

from __future__ import annotations

from fastapi import HTTPException, status


class EngineNotFoundError(HTTPException):
    def __init__(self, provider: str) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"No adapter registered for provider '{provider}'.",
        )


class PrebuiltNotFoundError(HTTPException):
    def __init__(self, document_type: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prebuilt template '{document_type}' not found.",
        )


class ExtractionError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Extraction failed: {detail}",
        )
