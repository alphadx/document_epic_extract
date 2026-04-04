"""Integration tests for custom prebuilt endpoint."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app
from api.services import prebuilt_service


def test_create_custom_prebuilt_endpoint(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(prebuilt_service, "_PREBUILT_DIR", tmp_path)

    client = TestClient(app)
    response = client.post(
        "/prebuilts/custom",
        json={
            "id": "vehicle_claim",
            "display_name": "Vehicle Claim",
            "fields": ["claim_number", "plate"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "vehicle_claim"
    assert payload["display_name"] == "Vehicle Claim"

    yaml_path = tmp_path / "custom" / "vehicle_claim.yaml"
    assert yaml_path.exists()


def test_create_custom_prebuilt_invalid_id_returns_422(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(prebuilt_service, "_PREBUILT_DIR", tmp_path)

    client = TestClient(app)
    response = client.post(
        "/prebuilts/custom",
        json={
            "id": "../../etc/passwd",
            "display_name": "Bad",
            "fields": ["x"],
        },
    )

    assert response.status_code == 422
    assert "alphanumeric" in response.json()["detail"]


def test_create_custom_prebuilt_empty_fields_returns_422():
    client = TestClient(app)
    response = client.post(
        "/prebuilts/custom",
        json={
            "id": "empty_fields",
            "display_name": "Empty Fields",
            "fields": [],
        },
    )

    assert response.status_code == 422
