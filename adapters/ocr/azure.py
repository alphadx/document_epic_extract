"""Azure Document Intelligence adapter — maps output to StandardizedExtraction."""

from __future__ import annotations

from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction
from adapters.base import BaseAdapter


class AzureDocIntelligenceAdapter(BaseAdapter):
    """
    Adapter for Azure AI Document Intelligence (formerly Form Recognizer).

    Calls the Analyze Document API and maps key-value pairs,
    tables, and document fields to the unified schema.

    Requirements:
        azure-ai-documentintelligence >= 1.0  (add to pyproject.toml extras)
    """

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        # TODO: Implement Phase 2 — Azure Document Intelligence integration
        # 1. Decode base64 document or fetch from URL.
        # 2. Call DocumentIntelligenceClient.begin_analyze_document().
        # 3. Map AnalyzeResult.key_value_pairs and tables to schema.
        raise NotImplementedError(
            "AzureDocIntelligenceAdapter is not yet implemented. "
            "Tracked in Phase 2 of the project roadmap."
        )
