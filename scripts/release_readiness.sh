#!/usr/bin/env bash
set -euo pipefail

echo "[release-readiness] Running lint..."
ruff check .

echo "[release-readiness] Running tests..."
pytest -q

echo "[release-readiness] Refreshing OpenAPI signature..."
python scripts/generate_openapi_signature.py

echo "[release-readiness] Verifying OpenAPI signature snapshot is up to date..."
git diff --exit-code tests/fixtures/openapi_signature.json

echo "[release-readiness] OK"
