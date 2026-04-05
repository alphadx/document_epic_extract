.PHONY: test lint openapi-signature

lint:
	ruff check .

test:
	pytest -q

openapi-signature:
	python scripts/generate_openapi_signature.py
