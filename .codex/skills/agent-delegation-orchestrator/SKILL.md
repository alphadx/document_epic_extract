---
name: agent-delegation-orchestrator
description: Orquestar delegación por subagentes para planificar, implementar y revisar cambios en este repositorio. Usar cuando la tarea sea compleja, atraviese múltiples capas (api/adapters/tests/docs), o requiera paralelización controlada.
---

# agent-delegation-orchestrator

## Principio clave

Los agentes son el mecanismo principal para escalar calidad y velocidad: dividir una tarea grande en subproblemas con alcance y herramientas acotadas.

## Roles recomendados

1. **planner**: define plan incremental, riesgos y criterios de salida.
2. **implementer**: aplica cambios mínimos por fase.
3. **reviewer**: valida calidad, contratos y regresiones.
4. **release-checker**: confirma readiness y evidencia.
5. **doc-updater**: sincroniza `README.md`, `docs/` y `TODO.md`.

## Estrategia de delegación

- Delegar por dominio (docs, extracción, contratos, testing, release), no por archivo aislado.
- Permitir paralelismo solo entre dominios sin dependencia directa.
- Exigir entregables concretos por agente: diff, tests ejecutados y riesgos abiertos.

## Guardrails

- Cada agente debe tocar el menor número de archivos posible.
- Toda delegación debe terminar con verificación reproducible (comando + resultado).
- Si hay incertidumbre, volver a planner antes de escalar cambios.

## Integración con otras skills

- `agent-workflow-hygiene`: reglas globales de operación.
- `hooks-automation-guardrails`: automatización de checks repetitivos.
- `mcp-context-governance`: activación mínima de MCPs según tarea.
