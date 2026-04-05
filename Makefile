.PHONY: test lint openapi-signature release-readiness

lint:
	ruff check .

test:
	pytest -q

openapi-signature:
	python scripts/generate_openapi_signature.py

release-readiness:
	ruff check .
	pytest -q
	python scripts/generate_openapi_signature.py
	git diff --exit-code tests/fixtures/openapi_signature.json
