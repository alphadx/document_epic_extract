"""AWS Textract adapter — maps Textract output to StandardizedExtraction."""

from __future__ import annotations

from adapters.base import BaseAdapter
from api.schemas.request import ExtractionRequest
from api.schemas.response import BoundingBox, StandardizedExtraction


class AWSTextractAdapter(BaseAdapter):
    """
    Adapter for Amazon Textract.

    Calls the Textract AnalyzeDocument / AnalyzeExpense APIs and maps
    blocks, key-value sets, and tables to the unified schema.

    Requirements:
        boto3 >= 1.34  (add to pyproject.toml extras)
    """

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        # TODO: Implement Phase 2 — AWS Textract integration
        # 1. Decode base64 document or fetch from URL.
        # 2. Call boto3 textract client with AnalyzeDocument / AnalyzeExpense.
        # 3. Map Block objects (KEY_VALUE_SET, TABLE, CELL, LINE) to schema.
        raise NotImplementedError(
            "AWSTextractAdapter is not yet implemented. "
            "Tracked in Phase 2 of the project roadmap."
        )

    @staticmethod
    def _map_bounding_box(geometry: dict) -> BoundingBox:
        """Convert Textract Geometry.BoundingBox to normalized BoundingBox."""
        bb = geometry["BoundingBox"]
        return BoundingBox(
            x0=bb["Left"],
            y0=bb["Top"],
            x1=bb["Left"] + bb["Width"],
            y1=bb["Top"] + bb["Height"],
        )
