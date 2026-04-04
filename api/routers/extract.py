"""Router: POST /extract — main extraction endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction
from api.services.router_service import route_extraction

router = APIRouter()


@router.post(
    "",
    response_model=StandardizedExtraction,
    summary="Extract structured data from a document",
    description=(
        "Routes the extraction request to the appropriate engine adapter "
        "(OCR Cloud, LLM via LiteLLM, or Local model) and returns a "
        "standardized `StandardizedExtraction` object regardless of the engine used."
    ),
)
async def extract(request: ExtractionRequest) -> StandardizedExtraction:
    return await route_extraction(request)
