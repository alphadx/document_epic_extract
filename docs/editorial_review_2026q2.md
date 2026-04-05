# Revisión editorial trimestral — 2026 Q2

Fecha de ejecución: **2026-04-05**  
Responsable: **Equipo Core OmniExtract (mantención documental)**

## Objetivo

Validar sincronía documental entre `README.md`, `docs/`, `plan.md` y `TODO.md` para cerrar el pendiente de prioridad baja definido en backlog consolidado.

## Alcance revisado

- `README.md`
- `plan.md`
- `TODO.md`
- `docs/hitos_avances.md`
- `docs/milestone_decisions.md`
- `docs/hito7_distribution_decision.md`
- `docs/hito7_cierre.md`
- `docs/README.md`

## Hallazgos y ajustes aplicados

1. **Estado de Hito 7 desactualizado en README**
   - Hallazgo: se reportaba “cierre propuesto”.
   - Acción: actualización a “cerrado (aprobado)” con fecha `2026-04-05`.

2. **Narrativa de distribución no homogénea**
   - Hallazgo: README no explicitaba diferimiento operativo ni fecha de reevaluación.
   - Acción: se agregó estado “No publicar aún” y reevaluación `2026-04-19`.

3. **Referencia de cierre en roadmap (`plan.md`)**
   - Hallazgo: texto indicaba cierre “propuesto”.
   - Acción: texto normalizado a cierre “aprobado”.

4. **Backlog de prioridad baja (`TODO.md`)**
   - Hallazgo: ítem de publicación PyPI figuraba abierto pese a decisión formal de diferimiento.
   - Acción: ítem actualizado a resuelto por decisión ejecutada (no upload) y trazabilidad documental.

5. **Checklists/roadmap con semántica ambigua sobre publicación opcional**
   - Hallazgo: `plan.md` y `docs/release_checklist.md` mantenían checkbox abierto de “Publicar” pese a decisión formal de diferimiento.
   - Acción: se normalizó a estado evaluado/cerrado como **N/A en v0.1.1** por decisión `No publicar aún` (con reevaluación definida).

## Resultado de la revisión

- **Consistencia global:** alineada para estado de Hito 7 y estrategia de distribución.
- **Pendientes técnicos vigentes (fuera de esta revisión editorial):**
  - Integración SDK cloud real (Hito 2).
  - `FlanT5Adapter` + hardening de colas (Hito 4).
  - Política operativa de circuit breaker distribuido (Hito 3, mejora cross-hito).

## Próxima revisión sugerida

- Ventana objetivo: **2026-07-05** (Q3), o antes si cambia la decisión de publicación.
