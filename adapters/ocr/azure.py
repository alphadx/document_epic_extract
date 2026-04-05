"""Azure Document Intelligence adapter — maps output to StandardizedExtraction."""

from __future__ import annotations

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


class AzureDocIntelligenceAdapter(BaseAdapter):
    """Adapter for Azure AI Document Intelligence payloads."""

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        payload = try_load_mock_payload(request, provider_label="azure")
        if payload is None:
            payload = self._call_document_intelligence(request)
        if payload is None:
            raise fail_missing_payload("azure")

        result = payload.get("analyzeResult", payload)

        raw_text = result.get("content", "")
        fields: list[ExtractedField] = []

        for pair in result.get("keyValuePairs", []) or []:
            key_obj = pair.get("key", {}) or {}
            value_obj = pair.get("value", {}) or {}
            key = key_obj.get("content", "").strip()
            value = value_obj.get("content", "").strip()
            if key:
                fields.append(
                    ExtractedField(
                        key=key,
                        value=value,
                        confidence=clamp01(float(pair.get("confidence", 0.0)))
                        if pair.get("confidence") is not None
                        else None,
                        bounding_box=polygon_to_bbox((key_obj.get("boundingRegions") or [{}])[0].get("polygon")),
                    )
                )

        for doc in result.get("documents", []) or []:
            for field_name, field_data in (doc.get("fields") or {}).items():
                if not isinstance(field_data, dict):
                    continue
                if any(existing.key == field_name for existing in fields):
                    continue
                value = (
                    field_data.get("content")
                    or field_data.get("valueString")
                    or str(field_data.get("valueNumber", ""))
                )
                fields.append(
                    ExtractedField(
                        key=field_name,
                        value=str(value).strip(),
                        confidence=clamp01(float(field_data.get("confidence", 0.0)))
                        if field_data.get("confidence") is not None
                        else None,
                        bounding_box=polygon_to_bbox(
                            (field_data.get("boundingRegions") or [{}])[0].get("polygon")
                        ),
                    )
                )

        tables: list[ExtractedTable] = []
        for table in result.get("tables", []) or []:
            rows = int(table.get("rowCount", 0) or 0)
            cols = int(table.get("columnCount", 0) or 0)
            cells: list[TableCell] = []
            for cell in table.get("cells", []) or []:
                cells.append(
                    TableCell(
                        row=max(int(cell.get("rowIndex", 0)), 0),
                        col=max(int(cell.get("columnIndex", 0)), 0),
                        value=str(cell.get("content", "")),
                        bounding_box=polygon_to_bbox(
                            (cell.get("boundingRegions") or [{}])[0].get("polygon")
                        ),
                    )
                )
            tables.append(ExtractedTable(rows=rows, cols=cols, cells=cells))

        return StandardizedExtraction(
            raw_text=raw_text,
            fields=fields,
            tables=tables,
            engine_used=request.engine_config.model,
        )

    @staticmethod
    def _call_document_intelligence(request: ExtractionRequest) -> dict | None:
        try:
            from azure.ai.documentintelligence import DocumentIntelligenceClient
            from azure.core.credentials import AzureKeyCredential

            endpoint = request.engine_config.api_keys.get("azure_endpoint")
            key = request.engine_config.api_keys.get("azure_key")
            if not endpoint or not key:
                return None

            client = DocumentIntelligenceClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(key),
            )
            poller = client.begin_analyze_document(
                model_id=request.engine_config.model or "prebuilt-document",
                body=get_document_bytes(request, provider_label="azure"),
            )
            result = poller.result()
            if hasattr(result, "as_dict"):
                return result.as_dict()
            if hasattr(result, "to_dict"):
                return result.to_dict()
            return None
        except ImportError:
            return None
        except Exception as exc:
            raise normalize_provider_error("azure", exc) from exc
