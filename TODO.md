# TODO del Proyecto (Consolidado)

Backlog único consolidado desde `plan.md`, checklists de hitos y decisiones operativas.

## Prioridad alta

> Ver estado por hito en `docs/hitos_avances.md`.

- [x] **Aprobación explícita de cierre de Hito 7** en roadmap (pasar de “cierre propuesto” a “cerrado”).
  - Referencias: `docs/hito7_cierre.md`, `docs/milestone_decisions.md`.
- [x] **Decisión final de distribución** (no publicar / TestPyPI / PyPI) con owner y fecha.
  - Referencia: `docs/hito7_distribution_decision.md`.
- [x] **Abrir siguiente ciclo de estabilización** si permanecen riesgos medios/altos.
  - Referencias: `docs/release_checklist.md`, `docs/hito7_risk_register.md`, `docs/hitos_avances.md`, `docs/milestone_decisions.md`.

## Prioridad media

- [ ] **Implementar `FlanT5Adapter` (mini/base)** y cerrar hardening de colas asíncronas del worker local.
  - Referencia: tarea pendiente en Fase 4 de `plan.md`.
- [ ] **Cerrar integración SDK cloud real** (credenciales/timeout/proveedor caído) para AWS/GCP/Azure con evidencia de pruebas.
  - Referencia: pendiente explícito en `docs/hito2_cierre_operativo.md`.
- [ ] **Definir política operativa de circuit breaker distribuido** para despliegues multi-réplica.
  - Referencia: riesgo pendiente en `docs/milestone_decisions.md` (Hito 3).

## Prioridad baja

- [x] **Ejecutar decisión de publicación en PyPI/TestPyPI según acta vigente**.
  - Resolución 2026-04-05: **No publicar aún** (diferimiento controlado); no se ejecuta upload hasta nueva aprobación.
  - Owner: Release Manager (Equipo Core OmniExtract). Fecha de reevaluación: 2026-04-19.
  - Referencias: `docs/hito7_distribution_decision.md`, `docs/hito7_cierre.md`, Fase 6 de `plan.md` (opcional).
- [x] **Revisión editorial trimestral de documentación** para mantener sincronía entre README, `docs/`, y `plan.md`.
  - Owner: Equipo Core OmniExtract (mantención documental). Fecha de ejecución: 2026-04-05.
  - Evidencia: `docs/editorial_review_2026q2.md`.

## Tareas de documentación (este cambio)

- [x] Reorientar `README.md` a presentación de producto y enlaces.
- [x] Mover guía de inicio y operación a `docs/getting_started.md`.
- [x] Crear índice documental en `docs/README.md`.
- [x] Crear skill de documentación para estandarizar mantenimiento documental.

## Criterio de “Done” para este TODO

Se considera al día cuando no existan ítems abiertos de prioridad alta y cada ítem tenga owner, fecha objetivo y evidencia enlazada en PR/documento.
