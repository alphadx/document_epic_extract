"""Generate compact OpenAPI signature snapshot used by contract tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

OUT_PATH = Path("tests/fixtures/openapi_signature.json")


def build_signature(schema: dict) -> dict:
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


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from api.main import app

    schema = TestClient(app).get("/openapi.json").json()
    signature = build_signature(schema)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(signature, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
