# AGENTS.md

## Estándar de trabajo asistido en este repositorio

Usar esta estructura como fuente canónica durante programación asistida:

- Skills: `.codex/skills/*/SKILL.md`
- Agentes: `.codex/agents/*.md`
- Hooks (plantilla): `.codex/hooks/hooks.example.json`
- MCP (plantilla): `.codex/mcp.example.json`

## Reglas operativas

1. Antes de implementar cambios complejos, usar `agent-delegation-orchestrator` y `agent-workflow-hygiene`.
2. Para calidad de código, combinar `tdd-workflow`, `test-suite-guardian` y `pr-review-guardian`.
3. Para estabilidad operativa, usar `build-error-resolver`, `release-readiness-operator` y `contract-drift-auditor`.
4. Para seguridad y gobierno, usar `security-reviewer-lite`, `hooks-automation-guardrails` y `mcp-context-governance`.

## Agentes recomendados

- `planner.md`: planificación incremental.
- `implementer.md`: cambios mínimos por fase.
- `reviewer.md`: revisión de calidad/contrato.
- `release-checker.md`: verificación de salida.
- `doc-updater.md`: sincronización documental.

## Nota

Las plantillas de Hooks y MCP son guías de configuración; deben adaptarse al entorno real antes de activarse.
