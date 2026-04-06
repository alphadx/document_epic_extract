---
name: tdd-workflow
description: Aplicar flujo TDD para cambios funcionales en extracción, ruteo y contratos. Usar cuando se implemente feature nueva o bugfix con impacto en comportamiento observable.
---

# tdd-workflow

## Ciclo recomendado

1. Escribir test que falle (unitario o integración focalizada).
2. Implementar cambio mínimo para pasar el test.
3. Refactorizar sin romper cobertura.
4. Ejecutar subset relevante y luego suite ampliada si aplica.

## Mapeo rápido por área

- Parsing/LLM: `tests/unit/test_llm_parsing.py`
- OCR adapters: `tests/unit/test_ocr_adapters.py`
- Contrato API: `tests/integration/test_openapi_*.py`
- Extract flow: `tests/integration/test_extract_*.py`
