---
name: hooks-automation-guardrails
description: Definir hooks ligeros para automatizar validaciones repetitivas y proteger calidad en este repositorio. Usar cuando se quiera ejecutar checks automáticos antes o después de editar archivos, correr tests o preparar commits.
---

# hooks-automation-guardrails

## Cuándo sí usar hooks

- Cuando una validación se repite en casi cada cambio (formato, lint, chequeos de contratos).
- Cuando se quiere prevenir errores frecuentes antes de commit/push.
- Cuando el costo de automatizar es menor que revisar manualmente cada vez.

## Cuándo no usar hooks

- Si el hook tarda demasiado y bloquea el flujo normal.
- Si depende de red o recursos inestables para cada ejecución local.
- Si duplica exactamente una validación ya ejecutada en CI sin aportar feedback temprano.

## Hooks recomendados para este repo

1. **Post-edición Python**: correr check rápido de estilo en archivos tocados.
2. **Pre-commit**: validación mínima de tests unitarios focalizados por módulo afectado.
3. **Pre-push**: validar contratos OpenAPI/snapshots cuando se toquen `api/`, `api/schemas/` o `tests/integration/test_openapi_*`.
4. **Stop hook**: recordar actualizar `docs/` cuando cambien contratos públicos o flujos de release.

## Política de diseño

- Mantener hooks pequeños, deterministas y opcionalmente desactivables por contexto.
- Priorizar feedback inmediato (segundos, no minutos).
- Versionar reglas y racional de cada hook dentro de la skill para evitar drift.

## Estado de uso de hooks

- Hooks incluidos en esta skill: **Post-edición Python**, **Pre-commit**, **Pre-push**, **Stop hook**.
- Uso efectivo en este repositorio (al momento): **documentados y recomendados**, **sin evidencia de activación automática versionada**.

