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


---

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
