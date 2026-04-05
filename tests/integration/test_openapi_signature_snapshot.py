"""Snapshot-style OpenAPI signature checks for key public endpoints."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app


def _build_signature(schema: dict) -> dict:
    return {
        "extract_post_200_ref": schema["paths"]["/extract"]["post"]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]["$ref"],
        "prebuilts_get_200_items_ref": schema["paths"]["/prebuilts"]["get"]["responses"]["200"][
            "content"
        ]["application/json"]["schema"]["items"]["$ref"],
        "prebuilts_custom_post_request_ref": schema["paths"]["/prebuilts/custom"]["post"][
            "requestBody"
        ]["content"]["application/json"]["schema"]["$ref"],
        "prebuilts_custom_post_200_ref": schema["paths"]["/prebuilts/custom"]["post"]["responses"][
            "200"
        ]["content"]["application/json"]["schema"]["$ref"],
        "prebuilts_custom_has_422": "422" in schema["paths"]["/prebuilts/custom"]["post"]["responses"],
        "registry_models_has_200": "200" in schema["paths"]["/registry/models"]["get"]["responses"],
    }


def test_openapi_signature_matches_snapshot():
    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    actual = _build_signature(schema)

    snapshot_path = Path("tests/fixtures/openapi_signature.json")
    expected = json.loads(snapshot_path.read_text(encoding="utf-8"))

    assert actual == expected
