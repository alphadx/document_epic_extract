# Documentación de OmniExtract Gateway

Este índice organiza toda la documentación por objetivo. El `README.md` principal presenta el producto; aquí vive la operación, arquitectura y trazabilidad.

## 1) Empezar y operar

- [Getting Started](getting_started.md): instalación, arranque con Docker, ejecución local y primeros requests.
- [OpenAPI y contrato](openapi.md): enfoque de gobernanza y verificación de contrato.
- [Troubleshooting del demo](demo_troubleshooting.md): fallos frecuentes en UI/API.
- [Política operativa de circuit breaker distribuido](circuit_breaker_distribuido.md): diseño, runbook y evidencia de implementación.

## 2) Uso funcional

- [Custom Prebuilts](custom_prebuilts.md): cómo registrar plantillas personalizadas.
- [Agregar modelos al registry](adding_models.md): extensión de `registry/models.yaml`.
- [Versionado de contrato](contract_versioning.md): reglas de cambios API.

## 3) Arquitectura y roadmap

- [Avances consolidados de hitos](hitos_avances.md): estado ejecutivo por hito (logros, pendientes y siguiente paso).
- [Plan maestro del proyecto](../plan.md): arquitectura, fases y decisiones globales.
- [Registro de decisiones por hito](milestone_decisions.md): actas y rationale.
- [TODO consolidado](../TODO.md): backlog pendiente del proyecto y del plan.
- [Acta de cierre Hito 4 — circuit breaker](circuit_breaker_hito4_cierre_2026-04-05.md): evidencia final de transición CLOSED→OPEN→HALF_OPEN→CLOSED.
- [Acta de consistencia documental — circuit breaker](acta_consistencia_circuit_breaker_2026-04-05.md): estado canónico y mapa de fuentes de verdad.
- [Definition of Done — circuit breaker](circuit_breaker_definition_of_done_2026-04-05.md): checklist final de cierre y evidencias.
- [Resumen ejecutivo — circuit breaker](resumen_ejecutivo_circuit_breaker_2026-04-05.md): síntesis de estado, evidencias y gates.
- [Handoff final — circuit breaker](handoff_circuit_breaker_2026-04-05.md): paquete de entrega y comandos de validación.

## 4) Releases y estabilización

- [Checklist de release](release_checklist.md)
- [Plan de estabilización](public_release_stabilization.md)
- [Evidencia RC v0.1.1-rc1](release_rc_0.1.1-rc1.md)
- [Evidencia release estable v0.1.1](release_v0.1.1.md)
- [Revisión editorial trimestral 2026 Q2](editorial_review_2026q2.md)

## 5) Historial de hitos

- [Hito 2 — cierre operativo OCR](hito2_cierre_operativo.md)
- [Hito 3 — checklist](hito3_checklist.md) y [auditoría final](hito3_final_audit.md)
- [Hito 4 — checklist](hito4_checklist.md) y [contrato API↔worker local](local_worker_contract.md)
- [Hito 5 — checklist](hito5_checklist.md)
- [Hito 6 — checklist](hito6_checklist.md)
- [Hito 7 — checklist](hito7_checklist.md), [riesgos](hito7_risk_register.md), [decisión de distribución](hito7_distribution_decision.md), [validación de empaquetado](hito7_packaging_validation.md), [acta de cierre](hito7_cierre.md)

## 6) Regla editorial de documentación

- `README.md` raíz = visión de producto + propuesta de valor + enlaces.
- `docs/` = operación, guías, troubleshooting, decisiones y evidencias.
- `TODO.md` = backlog único y priorizado con estado.
