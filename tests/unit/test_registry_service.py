"""Unit tests for the registry service."""

import pytest

from api.services.registry_service import get_all_models


class TestGetAllModels:
    @pytest.mark.asyncio
    async def test_returns_dict(self):
        models = await get_all_models()
        assert isinstance(models, dict)

    @pytest.mark.asyncio
    async def test_has_providers_key(self):
        models = await get_all_models()
        assert "providers" in models

    @pytest.mark.asyncio
    async def test_anthropic_present(self):
        models = await get_all_models()
        providers = models.get("providers", {})
        assert "anthropic" in providers

    @pytest.mark.asyncio
    async def test_local_provider_present(self):
        models = await get_all_models()
        providers = models.get("providers", {})
        assert "local" in providers
