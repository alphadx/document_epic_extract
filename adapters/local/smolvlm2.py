"""SmolVLM2 local adapter — sends requests to the Worker container."""

from __future__ import annotations

import json

import httpx

from adapters.base import BaseAdapter
from api.core.config import settings
from api.core.exceptions import ExtractionError
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
        payload = await self._resolve_payload(request)
        standardized = self._to_standardized_extraction(payload, request)
        if not standardized.engine_used:
            standardized.engine_used = f"local:{request.engine_config.model}"
        return standardized

    async def _call_worker(self, request: ExtractionRequest) -> dict:
        infer_url = f"{settings.worker_base_url.rstrip('/')}/infer"
        body = {
            "document": request.document,
            "engine_config": {
                "provider": request.engine_config.provider,
                "model": request.engine_config.model,
                "custom_endpoint": request.engine_config.custom_endpoint,
            },
            "extraction_target": {
                "document_type": request.extraction_target.document_type,
                "custom_fields": request.extraction_target.custom_fields,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=settings.http_timeout) as client:
                response = await client.post(infer_url, json=body)
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, dict):
                    raise ExtractionError("Local worker returned a non-JSON object.")
                return data
        except httpx.HTTPStatusError as exc:
            raise ExtractionError(
                f"Local worker returned HTTP {exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise ExtractionError("Local worker request failed.") from exc
        except ValueError as exc:
            raise ExtractionError("Local worker returned invalid JSON.") from exc

    async def _resolve_payload(self, request: ExtractionRequest) -> dict:
        mock_response_json = request.engine_config.api_keys.get("mock_response_json")
        if mock_response_json:
            try:
                payload = json.loads(mock_response_json)
            except json.JSONDecodeError as exc:
                raise ExtractionError("Invalid local mock payload JSON.") from exc
            if not isinstance(payload, dict):
                raise ExtractionError("Local mock payload must be a JSON object.")
            return payload
        return await self._call_worker(request)

    @staticmethod
    def _to_standardized_extraction(
        payload: dict,
        request: ExtractionRequest,
    ) -> StandardizedExtraction:
        candidate = payload.get("result", payload)
        if not isinstance(candidate, dict):
            raise ExtractionError("Local worker payload has invalid format.")

        if "engine_used" not in candidate or not candidate.get("engine_used"):
            candidate = {
                **candidate,
                "engine_used": f"local:{request.engine_config.model}",
            }

        try:
            return StandardizedExtraction.model_validate(candidate)
        except Exception as exc:  # noqa: BLE001
            raise ExtractionError("Local worker payload is incompatible with contract.") from exc
