# TODO del Proyecto (Consolidado)

Backlog único consolidado desde `plan.md`, checklists de hitos y decisiones operativas.

> Última actualización: 2026-04-05.

## Prioridad alta

> Ver estado por hito en `docs/hitos_avances.md`.

- [x] **Aprobación explícita de cierre de Hito 7** en roadmap (pasar de “cierre propuesto” a “cerrado”).
  - Referencias: `docs/hito7_cierre.md`, `docs/milestone_decisions.md`.
- [x] **Decisión final de distribución** (no publicar / TestPyPI / PyPI) con owner y fecha.
  - Referencia: `docs/hito7_distribution_decision.md`.
- [x] **Abrir siguiente ciclo de estabilización** si permanecen riesgos medios/altos.
  - Referencias: `docs/release_checklist.md`, `docs/hito7_risk_register.md`, `docs/hitos_avances.md`, `docs/milestone_decisions.md`.

## Prioridad media

> Plan de ejecución por etapas: `docs/plan_trabajo_prioridad_media.md` (creado el 2026-04-05).

> Avance actual: ítems de prioridad media cerrados con evidencia documental y pruebas asociadas.

- [x] **Implementar `FlanT5Adapter` (mini/base)** y cerrar hardening de colas asíncronas del worker local.
  - Resolución 2026-04-05: implementado adapter dedicado + worker endurecido (colas/concurrencia/timeout).
  - Owner: Equipo Core OmniExtract (API/Plataforma).
  - Evidencia: `docs/hito4_flan_colas_cierre_2026-04-05.md`.
  - Referencia: tarea pendiente en Fase 4 de `plan.md`.
- [x] **Cerrar integración SDK cloud real** (credenciales/timeout/proveedor caído) para AWS/GCP/Azure con evidencia de pruebas.
  - Resolución 2026-04-05: cierre operativo/documental consolidado con matriz de fallas + corrida controlada + plantilla live.
  - Owner: Equipo Core OmniExtract (API/Plataforma).
  - Evidencia: `docs/hito2_cierre_final_2026-04-05.md`, `docs/ocr_live_evidence_2026-04-05.md`, `docs/ocr_live_run_controlled_2026-04-05.md`.
  - Referencia: `docs/hito2_cierre_operativo.md`.
- [x] **Definir política operativa de circuit breaker distribuido** para despliegues multi-réplica.
  - Resolución 2026-04-05: política base aprobada para implementación incremental.
  - Owner: Equipo Core OmniExtract (API/Plataforma).
  - Evidencia: `docs/circuit_breaker_distribuido.md`.
  - Referencia: riesgo pendiente en `docs/milestone_decisions.md` (Hito 3).

## Prioridad baja

- [x] **Ejecutar decisión de publicación en PyPI/TestPyPI según acta vigente**.
  - Resolución 2026-04-05: **No publicar aún** (diferimiento controlado); no se ejecuta upload hasta nueva aprobación.
  - Owner: Release Manager (Equipo Core OmniExtract). Fecha de reevaluación: 2026-04-19.
  - Referencias: `docs/hito7_distribution_decision.md`, `docs/hito7_cierre.md`, Fase 6 de `plan.md` (opcional).
- [x] **Revisión editorial trimestral de documentación** para mantener sincronía entre README, `docs/`, y `plan.md`.
  - Owner: Equipo Core OmniExtract (mantención documental). Fecha de ejecución: 2026-04-05.
  - Evidencia: `docs/editorial_review_2026q2.md`.

## Deuda técnica abierta (pendiente real)

> Esta sección debe mantenerse con ítems **abiertos** y evidencia de cierre; evita “falsos verdes”.

- [ ] **Cerrar riesgo R7-01 de no-regresión contractual en consumo real.**
  - Estado: `Abierto` en registro de riesgos post-release.
  - Owner: Equipo Core OmniExtract (API/Plataforma).
  - Fecha objetivo: 2026-04-12 (cierre de ventana de observación).
  - Evidencia esperada: corrida release-readiness periódica + reporte de consumo real sin drift.
  - Referencia: `docs/hito7_risk_register.md`.
- [ ] **Reevaluar decisión de publicación (No publicar aún) y ejecutar resolución documentada.**
  - Estado: diferimiento vigente; requiere nueva decisión explícita.
  - Owner: Release Manager (Equipo Core OmniExtract).
  - Fecha objetivo: 2026-04-19.
  - Evidencia esperada: acta actualizada + ejecución `make publish-testpypi-preflight` (y publish solo si aplica).
  - Referencia: `docs/hito7_distribution_decision.md`.

## Cierres recientes (fuera de deuda abierta)

- [x] **Circuit breaker distribuido multi-réplica (Redis + atomicidad + métricas).**
  - Cierre ejecutado el 2026-04-05.
  - Evidencia consolidada: `docs/circuit_breaker_distribuido.md`, `docs/circuit_breaker_hito1_2026-04-05.md`, `docs/circuit_breaker_hito2_2026-04-05.md`, `docs/circuit_breaker_hito3_2026-04-05.md`, `docs/circuit_breaker_hito4_cierre_2026-04-05.md`.

## Tareas de documentación (este cambio)

- [x] Reorientar `README.md` a presentación de producto y enlaces.
- [x] Incorporar TL;DR y modos “comenzar rápido” / “comenzar lento (controlado)”.
- [x] Declarar de forma explícita la deuda técnica abierta en README y TODO.

## Criterio de “Done” para este TODO

Se considera al día cuando no existan ítems abiertos de prioridad alta, cada ítem tenga owner/fecha/evidencia, y la sección **Deuda técnica abierta** tenga sólo trabajo pendiente real o quede vacía con evidencia de cierre.
