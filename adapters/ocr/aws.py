"""AWS Textract adapter — maps Textract output to StandardizedExtraction."""

from __future__ import annotations

from adapters.base import BaseAdapter
from adapters.ocr.common import (
    clamp01,
    fail_missing_payload,
    get_document_bytes,
    normalize_provider_error,
    try_load_mock_payload,
)
from api.schemas.request import ExtractionRequest
from api.schemas.response import (
    BoundingBox,
    ExtractedField,
    ExtractedTable,
    StandardizedExtraction,
    TableCell,
)


class AWSTextractAdapter(BaseAdapter):
    """Adapter for Amazon Textract payloads."""

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        payload = try_load_mock_payload(request, provider_label="aws")
        if payload is None:
            payload = self._call_textract(request)
        if payload is None:
            raise fail_missing_payload("aws")

        blocks = payload.get("Blocks", [])
        by_id = {b.get("Id"): b for b in blocks if b.get("Id")}

        raw_lines: list[str] = []
        fields: list[ExtractedField] = []
        tables: list[ExtractedTable] = []

        for block in blocks:
            if block.get("BlockType") == "LINE" and block.get("Text"):
                raw_lines.append(block["Text"])

        key_blocks = [
            b
            for b in blocks
            if b.get("BlockType") == "KEY_VALUE_SET" and "KEY" in b.get("EntityTypes", [])
        ]
        for key_block in key_blocks:
            key_text = self._collect_text(key_block, by_id)
            value_block = self._find_related_value_block(key_block, by_id)
            value_text = self._collect_text(value_block, by_id) if value_block else ""
            if key_text:
                fields.append(
                    ExtractedField(
                        key=key_text,
                        value=value_text,
                        confidence=clamp01(float(key_block.get("Confidence", 0.0)) / 100.0)
                        if key_block.get("Confidence") is not None
                        else None,
                        bounding_box=self._map_bounding_box(key_block.get("Geometry", {})),
                    )
                )

        table_blocks = [b for b in blocks if b.get("BlockType") == "TABLE"]
        for table_block in table_blocks:
            cell_ids = self._relationship_ids(table_block, relationship_type="CHILD")
            cells: list[TableCell] = []
            max_row = 0
            max_col = 0
            for cell_id in cell_ids:
                cell_block = by_id.get(cell_id)
                if not cell_block or cell_block.get("BlockType") != "CELL":
                    continue
                row = max(int(cell_block.get("RowIndex", 1)) - 1, 0)
                col = max(int(cell_block.get("ColumnIndex", 1)) - 1, 0)
                max_row = max(max_row, row + 1)
                max_col = max(max_col, col + 1)
                cells.append(
                    TableCell(
                        row=row,
                        col=col,
                        value=self._collect_text(cell_block, by_id),
                        bounding_box=self._map_bounding_box(cell_block.get("Geometry", {})),
                    )
                )
            tables.append(ExtractedTable(rows=max_row, cols=max_col, cells=cells))

        return StandardizedExtraction(
            raw_text="\n".join(raw_lines).strip(),
            fields=fields,
            tables=tables,
            engine_used=request.engine_config.model,
        )

    @staticmethod
    def _call_textract(request: ExtractionRequest) -> dict | None:
        try:
            import boto3

            client = boto3.client("textract")
            document_bytes = get_document_bytes(request, provider_label="aws")
            response = client.analyze_document(
                Document={"Bytes": document_bytes},
                FeatureTypes=["FORMS", "TABLES"],
            )
            return response
        except ImportError:
            return None
        except Exception as exc:
            raise normalize_provider_error("aws", exc) from exc

    @staticmethod
    def _relationship_ids(block: dict, relationship_type: str) -> list[str]:
        ids: list[str] = []
        for rel in block.get("Relationships", []) or []:
            if rel.get("Type") == relationship_type:
                ids.extend(rel.get("Ids", []) or [])
        return ids

    @staticmethod
    def _collect_text(block: dict | None, by_id: dict[str, dict]) -> str:
        if not block:
            return ""
        child_ids = AWSTextractAdapter._relationship_ids(block, relationship_type="CHILD")
        words: list[str] = []
        for cid in child_ids:
            child = by_id.get(cid)
            if not child:
                continue
            if child.get("BlockType") == "WORD" and child.get("Text"):
                words.append(child["Text"])
            if child.get("BlockType") == "SELECTION_ELEMENT":
                status = child.get("SelectionStatus")
                if status:
                    words.append(status)
        return " ".join(words).strip()

    @staticmethod
    def _find_related_value_block(key_block: dict, by_id: dict[str, dict]) -> dict | None:
        for rel in key_block.get("Relationships", []) or []:
            if rel.get("Type") != "VALUE":
                continue
            for vid in rel.get("Ids", []) or []:
                value_block = by_id.get(vid)
                if value_block and value_block.get("BlockType") == "KEY_VALUE_SET":
                    return value_block
        return None

    @staticmethod
    def _map_bounding_box(geometry: dict) -> BoundingBox | None:
        bb = (geometry or {}).get("BoundingBox")
        if not bb:
            return None
        left = float(bb.get("Left", 0.0))
        top = float(bb.get("Top", 0.0))
        width = float(bb.get("Width", 0.0))
        height = float(bb.get("Height", 0.0))
        return BoundingBox(
            x0=clamp01(left),
            y0=clamp01(top),
            x1=clamp01(left + width),
            y1=clamp01(top + height),
        )
