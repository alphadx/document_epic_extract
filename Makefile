.PHONY: test lint openapi-signature cb-consistency release-readiness package-check publish-testpypi-preflight publish-testpypi

lint:
	ruff check .

test:
	pytest -q

openapi-signature:
	python scripts/generate_openapi_signature.py

cb-consistency:
	python scripts/check_circuit_breaker_consistency.py

release-readiness:
	ruff check .
	pytest -q
	python scripts/check_circuit_breaker_consistency.py
	python scripts/generate_openapi_signature.py
	git diff --exit-code tests/fixtures/openapi_signature.json

package-check:
	python -m pip install -q build twine
	python -m build
	twine check dist/*

publish-testpypi-preflight:
	bash scripts/testpypi_publish_gate.sh

publish-testpypi:
	bash scripts/testpypi_publish_gate.sh --execute
