# Skill: documentation-maintainer

## Objetivo
Mantener la documentación del repositorio clara, navegable y sincronizada con el estado real del producto.

## Cuándo usar esta skill
- Cuando se pida reorganizar documentación.
- Cuando `README.md` esté demasiado técnico y deba enfocarse en producto.
- Cuando falte consolidar pendientes en un backlog documental (`TODO.md`).

## Principios
1. `README.md` raíz = presentación del producto + valor + enlaces clave.
2. `docs/` = operación técnica, guías, troubleshooting, evidencia de hitos/releases.
3. `TODO.md` = backlog consolidado de tareas abiertas (proyecto + plan).
4. Mantener trazabilidad: toda tarea pendiente debe referenciar su fuente (`plan.md`, checklist o acta).

## Workflow recomendado
1. Revisar `README.md`, `plan.md`, `docs/` y detectar redundancias.
2. Mover contenido operativo a `docs/getting_started.md` y otras guías especializadas.
3. Crear/actualizar `docs/README.md` como índice por categorías.
4. Consolidar pendientes en `TODO.md` con prioridad (alta/media/baja).
5. Verificar enlaces internos Markdown.
6. Ejecutar checks mínimos (`ruff check .`, `pytest -q` cuando aplique).

## Plantilla mínima para TODO
- Prioridad alta: bloqueantes de release/roadmap.
- Prioridad media: deuda técnica funcional.
- Prioridad baja: mejoras no bloqueantes.
- Cada tarea con referencia documental de origen.

## DoD documental
- README breve y orientado a producto.
- `docs/README.md` existe y organiza contenido.
- `docs/getting_started.md` cubre arranque reproducible.
- `TODO.md` refleja pendientes reales del plan y hitos.
