"""Unit tests for the prebuilt service."""

import pytest

from api.core.exceptions import PrebuiltNotFoundError
from api.services.prebuilt_service import get_all_prebuilts, load_prebuilt


class TestGetAllPrebuilts:
    @pytest.mark.asyncio
    async def test_returns_list(self):
        prebuilts = await get_all_prebuilts()
        assert isinstance(prebuilts, list)

    @pytest.mark.asyncio
    async def test_includes_invoice(self):
        prebuilts = await get_all_prebuilts()
        ids = [p["id"] for p in prebuilts]
        assert "invoice" in ids

    @pytest.mark.asyncio
    async def test_includes_receipt(self):
        prebuilts = await get_all_prebuilts()
        ids = [p["id"] for p in prebuilts]
        assert "receipt" in ids


class TestLoadPrebuilt:
    @pytest.mark.asyncio
    async def test_load_invoice(self):
        template = await load_prebuilt("invoice")
        assert template["id"] == "invoice"
        assert "required_fields" in template
        assert "system_prompt" in template

    @pytest.mark.asyncio
    async def test_load_nonexistent_raises(self):
        with pytest.raises(PrebuiltNotFoundError):
            await load_prebuilt("nonexistent_document_type_xyz")
