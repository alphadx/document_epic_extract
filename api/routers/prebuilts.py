"""Router: GET /prebuilts — list and manage prebuilt templates."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from api.schemas.request import CustomPrebuiltRequest
from api.schemas.response import CustomPrebuiltResponse, PrebuiltMetadata
from api.services.prebuilt_service import get_all_prebuilts, register_custom_prebuilt

router = APIRouter()


@router.get(
    "",
    summary="List available prebuilt templates",
    response_model=list[PrebuiltMetadata],
)
async def list_prebuilts() -> list[dict]:
    """Return all available prebuilt document templates."""
    return await get_all_prebuilts()


@router.post(
    "/custom",
    summary="Register a custom prebuilt template",
    response_model=CustomPrebuiltResponse,
    description=(
        "Provide an ID and a list of field names; the gateway will auto-generate "
        "an optimized LLM prompt and persist it in the custom prebuilts catalog."
    ),
)
async def create_custom_prebuilt(payload: CustomPrebuiltRequest) -> dict:
    """Register a new Custom Prebuilt and return the generated template."""
    try:
        return await register_custom_prebuilt(
            id=payload.id,
            display_name=payload.display_name,
            fields=payload.fields,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
