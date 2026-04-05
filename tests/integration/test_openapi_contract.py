"""Integration tests for OpenAPI contract stability."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


def test_openapi_extract_contract_has_standardized_response():
    client = TestClient(app)
    schema = client.get("/openapi.json").json()

    extract_post = schema["paths"]["/extract"]["post"]
    response_200 = extract_post["responses"]["200"]["content"]["application/json"]["schema"]
    assert response_200["$ref"].endswith("/StandardizedExtraction")


def test_openapi_custom_prebuilt_contract_has_typed_models():
    client = TestClient(app)
    schema = client.get("/openapi.json").json()

    post_custom = schema["paths"]["/prebuilts/custom"]["post"]
    request_schema = post_custom["requestBody"]["content"]["application/json"]["schema"]
    response_schema = post_custom["responses"]["200"]["content"]["application/json"]["schema"]

    assert request_schema["$ref"].endswith("/CustomPrebuiltRequest")
    assert response_schema["$ref"].endswith("/CustomPrebuiltResponse")


def test_openapi_custom_prebuilt_includes_validation_error_response():
    client = TestClient(app)
    schema = client.get("/openapi.json").json()

    post_custom = schema["paths"]["/prebuilts/custom"]["post"]
    assert "422" in post_custom["responses"]


def test_openapi_prebuilts_list_has_metadata_schema():
    client = TestClient(app)
    schema = client.get("/openapi.json").json()

    list_prebuilts = schema["paths"]["/prebuilts"]["get"]
    response_schema = list_prebuilts["responses"]["200"]["content"]["application/json"]["schema"]

    assert response_schema["type"] == "array"
    assert response_schema["items"]["$ref"].endswith("/PrebuiltMetadata")


def test_openapi_registry_models_endpoint_present():
    client = TestClient(app)
    schema = client.get("/openapi.json").json()

    registry_get = schema["paths"]["/registry/models"]["get"]
    assert "200" in registry_get["responses"]
    assert "application/json" in registry_get["responses"]["200"]["content"]
