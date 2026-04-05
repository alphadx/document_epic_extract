# Registro de Decisiones por Hito

Este documento deja constancia de **qué decisiones se tomaron en cada hito, por qué se tomaron y cuál fue su impacto**.

> Norma del proyecto (obligatoria): **cada hito nuevo debe actualizar este archivo** antes de darse por cerrado.

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
