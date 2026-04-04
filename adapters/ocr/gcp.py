"""GCP Document AI adapter — maps Document AI output to StandardizedExtraction."""

from __future__ import annotations

from adapters.base import BaseAdapter
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction


class GCPDocumentAIAdapter(BaseAdapter):
    """
    Adapter for Google Cloud Document AI.

    Calls the Document AI ProcessDocument API and maps entities,
    form fields, and tables to the unified schema.

    Requirements:
        google-cloud-documentai >= 2.0  (add to pyproject.toml extras)
    """

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        # TODO: Implement Phase 2 — GCP Document AI integration
        # 1. Decode base64 document or fetch from URL.
        # 2. Call DocumentAI ProcessorServiceClient.process_document().
        # 3. Map Document.entities and Document.pages.tables to schema.
        raise NotImplementedError(
            "GCPDocumentAIAdapter is not yet implemented. "
            "Tracked in Phase 2 of the project roadmap."
        )
