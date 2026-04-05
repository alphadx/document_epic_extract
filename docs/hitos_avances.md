# Avances de Hitos (Estado consolidado)

Última actualización: **2026-04-05**.

Este documento consolida el estado real de avance por hito con foco en: **logros**, **evidencia**, **pendientes** y **siguiente paso**. Complementa (no reemplaza) a `docs/milestone_decisions.md`.

## Resumen ejecutivo

| Hito | Estado | Avance | Evidencia principal | Pendiente clave |
|---|---|---:|---|---|
| Hito 0 — Kickoff | Cerrado | 100% | `LICENSE`, `README.md`, `CONTRIBUTING.md`, `plan.md` | Ninguno |
| Hito 1 — Fundación/Core | Cerrado | 100% | CI + contrato base + `/extract` | Ninguno |
| Hito 2 — OCR cloud | En progreso | 85% | Adaptadores + tests + modo mock + intento SDK real | Matriz completa SDK real con credenciales/timeout/proveedor caído |
| Hito 3 — LiteLLM + Prebuilt | Cerrado | 100% | Adapter LiteLLM + contrato OpenAPI + CI contract checks | Circuit breaker distribuido (mejora posterior) |
| Hito 4 — Ejecución local | Cerrado (operativo) | 90% | `SmolVLM2Adapter` + contrato worker + e2e local | `FlanT5Adapter` mini/base + hardening de colas |
| Hito 5 — Demo frontend | Cerrado (operativo) | 100% | Manejo de errores + sesión + pruebas demo | Mejoras UX no bloqueantes |
| Hito 6 — Docs/OSS | Cerrado (operativo) | 95% | Guías operativas + checklist release + versionado contrato | Publicación PyPI (opcional, dependiente de decisión) |
| Hito 7 — Post-release | Cerrado (aprobado) | 100% | Riesgos + decisión distribución + validación paquete + acta aprobada | Ninguno (seguir ciclo de pendientes transversales) |

---

## Hito 0 — Kickoff, base de repositorio

**Estado:** Cerrado.

### Avances confirmados
- Licencia OSS y base editorial publicadas.
- Arquitectura/roadmap base y guía de contribución disponibles.
- Baseline de seguridad inicial documentada.

### Evidencia
- `plan.md` (fases + seguridad base).
- `CONTRIBUTING.md`.

---

## Hito 1 — Fundación y Core

**Estado:** Cerrado.

### Avances confirmados
- API core funcional con `POST /extract`.
- Contrato estandarizado de salida definido en schemas.
- CI mínimo con lint + tests.

### Evidencia
- `docs/milestone_decisions.md` (Hito 1).
- Workflows CI en `.github/workflows`.

---

## Hito 2 — Adaptadores OCR cloud

**Estado:** En progreso (muy avanzado).

### Avances confirmados
- Adaptadores AWS/Azure/GCP operativos con normalización de contrato.
- Cobertura de pruebas unitarias e integración del endpoint en modo mock.
- Modo SDK real habilitado cuando no se inyecta `mock_response_json`.

### Evidencia
- `docs/hito2_cierre_operativo.md`.
- `docs/milestone_decisions.md` (sección Hito 2).

### Pendientes de cierre
- Validación completa en runtime real por proveedor con matriz explícita:
  - credenciales inválidas,
  - timeout/retry,
  - proveedor no disponible,
  - mensajes de error homogéneos hacia API.

### Siguiente paso operativo
- Ejecutar batería controlada por proveedor y adjuntar evidencia en doc de hito + PR.

---

## Hito 3 — Meta-gateway LLM + LiteLLM + Prebuilt

**Estado:** Cerrado.

### Avances confirmados
- Integración LiteLLM y adapter multimotor.
- Hardening de parseo y resiliencia.
- Gobernanza contractual con snapshot y checks dedicados.

### Evidencia
- `docs/hito3_checklist.md`.
- `docs/hito3_final_audit.md`.
- `docs/milestone_decisions.md` (Hito 3).

### Riesgo residual (no bloqueante)
- Circuit breaker distribuido en despliegues multi-réplica.

---

## Hito 4 — Ejecución local

**Estado:** Cerrado (operativo).

### Avances confirmados
- Flujo `provider=local` de punta a punta validado.
- Contrato API↔worker documentado y estable.
- Operación CPU/GPU documentada para worker local.

### Evidencia
- `docs/hito4_checklist.md`.
- `docs/local_worker_contract.md`.
- `docs/milestone_decisions.md` (Hito 4).

### Pendiente de evolución
- Implementar `FlanT5Adapter` mini/base y hardening de colas asíncronas.

---

## Hito 5 — Demo Front-end

**Estado:** Cerrado (operativo).

### Avances confirmados
- Demo robustecido con errores accionables y persistencia de sesión.
- Fallback para previews y pruebas unitarias de helpers críticos.

### Evidencia
- `docs/hito5_checklist.md`.
- `docs/demo_troubleshooting.md`.
- `docs/milestone_decisions.md` (Hito 5).

---

## Hito 6 — Documentación y OSS

**Estado:** Cerrado (operativo).

### Avances confirmados
- Publicadas guías de operación, contribución y release.
- Política de versionado del contrato definida.

### Evidencia
- `docs/hito6_checklist.md`.
- `docs/release_checklist.md`.
- `docs/contract_versioning.md`.

### Pendiente condicionado
- Publicación en PyPI sólo si la decisión de distribución cambia a publicar.

---

## Hito 7 — Post-release, distribución y cierre

**Estado:** Cerrado (aprobado).

### Avances confirmados
- Riesgos post-release registrados y gestionados.
- Decisión de distribución documentada.
- Build/check de artefactos ejecutados con evidencia.

### Evidencia
- `docs/hito7_checklist.md`.
- `docs/hito7_risk_register.md`.
- `docs/hito7_distribution_decision.md`.
- `docs/hito7_packaging_validation.md`.
- `docs/hito7_cierre.md`.

### Cierre de gobernanza
- Aprobación explícita del cierre confirmada por responsable del roadmap en fecha 2026-04-05.

---

## Acciones inmediatas recomendadas (cross-hito)

1. Cerrar brecha técnica de Hito 2 con matriz SDK real certificada.
2. Planificar evolución local de Hito 4 (`FlanT5Adapter` + colas) como próximo bloque técnico.
3. Definir política operativa de circuit breaker distribuido para despliegues multi-réplica.
