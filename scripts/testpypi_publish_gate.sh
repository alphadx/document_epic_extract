#!/usr/bin/env bash
set -euo pipefail

MODE="preflight"
if [[ "${1:-}" == "--execute" ]]; then
  MODE="execute"
fi

if [[ "${1:-}" == "--help" ]]; then
  echo "Usage: $0 [--execute]"
  echo "  default: preflight checks only"
  exit 0
fi

if ! ls dist/*.whl dist/*.tar.gz >/dev/null 2>&1; then
  echo "[testpypi-gate] dist/* not found. Running package-check..."
  make package-check
fi

if [[ -n "${TWINE_API_TOKEN:-}" ]]; then
  TWINE_USERNAME="__token__"
  TWINE_PASSWORD="${TWINE_API_TOKEN}"
fi

if [[ -z "${TWINE_USERNAME:-}" || -z "${TWINE_PASSWORD:-}" ]]; then
  echo "[testpypi-gate] Missing credentials."
  echo "Set TWINE_API_TOKEN (recommended) or TWINE_USERNAME/TWINE_PASSWORD."
  exit 1
fi

echo "[testpypi-gate] Artifacts present and credentials detected."

if [[ "$MODE" == "preflight" ]]; then
  echo "[testpypi-gate] Preflight OK (no upload performed)."
  exit 0
fi

echo "[testpypi-gate] Uploading to TestPyPI..."
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
echo "[testpypi-gate] Upload complete."
