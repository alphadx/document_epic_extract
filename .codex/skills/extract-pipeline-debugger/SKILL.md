---
name: extract-pipeline-debugger
description: Diagnosticar fallos en el flujo de extracción documental (OCR + LLM + enrutamiento). Usar cuando fallen tests de extracción, respuestas de `/extract`, integraciones OCR cloud/local, o parsing estructurado.
---

# extract-pipeline-debugger

## Diagnóstico mínimo

1. Reproducir el fallo con tests focalizados:
   - `tests/integration/test_extract_*.py`
   - `tests/unit/test_ocr_adapters.py`
   - `tests/unit/test_llm_parsing.py`
2. Ubicar capa afectada:
   - OCR: `adapters/ocr/`
   - LLM/parsing: `adapters/llm/`
   - Router/servicios API: `api/services/` y `api/routers/`
3. Validar contrato request/response en `api/schemas/`.
4. Confirmar que la selección de modelo/proveedor coincide con `registry/models.yaml` y `api/services/registry_service.py`.

## Lecciones operativas incorporadas

- Aplicar cambios mínimos y medibles por capa antes de tocar múltiples componentes.
- Mantener contexto acotado: abrir solo tests y módulos del flujo afectado.
- Paralelizar solo cuando no hay solapamiento (ej. OCR y parsing en worktrees distintos).

## Guía de resolución

- Preferir fix pequeño y testeable por capa.
- Agregar o ajustar test de regresión junto con el fix.
- Si el bug afecta contratos públicos, sincronizar `docs/openapi.md` y snapshots de contrato.

## Hooks relacionados y uso

- Hook sugerido: post-edición para correr tests focalizados (`tests/unit/test_ocr_adapters.py`, `tests/unit/test_llm_parsing.py`) cuando se toquen `adapters/`.
- Estado de uso en esta skill: **propuestos**, **no instrumentados aún** en configuración local.

