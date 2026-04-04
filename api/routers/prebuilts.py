"""Router: GET /prebuilts — list and manage prebuilt templates."""

from __future__ import annotations

from fastapi import APIRouter

from api.services.prebuilt_service import get_all_prebuilts, register_custom_prebuilt

router = APIRouter()


@router.get(
    "",
    summary="List available prebuilt templates",
)
async def list_prebuilts() -> list[dict]:
    """Return all available prebuilt document templates."""
    return await get_all_prebuilts()


@router.post(
    "/custom",
    summary="Register a custom prebuilt template",
    description=(
        "Provide an ID and a list of field names; the gateway will auto-generate "
        "an optimized LLM prompt and persist it in the custom prebuilts catalog."
    ),
)
async def create_custom_prebuilt(
    id: str,
    display_name: str,
    fields: list[str],
) -> dict:
    """Register a new Custom Prebuilt and return the generated template."""
    return await register_custom_prebuilt(id=id, display_name=display_name, fields=fields)
