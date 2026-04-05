"""Engine routing service — selects and delegates to the correct adapter."""

from __future__ import annotations

import time

from api.core.exceptions import EngineNotFoundError
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction

# Lazy imports to keep startup fast; adapters are only loaded when needed.
_ADAPTER_MAP: dict[str, str] = {
    "aws": "adapters.ocr.aws.AWSTextractAdapter",
    "gcp": "adapters.ocr.gcp.GCPDocumentAIAdapter",
    "azure": "adapters.ocr.azure.AzureDocIntelligenceAdapter",
    "llm_router": "adapters.llm.litellm_adapter.LiteLLMVisionAdapter",
    "local": "adapters.local.smolvlm2.SmolVLM2Adapter",
}


def _load_adapter(dotted_path: str):
    """Dynamically load an adapter class from its dotted module path."""
    module_path, class_name = dotted_path.rsplit(".", 1)
    import importlib

    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def _resolve_adapter_path(provider: str, model: str) -> str:
    """Resolve adapter dotted path, allowing local routing by model family."""
    if provider != "local":
        return _ADAPTER_MAP[provider]

    normalized_model = (model or "").lower()
    if "flan-t5" in normalized_model:
        return "adapters.local.flant5.FlanT5Adapter"

    return _ADAPTER_MAP[provider]


async def route_extraction(request: ExtractionRequest) -> StandardizedExtraction:
    """
    Select the appropriate engine adapter and execute the extraction.

    Raises:
        EngineNotFoundError: If no adapter is registered for the requested provider.
    """
    provider = request.engine_config.provider
    if provider not in _ADAPTER_MAP:
        raise EngineNotFoundError(provider)

    adapter_class = _load_adapter(_resolve_adapter_path(provider, request.engine_config.model))
    adapter = adapter_class()

    start = time.monotonic()
    result: StandardizedExtraction = await adapter.extract(request)
    elapsed_ms = (time.monotonic() - start) * 1000

    result.processing_time_ms = round(elapsed_ms, 2)
    return result
