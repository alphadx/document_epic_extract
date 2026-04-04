"""Router: GET /registry/models — dynamic model registry."""

from __future__ import annotations

from fastapi import APIRouter

from api.services.registry_service import get_all_models

router = APIRouter()


@router.get(
    "/models",
    summary="List all models in the dynamic registry",
    description=(
        "Returns the full list of models available in `registry/models.yaml`. "
        "Update this file via Pull Request to add new models to the registry."
    ),
)
async def list_models() -> dict:
    """Return the full model registry."""
    return await get_all_models()
