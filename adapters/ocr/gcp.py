"""GCP Document AI adapter — maps Document AI output to StandardizedExtraction."""

from __future__ import annotations

import os

from adapters.base import BaseAdapter
from adapters.ocr.common import (
    clamp01,
    fail_missing_payload,
    get_document_bytes,
    normalize_provider_error,
    polygon_to_bbox,
    try_load_mock_payload,
)
from api.schemas.request import ExtractionRequest
from api.schemas.response import ExtractedField, ExtractedTable, StandardizedExtraction, TableCell


class GCPDocumentAIAdapter(BaseAdapter):
    """Adapter for Google Cloud Document AI payloads."""

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        payload = try_load_mock_payload(request, provider_label="gcp")
        if payload is None:
            payload = self._call_document_ai(request)
        if payload is None:
            raise fail_missing_payload("gcp")

        doc = payload.get("document", payload)
        text = doc.get("text", "")

        fields: list[ExtractedField] = []
        for entity in doc.get("entities", []) or []:
            fields.append(
                ExtractedField(
                    key=str(entity.get("type", "")).strip(),
                    value=(
                        entity.get("mentionText")
                        or self._text_from_anchor(text, (entity.get("textAnchor") or {}).get("textSegments"))
                    ).strip(),
                    confidence=clamp01(float(entity.get("confidence", 0.0)))
                    if entity.get("confidence") is not None
                    else None,
                    bounding_box=polygon_to_bbox(
                        (((entity.get("pageAnchor") or {}).get("pageRefs") or [{}])[0].get("boundingPoly")
                        or {}).get("normalizedVertices")
                    ),
                )
            )

        tables: list[ExtractedTable] = []
        for page in doc.get("pages", []) or []:
            for table in page.get("tables", []) or []:
                cells: list[TableCell] = []
                row_idx = 0
                max_cols = 0

                for row in table.get("headerRows", []) or []:
                    row_cells = row.get("cells", []) or []
                    max_cols = max(max_cols, len(row_cells))
                    for col_idx, cell in enumerate(row_cells):
                        cells.append(
                            TableCell(
                                row=row_idx,
                                col=col_idx,
                                value=self._cell_text(text, cell),
                                bounding_box=polygon_to_bbox(
                                    ((cell.get("layout") or {}).get("boundingPoly") or {}).get(
                                        "normalizedVertices"
                                    )
                                ),
                            )
                        )
                    row_idx += 1

                for row in table.get("bodyRows", []) or []:
                    row_cells = row.get("cells", []) or []
                    max_cols = max(max_cols, len(row_cells))
                    for col_idx, cell in enumerate(row_cells):
                        cells.append(
                            TableCell(
                                row=row_idx,
                                col=col_idx,
                                value=self._cell_text(text, cell),
                                bounding_box=polygon_to_bbox(
                                    ((cell.get("layout") or {}).get("boundingPoly") or {}).get(
                                        "normalizedVertices"
                                    )
                                ),
                            )
                        )
                    row_idx += 1

                tables.append(ExtractedTable(rows=row_idx, cols=max_cols, cells=cells))

        return StandardizedExtraction(
            raw_text=text,
            fields=fields,
            tables=tables,
            engine_used=request.engine_config.model,
        )

    @staticmethod
    def _call_document_ai(request: ExtractionRequest) -> dict | None:
        try:
            from google.cloud import documentai

            project_id = request.engine_config.api_keys.get("gcp_project_id") or os.getenv("GCP_PROJECT_ID")
            location = request.engine_config.api_keys.get("gcp_location") or os.getenv("GCP_LOCATION", "us")
            processor_id = request.engine_config.api_keys.get("gcp_processor_id") or os.getenv(
                "GCP_PROCESSOR_ID"
            )
            if not (project_id and processor_id):
                return None

            client = documentai.DocumentProcessorServiceClient()
            name = client.processor_path(project_id, location, processor_id)
            raw_document = documentai.RawDocument(
                content=get_document_bytes(request, provider_label="gcp"),
                mime_type="application/pdf",
            )
            req = documentai.ProcessRequest(name=name, raw_document=raw_document)
            result = client.process_document(request=req)
            if hasattr(result, "to_dict"):
                return result.to_dict()
            if hasattr(result, "document") and hasattr(result.document, "to_dict"):
                return {"document": result.document.to_dict()}
            return None
        except ImportError:
            return None
        except Exception as exc:
            raise normalize_provider_error("gcp", exc) from exc

    @staticmethod
    def _text_from_anchor(text: str, segments: list[dict] | None) -> str:
        if not segments:
            return ""
        fragments: list[str] = []
        for seg in segments:
            start = int(seg.get("startIndex", 0) or 0)
            end = int(seg.get("endIndex", 0) or 0)
            if 0 <= start <= end <= len(text):
                fragments.append(text[start:end])
        return "".join(fragments)

    @classmethod
    def _cell_text(cls, full_text: str, cell: dict) -> str:
        layout = cell.get("layout") or {}
        text_anchor = layout.get("textAnchor") or {}
        return cls._text_from_anchor(full_text, text_anchor.get("textSegments"))
