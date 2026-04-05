# Registro de Decisiones por Hito

Este documento deja constancia de **qué decisiones se tomaron en cada hito, por qué se tomaron y cuál fue su impacto**.

> Norma del proyecto (obligatoria): **cada hito nuevo debe actualizar este archivo** antes de darse por cerrado.

> Vista ejecutiva de avance por hito: `docs/hitos_avances.md`.

---

## Propósito

Mantener trazabilidad técnica y de producto para:

- Evitar ambigüedades sobre el alcance real de cada hito.
- Facilitar onboarding de nuevos contribuidores.
- Reducir retrabajo al hacer explícito el porqué de cada decisión.
- Conservar contexto para auditorías técnicas y de seguridad.

---

## Plantilla obligatoria para próximos hitos

Copiar y completar este bloque en cada hito:

```md
## Hito N — <nombre>
Fecha de cierre: YYYY-MM-DD
Estado: Cerrado | Parcial | En progreso

### Decisiones tomadas
1. **Decisión**
   - **Qué se decidió:**
   - **Por qué:**
   - **Alternativas consideradas:**
   - **Impacto / trade-offs:**

2. **Decisión**
   - **Qué se decidió:**
   - **Por qué:**
   - **Alternativas consideradas:**
   - **Impacto / trade-offs:**

### Evidencia de cierre
- PR(s):
- Checks ejecutados:
- Riesgos pendientes:
- Siguiente hito habilitado:
```

---

## Hito 1 — Fundación y Core

Fecha de cierre: 2026-04-04  
Estado: Cerrado

### Decisiones tomadas

1. **Incorporar CI mínimo en GitHub Actions (lint + tests)**
   - **Qué se decidió:** agregar pipeline con `ruff check .` y `pytest -q` en Python 3.11/3.12.
   - **Por qué:** establecer una barrera mínima de calidad para prevenir regresiones tempranas.
   - **Alternativas consideradas:** validación sólo local sin CI.
   - **Impacto / trade-offs:** mayor confiabilidad en PRs a cambio de tiempos de ejecución de CI.

2. **Cerrar formalmente Fase 1 en documentación**
   - **Qué se decidió:** reflejar en `plan.md` y `README.md` el estado de cierre del hito y comandos de verificación.
   - **Por qué:** alinear estado real de implementación con la documentación pública del proyecto.
   - **Alternativas consideradas:** mantener estado “en progreso” hasta Fase 2.
   - **Impacto / trade-offs:** mejora de transparencia; requiere disciplina de actualización documental por hito.

3. **Corregir deuda de lint para dejar baseline limpio**
   - **Qué se decidió:** eliminar imports no usados y ordenar bloques de import en módulos tocados.
   - **Por qué:** evitar ruido en revisiones y asegurar que el quality gate de CI sea estable.
   - **Alternativas consideradas:** postergar limpieza para un PR futuro.
   - **Impacto / trade-offs:** bajo costo de mantenimiento inmediato; reduce fricción en próximos hitos.

### Evidencia de cierre

- PR(s): cierre de Fase 1 + ajustes de documentación de hito.
- Checks ejecutados: `ruff check .`, `pytest -q`.
- Riesgos pendientes: implementación real de adaptadores OCR/LLM/local (Fases 2–4).
- Siguiente hito habilitado: Fase 2 — Adaptadores deterministas.



## Hito 2 — Adaptadores OCR Cloud

Fecha de inicio: 2026-04-04  
Estado: En progreso

### Decisiones tomadas (arranque)

1. **No declarar cierre del hito con stubs**
   - **Qué se decidió:** mantener explícitamente el estado "En progreso" mientras existan `NotImplementedError` en adaptadores OCR.
   - **Por qué:** evita falsos positivos de avance y protege la trazabilidad técnica del roadmap.
   - **Alternativas consideradas:** marcar cierre parcial por estructura base creada.
   - **Impacto / trade-offs:** mayor rigor de cierre; pospone el pase a Fase 3 hasta completar integración real.

2. **Formalizar checklist de cierre operativo del hito**
   - **Qué se decidió:** documentar DoD y secuencia de implementación en `docs/hito2_cierre_operativo.md`.
   - **Por qué:** asegurar ejecución sin cabos sueltos en implementación, pruebas y documentación.
   - **Alternativas consideradas:** gestionar tareas sólo en conversación o issues.
   - **Impacto / trade-offs:** mejora foco y control de avance; exige disciplina para mantener checklist actualizado.


3. **Cubrir endpoint /extract por proveedor OCR en modo mock**
   - **Qué se decidió:** agregar pruebas de integración por proveedor (AWS/Azure/GCP) contra `POST /extract` usando payload mock.
   - **Por qué:** validar el contrato del gateway completo (router + adapter + esquema) y no sólo pruebas unitarias de adapters.
   - **Alternativas consideradas:** mantener sólo pruebas unitarias por adapter.
   - **Impacto / trade-offs:** mayor confianza en comportamiento end-to-end; todavía pendiente validación con SDK cloud real.

### Evidencia de avance

- Documento de cierre operativo creado: `docs/hito2_cierre_operativo.md`.
- Riesgos actuales: falta completar conexión SDK cloud real (hoy se habilitó mapeo funcional basado en payload proveedor/mock).
- Próximo paso inmediato: cerrar integración SDK real por proveedor (credenciales/timeout/proveedor caído) y conservar quality gates en verde.
- Avance documental adicional: README actualizado con variables de entorno OCR cloud y ejemplo de uso en modo mock payload.

## Hito 3 — Meta-Gateway LLM + LiteLLM + Prebuilt Engine

Fecha de cierre: 2026-04-04  
Estado: Cerrado

### Decisiones tomadas

1. **Definir DoD explícito para evitar cierre parcial del hito**
   - **Qué se decidió:** formalizar checklist de cierre en `docs/hito3_checklist.md` con criterios técnicos, pruebas y documentación.
   - **Por qué:** reducir ambigüedad sobre qué significa “terminar Hito 3”.
   - **Alternativas consideradas:** gestionar avances sólo en conversaciones/PRs sin checklist persistente.
   - **Impacto / trade-offs:** mayor claridad y trazabilidad; requiere mantener checklist actualizado en cada avance.

2. **Mantener el hito en progreso hasta completar hardening e integración endpoint**
   - **Qué se decidió:** mantener el estado del hito como “En progreso” hasta cerrar hardening, integración y validaciones de contrato.
   - **Por qué:** evitar deuda técnica y proteger la API pública de regresiones silenciosas.
   - **Alternativas consideradas:** cerrar el hito al completar solo la implementación base del adapter.
   - **Impacto / trade-offs:** cronograma más estricto, pero mejor calidad de salida y menor retrabajo.

3. **Blindar contrato OpenAPI con snapshot + CI dedicado**
   - **Qué se decidió:** versionar firma OpenAPI, agregar tests de contrato y un job de CI específico para contract-checks.
   - **Por qué:** detectar regresiones de contrato API antes de mergear PRs.
   - **Alternativas consideradas:** depender solo de pruebas funcionales sin snapshot de firma.
   - **Impacto / trade-offs:** mayor disciplina en cambios de API; más claridad para consumidores externos.

### Evidencia de cierre

- PR(s): implementación adapter LiteLLM + hardening + contrato OpenAPI (snapshot/tests/CI) + documentación de cierre.
- Checks ejecutados: `ruff check .`, `pytest -q`, `make openapi-signature`, `git diff --exit-code tests/fixtures/openapi_signature.json`.
- Riesgos pendientes: monitoreo en producción de variabilidad por proveedor LLM; circuit breaker distribuido en despliegues multi-réplica.
- Siguiente hito habilitado: Fase 4 — Ejecución Local (SmolVLM2).

### Addendum operativo (2026-04-05)

- **Qué se decidió:** establecer política operativa de circuit breaker distribuido con estado compartido (Redis), transición `closed/open/half_open`, runbook y métricas mínimas.
- **Por qué:** eliminar divergencia de estado entre réplicas y reducir cascadas de fallo en proveedores externos.
- **Evidencia:** `docs/circuit_breaker_distribuido.md`.
- **Estado del riesgo:** mitigación definida a nivel operativo; pendiente implementación completa del store distribuido en runtime.


## Hito 4 — Ejecución Local (SmolVLM2)

Fecha de inicio: 2026-04-05  
Fecha de cierre: 2026-04-05  
Estado: Cerrado (operativo)

### Decisiones tomadas (arranque)

1. **No cerrar Hito 4 hasta tener flujo `provider=local` end-to-end verificable**
   - **Qué se decidió:** exigir implementación funcional del `SmolVLM2Adapter` con pruebas unitarias e integración de `POST /extract`.
   - **Por qué:** evitar cierre documental sin capacidad operativa real del camino local.
   - **Alternativas consideradas:** cerrar “parcial” con stub + documentación.
   - **Impacto / trade-offs:** mayor rigor de cierre; incrementa el trabajo inicial de pruebas y hardening.

2. **Formalizar DoD del hito en checklist dedicado**
   - **Qué se decidió:** crear `docs/hito4_checklist.md` con alcance, criterios de validación y riesgos.
   - **Por qué:** reducir ambigüedad y dejar trazabilidad explícita de pendientes.
   - **Alternativas consideradas:** gestionar el avance sólo en PRs/conversación.
   - **Impacto / trade-offs:** mejor gobernanza del hito; requiere disciplina para mantener el checklist al día.

3. **Priorizar SmolVLM2 antes de FLAN-T5**
   - **Qué se decidió:** abordar primero `SmolVLM2Adapter` para consolidar contrato API ↔ Worker y reutilizar ese patrón para otros modelos locales.
   - **Por qué:** reduce riesgo técnico al validar temprano la integración local más representativa del flujo multimodal.
   - **Alternativas consideradas:** implementar simultáneamente SmolVLM2 + FLAN-T5.
   - **Impacto / trade-offs:** entrega incremental más controlada; FLAN-T5 queda explícitamente en siguiente tramo del hito.

### Evidencia de avance

- Documento de arranque y DoD de Hito 4: `docs/hito4_checklist.md`.
- `SmolVLM2Adapter` implementado con llamada HTTP asíncrona al Worker, validación de contrato y manejo de errores.
- Cobertura de pruebas para `provider=local`: unit tests del adapter + integración de `POST /extract` con mock payload.
- Worker local implementado en `adapters/local/worker_app.py` con contrato estable de `/infer`.
- Contrato final API↔Worker y operación CPU/GPU documentados en `docs/local_worker_contract.md` y `README.md`.
- Validación end-to-end sin mock payload: API local (`/extract`) → Worker real (`/infer`) en tests de integración.
- Checks de calidad en verde: `ruff check .` y `pytest -q`.
- Riesgos post-cierre: tuning de rendimiento en GPU y pruebas de carga para escenario productivo.
- Siguiente hito habilitado: Fase 5 — Demo Front-end.

## Hito 5 — Demo Front-end (Streamlit)

Fecha de inicio: 2026-04-05  
Fecha de cierre: 2026-04-05  
Estado: Cerrado (operativo)

### Decisiones tomadas (arranque)

1. **No declarar cierre del hito con sólo UI feliz (happy path)**
   - **Qué se decidió:** mantener Hito 5 en “En progreso” hasta cubrir errores HTTP accionables, estado de sesión y pruebas mínimas del demo.
   - **Por qué:** un demo sin manejo de fallos reales puede ocultar problemas de integración y generar falsa sensación de cierre.
   - **Alternativas consideradas:** cerrar por disponibilidad visual del flujo base (upload + extract + comparación).
   - **Impacto / trade-offs:** aumenta el trabajo de hardening, pero reduce retrabajo y soporte reactivo.

2. **Formalizar DoD con checklist dedicado para evitar cabos sueltos**
   - **Qué se decidió:** crear `docs/hito5_checklist.md` con alcance obligatorio, riesgos y criterio explícito para pasar al siguiente hito.
   - **Por qué:** conservar trazabilidad de pendientes funcionales/técnicos y alinear expectativas de cierre.
   - **Alternativas consideradas:** gestionar pendientes sólo en conversación o PRs.
   - **Impacto / trade-offs:** mejora gobernanza del hito; requiere mantenimiento continuo de la checklist.

3. **Priorizar robustez de operación antes de expansión visual**
   - **Qué se decidió:** priorizar manejo de errores, persistencia de resultados en sesión y cobertura de pruebas sobre mejoras cosméticas de UI.
   - **Por qué:** la confiabilidad del demo es condición base para validar todo el gateway frente a usuarios/contribuidores.
   - **Alternativas consideradas:** iterar primero en diseño visual y componentes adicionales.
   - **Impacto / trade-offs:** entrega visual más conservadora en el corto plazo; mejor base para evolución de producto.

### Evidencia de avance

- Checklist operativo del hito publicado y actualizado con progreso: `docs/hito5_checklist.md`.
- Demo endurecido con manejo de errores HTTP accionables, persistencia de resultados en sesión y fallback de preview para archivos no imagen.
- Cobertura unitaria agregada para utilidades críticas del demo (`build_extract_payload`, `_format_confidence`, `render_bboxes`).
- README actualizado con referencia explícita al checklist de Hito 5 y estado de cierre.
- Guía operativa del demo publicada en `docs/demo_troubleshooting.md`.
- Checks de calidad en verde con entorno dev instalado: `ruff check .` y `pytest -q`.
- Riesgos post-cierre: mejorar UX de comparativas con datasets de evaluación dedicados.
- Siguiente hito habilitado: Fase 6 — Documentación y Open Source.

## Hito 6 — Documentación & Open Source

Fecha de inicio: 2026-04-05  
Fecha de cierre: 2026-04-05  
Estado: Cerrado (operativo)

### Decisiones tomadas (arranque)

1. **Iniciar Hito 6 con checklist formal para evitar cierre ambiguo**
   - **Qué se decidió:** crear `docs/hito6_checklist.md` con DoD, riesgos y criterios explícitos de salida.
   - **Por qué:** evitar cabos sueltos de documentación y garantizar trazabilidad del release OSS.
   - **Alternativas consideradas:** gestionar cierre sólo con notas de PR y README.
   - **Impacto / trade-offs:** mejor gobernanza del hito; exige mantenimiento continuo del checklist.

2. **Cerrar primero brechas de documentación operativa antes de empaquetado**
   - **Qué se decidió:** priorizar guías faltantes (troubleshooting demo, Custom Prebuilts y release checklist) antes de evaluar publicación en PyPI.
   - **Por qué:** reduce soporte reactivo y habilita adopción técnica por terceros con menor fricción.
   - **Alternativas consideradas:** priorizar release package temprano sin documentación completa.
   - **Impacto / trade-offs:** avance más sólido pero ligeramente más lento en “time-to-release”.

### Evidencia de cierre

- Checklist operativo de Hito 6 publicado: `docs/hito6_checklist.md`.
- Guía dedicada de demo/troubleshooting publicada: `docs/demo_troubleshooting.md`.
- Guía de Custom Prebuilts publicada: `docs/custom_prebuilts.md`.
- Checklist de release OSS publicado: `docs/release_checklist.md`.
- Política de versionado de contrato publicada: `docs/contract_versioning.md`.
- README actualizado con estado final del hito y enlaces a guías.
- Checks de calidad en verde: `ruff check .` y `pytest -q`.
- Riesgos post-cierre: estrategia de publicación en PyPI pendiente de decisión del equipo.
- Siguiente hito habilitado: fase de estabilización y release público.

## Tramo siguiente — Estabilización y Release Público

Fecha de inicio: 2026-04-05  
Fecha de cierre: 2026-04-05  
Estado: Cerrado (RC listo)

### Decisiones tomadas (arranque)

1. **Aplicar gate explícito Go/No-Go antes de release público**
   - **Qué se decidió:** publicar `docs/public_release_stabilization.md` con criterios objetivos de salida.
   - **Por qué:** evitar releases por percepción y exigir evidencia técnica reproducible.
   - **Alternativas consideradas:** promover release directamente desde cierre documental.
   - **Impacto / trade-offs:** mayor control de riesgo; agrega una fase corta adicional antes de publicar.

2. **Usar release candidate como paso obligatorio**
   - **Qué se decidió:** establecer paso `vX.Y.Z-rc1` previo al tag final.
   - **Por qué:** detectar regresiones de última milla en API/demo/worker antes de congelar versión.
   - **Alternativas consideradas:** publicar versión final sin RC.
   - **Impacto / trade-offs:** incrementa disciplina operativa; extiende levemente el ciclo de release.

### Evidencia de avance

- Plan de estabilización publicado: `docs/public_release_stabilization.md`.
- Checklist de release OSS actualizado con referencia a estabilización.
- README actualizado para reflejar el tramo de estabilización/release público.
- Automatización de gate pre-release añadida en `make release-readiness` y `scripts/release_readiness.sh`.
- Workflow dedicado de release readiness añadido en `.github/workflows/release-readiness.yml`.
- Changelog base publicado en `CHANGELOG.md` para preparar notas de release.
- RC `v0.1.1-rc1` ejecutado con decisión GO y evidencia en `docs/release_rc_0.1.1-rc1.md`.
- Versión del paquete promovida de `0.1.1rc1` a `0.1.1` para release estable.
- Release estable `v0.1.1` ejecutado con evidencia en `docs/release_v0.1.1.md`.
- `plan.md` sincronizado con estado real de fases (F3–F6 cerradas y F7 abierta para release estable).
- Siguiente hito habilitado: post-release (seguimiento de riesgos + canal de publicación PyPI/TestPyPI).

## Hito 7 — Post-release y decisión de distribución

Fecha de inicio: 2026-04-05  
Fecha de cierre: 2026-04-05  
Estado: Cerrado (aprobado)

### Decisiones tomadas (arranque)

1. **No cerrar el hito solo por tener release estable en GitHub**
   - **Qué se decidió:** exigir ventana de seguimiento post-release y registro de riesgos antes de declarar cierre.
   - **Por qué:** un tag estable no sustituye evidencia operativa posterior al release.
   - **Alternativas consideradas:** declarar cierre inmediato tras `v0.1.1`.
   - **Impacto / trade-offs:** menor riesgo de cierres prematuros; requiere disciplina de monitoreo corto.

2. **Forzar decisión explícita de canal de publicación**
   - **Qué se decidió:** documentar decisión entre `No publicar aún`, `TestPyPI` o `PyPI` con criterio verificable.
   - **Por qué:** evitar que PyPI quede como “pendiente eterno” entre hitos.
   - **Alternativas consideradas:** mantener decisión abierta sin fecha/trigger.
   - **Impacto / trade-offs:** clarifica ownership y próximos pasos; puede retrasar cierre si faltan credenciales.

### Evidencia de avance

- Checklist operativo de Hito 7 publicado: `docs/hito7_checklist.md`.
- README actualizado para exponer estado explícito de Hito 7 y enlace al checklist.
- Hito en estado cerrado: seguimiento post-release y decisión de canal documentados.
- Estabilización de tests async añadida en `tests/conftest.py` para asegurar ejecución local reproducible de `pytest -q`.
- Registro de riesgos post-release publicado en `docs/hito7_risk_register.md`.
- Acta de decisión de distribución cerrada en `docs/hito7_distribution_decision.md` (diferimiento controlado).
- Validación de empaquetado ejecutada (`python -m build` + `twine check dist/*`) con evidencia en `docs/hito7_packaging_validation.md`.
- Metadata de licencia modernizada en `pyproject.toml` para eliminar warnings de deprecación de `setuptools` durante build.
- Gate técnico de prepublicación TestPyPI añadido: `scripts/testpypi_publish_gate.sh` + targets `make publish-testpypi-preflight` / `make publish-testpypi`.
- Decisión de distribución documentada: **diferir publicación** (No publicar aún) con reevaluación en 2026-04-19.
- Acta de cierre aprobada publicada en `docs/hito7_cierre.md` (Go técnico y aprobación de roadmap registrada en 2026-04-05).
- Siguiente ciclo habilitado: estabilización de pendientes técnicos transversales (Hito 2 SDK real, Hito 4 FLAN-T5/colas, y política de circuit breaker distribuido).
