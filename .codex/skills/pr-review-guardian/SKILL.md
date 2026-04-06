---
name: pr-review-guardian
description: Revisar pull requests con enfoque en regresiones, contratos y riesgos de mantenimiento. Usar antes de merge cuando haya cambios en api/, adapters/, tests/ o docs/ operativos.
---

# pr-review-guardian

## Checklist de revisión

1. Verificar alcance real del diff y detectar cambios colaterales.
2. Confirmar que todo bugfix trae test de regresión.
3. Validar que cambios en `api/schemas/` o rutas tengan cobertura de contrato.
4. Revisar consistencia entre código y documentación (`docs/`, `README.md`).
5. Clasificar riesgos abiertos (bloqueante / no bloqueante).

## Entregables mínimos

- Resumen de hallazgos por severidad.
- Lista de archivos críticos revisados.
- Recomendación final: `approve`, `request-changes` o `follow-up`.
