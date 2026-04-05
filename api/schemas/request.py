"""Pydantic schemas for extraction requests."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class EngineConfig(BaseModel):
    """Configuration for the inference engine to use."""

    provider: Literal["aws", "gcp", "azure", "local", "llm_router"] = Field(
        ...,
        description="Backend provider to route the extraction request to.",
    )
    model: str = Field(
        ...,
        examples=["claude-3-5-sonnet-20241022", "gpt-4o", "smolvlm2-2.2b-instruct"],
        description="Model identifier as listed in the registry or a custom endpoint.",
    )
    api_keys: dict[str, str] = Field(
        default_factory=dict,
        description="Per-session credentials injected by the caller.",
    )
    custom_endpoint: str | None = Field(
        default=None,
        description="BYOE — custom base URL for models not in the official registry.",
    )


class ExtractionTarget(BaseModel):
    """Describes what to extract and how."""

    document_type: str = Field(
        ...,
        examples=["invoice", "receipt", "id_card", "bank_statement"],
        description="Prebuilt template ID or 'free' for unstructured extraction.",
    )
    custom_fields: list[str] | None = Field(
        default=None,
        description="List of field names for on-the-fly Custom Prebuilt generation.",
    )


class ExtractionRequest(BaseModel):
    """Top-level request body for POST /extract."""

    document: str = Field(
        ...,
        description="Base64-encoded image / PDF or a publicly accessible URL.",
    )
    engine_config: EngineConfig
    extraction_target: ExtractionTarget


class CustomPrebuiltRequest(BaseModel):
    """Request body for registering a custom prebuilt template."""

    id: str = Field(..., description="Unique prebuilt identifier.")
    display_name: str = Field(..., description="Human-readable template name.")
    fields: list[str] = Field(..., min_length=1, description="Fields required by the template.")
