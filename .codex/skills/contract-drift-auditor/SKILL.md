---
name: contract-drift-auditor
description: Detectar y corregir drift entre contratos OpenAPI, esquemas y comportamiento real de endpoints. Usar cuando cambien `api/`, `api/schemas/`, snapshots o documentación contractual.
---

# contract-drift-auditor

## Flujo

1. Identificar cambios en `api/routers/`, `api/schemas/` y tests de contrato.
2. Ejecutar pruebas/snapshots de OpenAPI afectados.
3. Comparar cambios con documentación en `docs/openapi.md`.
4. Marcar breaking vs non-breaking y proponer plan de compatibilidad.
5. Dejar evidencia de versión/fecha en documento de release si aplica.

## Entregable

- Reporte de drift con:
  - endpoints impactados,
  - tipo de cambio,
  - riesgo para clientes,
  - acción recomendada.
