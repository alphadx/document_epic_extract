"""SmolVLM2 local adapter — sends requests to the Worker container."""

from __future__ import annotations

from adapters.base import BaseAdapter
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction


class SmolVLM2Adapter(BaseAdapter):
    """
    Adapter for SmolVLM2 running in the local Worker container.

    Forwards the extraction request to the Worker service via HTTP
    and maps the response to the unified schema.

    Requirements:
        httpx >= 0.27  (add to pyproject.toml)
        Worker container running at WORKER_BASE_URL (see api/core/config.py)
    """

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        # TODO: Implement Phase 4 — SmolVLM2 local inference
        # 1. Encode request as JSON and POST to {WORKER_BASE_URL}/infer.
        # 2. Parse worker response into StandardizedExtraction.
        raise NotImplementedError(
            "SmolVLM2Adapter is not yet implemented. "
            "Tracked in Phase 4 of the project roadmap."
        )
