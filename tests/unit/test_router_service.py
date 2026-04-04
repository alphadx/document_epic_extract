"""Unit tests for the router service."""

import pytest

from api.core.exceptions import EngineNotFoundError
from api.schemas.request import EngineConfig, ExtractionRequest, ExtractionTarget
from api.services.router_service import _ADAPTER_MAP, _load_adapter


class TestAdapterMap:
    def test_all_expected_providers_registered(self):
        expected = {"aws", "gcp", "azure", "llm_router", "local"}
        assert expected == set(_ADAPTER_MAP.keys())

    def test_adapter_dotted_paths_importable(self):
        """All registered adapters must be importable (even if not yet implemented)."""
        for provider, dotted_path in _ADAPTER_MAP.items():
            cls = _load_adapter(dotted_path)
            assert cls is not None, f"Adapter for '{provider}' could not be loaded"


class TestRouterServiceRaisesOnUnknownProvider:
    @pytest.mark.asyncio
    async def test_unknown_provider_raises(self):
        from api.services.router_service import route_extraction

        req = ExtractionRequest(
            document="base64data",
            engine_config=EngineConfig(provider="aws", model="textract"),
            extraction_target=ExtractionTarget(document_type="invoice"),
        )
        # Patch provider to an unknown value post-construction
        req.engine_config.__dict__["provider"] = "nonexistent"

        with pytest.raises(EngineNotFoundError):
            await route_extraction(req)
