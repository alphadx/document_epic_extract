---
name: release-readiness-operator
description: Preparar y validar releases del proyecto de extracción documental. Usar para checklist de release, validación de empaquetado, verificación de scripts operativos y documentación de evidencia de salida a producción.
---

# release-readiness-operator

## Flujo recomendado

1. Ejecutar checks base del repositorio (`Makefile`, `pytest`, `ruff`, scripts de `scripts/`).
2. Correr verificaciones de release:
   - `scripts/release_readiness.sh`
   - `scripts/testpypi_publish_gate.sh`
3. Verificar documentación de release y checklist en `docs/`:
   - `docs/release_checklist.md`
   - notas de release (`docs/release_*.md`)
4. Confirmar versionado y consistencia contractual (OpenAPI/signature snapshots).
5. Registrar resultados con fecha explícita en un documento de evidencia dentro de `docs/`.

## Lecciones operativas incorporadas

- Evitar sobreconfiguración del proceso de salida: checklist corto, gates claros, evidencia mínima suficiente.
- Automatizar tareas repetitivas de release mediante scripts existentes en `scripts/`.
- Aplicar validación incremental (primero checks críticos, luego ampliaciones no bloqueantes).

## Criterios de salida

- Todos los checks críticos pasan o tienen excepción documentada.
- Cambios de contrato y compatibilidad quedan registrados.
- Riesgos abiertos se listan con mitigación y responsable.

## Hooks relacionados y uso

- Hook sugerido: pre-push para ejecutar validaciones de contrato/OpenAPI cuando se modifiquen `api/` y pruebas de contrato.
- Estado de uso en esta skill: **propuestos**, **no instrumentados aún** en configuración local.

