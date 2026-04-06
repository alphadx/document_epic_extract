.PHONY: test lint openapi-signature cb-consistency release-readiness package-check publish-testpypi-preflight publish-testpypi r701-observe r701-final-cut r701-sync-snapshot

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


R701_ARGS ?=
R701_CUT_DATE ?= 2026-04-12
R701_WINDOW_START ?= 2026-04-06
R701_WINDOW_END ?= 2026-04-12

r701-observe:
	R701_WINDOW_START=$(R701_WINDOW_START) R701_WINDOW_END=$(R701_WINDOW_END) bash scripts/r701_observation_run.sh --append $(R701_ARGS)

r701-sync-snapshot:
	python scripts/r701_sync_snapshot.py --snapshot-date $(R701_CUT_DATE) --window-start $(R701_WINDOW_START) --window-end $(R701_WINDOW_END)

r701-final-cut:
	python scripts/r701_final_cut.py --today $(R701_CUT_DATE) --window-start $(R701_WINDOW_START) --window-end $(R701_WINDOW_END)
