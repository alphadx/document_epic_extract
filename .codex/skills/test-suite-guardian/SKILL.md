---
name: test-suite-guardian
description: Orquestar ejecución eficiente de pruebas unitarias e integración para detectar regresiones rápido. Usar cuando haya cambios en adapters, API routers/services, contratos OpenAPI, o comportamiento de workers locales.
---

# test-suite-guardian

## Estrategia de ejecución

1. Ejecutar primero pruebas unitarias de la zona tocada (`tests/unit/`).
2. Ejecutar integración selectiva por dominio:
   - extracción/ocr: `tests/integration/test_extract_*.py`
   - contrato/openapi: `tests/integration/test_openapi_*.py`
   - operación: `tests/integration/test_ops_*.py`
3. Si hay cambios transversales, ejecutar suite completa.
4. Reportar siempre:
   - comando exacto
   - resultado (pass/fail)
   - regresiones detectadas y archivo de test asociado

## Lecciones operativas incorporadas

- Proteger contexto y tiempo: evitar correr toda la suite sin hipótesis previa.
- Automatizar lo repetitivo: fijar comandos de smoke/regresión reutilizables.
- Paralelizar pruebas en ramas/worktrees solo para áreas no dependientes entre sí.

## Reglas

- Nunca eliminar tests para “hacer pasar” el pipeline.
- Si se corrige bug, acompañar con test que falle antes y pase después.
- Mantener fixtures y snapshots versionados y legibles.

## Hooks relacionados y uso

- Hook sugerido: pre-commit para smoke tests de la zona tocada y pre-push para integración selectiva.
- Estado de uso en esta skill: **propuestos**, **no instrumentados aún** en configuración local.

