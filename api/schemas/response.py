"""Pydantic schemas for standardized extraction responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Normalized bounding box coordinates [0, 1]."""

    x0: float = Field(..., ge=0.0, le=1.0)
    y0: float = Field(..., ge=0.0, le=1.0)
    x1: float = Field(..., ge=0.0, le=1.0)
    y1: float = Field(..., ge=0.0, le=1.0)


class ExtractedField(BaseModel):
    """A single key-value pair extracted from the document."""

    key: str
    value: str
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    bounding_box: BoundingBox | None = None


class TableCell(BaseModel):
    """A single cell inside an extracted table."""

    row: int = Field(..., ge=0)
    col: int = Field(..., ge=0)
    value: str
    bounding_box: BoundingBox | None = None


class ExtractedTable(BaseModel):
    """Structured table extracted from the document."""

    rows: int = Field(..., ge=0)
    cols: int = Field(..., ge=0)
    cells: list[TableCell] = Field(default_factory=list)


class StandardizedExtraction(BaseModel):
    """
    Unified output schema returned by every engine adapter.

    Both deterministic OCR providers and probabilistic LLMs must
    conform to this contract so that clients remain engine-agnostic.
    """

    raw_text: str = Field(default="", description="Full plain text extracted from the document.")
    fields: list[ExtractedField] = Field(
        default_factory=list,
        description="Key-value pairs with optional confidence and bounding box.",
    )
    tables: list[ExtractedTable] = Field(
        default_factory=list,
        description="Structured tables with row/column/cell granularity.",
    )
    engine_used: str = Field(..., description="Identifier of the engine that produced this result.")
    processing_time_ms: float | None = Field(
        default=None,
        description="Wall-clock time in milliseconds for the extraction call.",
    )


class PrebuiltMetadata(BaseModel):
    """Metadata for listing available prebuilts."""

    id: str
    display_name: str
    version: str
    required_fields: list[str] = Field(default_factory=list)


class CustomPrebuiltResponse(BaseModel):
    """Response model for a registered custom prebuilt."""

    id: str
    display_name: str
    version: str
    system_prompt: str
    required_fields: list[str] = Field(default_factory=list)
    output_schema: str
