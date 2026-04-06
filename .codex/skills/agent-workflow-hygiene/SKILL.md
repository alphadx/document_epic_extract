---
name: agent-workflow-hygiene
description: Aplicar buenas prácticas de operación de agentes en tareas de desarrollo de este repositorio. Usar cuando se requiera optimizar contexto, decidir paralelización por worktrees, automatizar tareas repetitivas y evitar sobreconfiguración.
---

# agent-workflow-hygiene

## Principios operativos

1. No sobrecomplicar: priorizar reglas simples y cambios pequeños con impacto medible.
2. Proteger contexto: cargar solo archivos necesarios, evitar exploración masiva sin objetivo.
3. Paralelizar con control: usar `git worktree` solo para tareas no solapadas.
4. Automatizar repetitivo: estandarizar comandos de lint/test/docs en scripts reutilizables.
5. Delegar por alcance: separar planificación, implementación y revisión en pasos explícitos.

## Checklist antes de ejecutar cambios grandes

- ¿Existe plan incremental con fases mergeables?
- ¿Se definieron pruebas mínimas por fase?
- ¿Se limitaron los archivos a tocar por cada fase?
- ¿Hay criterio de rollback o reversión?

## Prácticas para este repo

- Usar `rg --files` y tests focalizados antes de correr la suite completa.
- Mantener skills breves y con rutas concretas a `docs/`, `tests/`, `scripts/`, `api/`, `adapters/`.
- Evitar skills monolíticas: dividir por dominio (docs, debug, release, testing).
- Para automatizaciones recurrentes, aplicar `hooks-automation-guardrails` en lugar de checks manuales repetidos.

## Hooks relacionados y uso

- Hook recomendado: delegar validaciones repetitivas a `hooks-automation-guardrails`.
- Estado de uso en esta skill: **definidos como guía**, **no ejecutados automáticamente** desde este documento.

## MCP relacionados y uso

- MCP recomendado: aplicar `mcp-context-governance` para decidir activación mínima por tarea.
- Estado de uso en esta skill: **definidos como guía**, **no configurados automáticamente** desde este documento.

## Agentes relacionados y uso

- Agente recomendado: aplicar `agent-delegation-orchestrator` cuando la tarea cruce múltiples dominios.
- Estado de uso en esta skill: **definidos como guía**, **sin runtime de subagentes versionado aquí**.

