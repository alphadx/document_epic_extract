"""Unit tests for custom prebuilt registration service."""

from __future__ import annotations

from pathlib import Path

import pytest

from api.services import prebuilt_service


@pytest.mark.asyncio
async def test_register_custom_prebuilt_persists_yaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(prebuilt_service, "_PREBUILT_DIR", tmp_path)

    template = await prebuilt_service.register_custom_prebuilt(
        id="accident_report",
        display_name="Accident Report",
        fields=["claim_id", "incident_date"],
    )

    out_path = tmp_path / "custom" / "accident_report.yaml"
    assert out_path.exists()
    assert template["id"] == "accident_report"
    assert "claim_id" in template["required_fields"]


@pytest.mark.asyncio
async def test_register_custom_prebuilt_rejects_invalid_id(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(prebuilt_service, "_PREBUILT_DIR", tmp_path)

    with pytest.raises(ValueError, match="only alphanumeric"):
        await prebuilt_service.register_custom_prebuilt(
            id="../../etc/passwd",
            display_name="Bad",
            fields=["x"],
        )
