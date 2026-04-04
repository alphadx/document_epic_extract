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

Fecha de actualización: 2026-04-04  
Estado: Cerrado técnicamente

### Decisiones tomadas

1. **Definir DoD explícito para evitar cierre parcial del hito**
   - **Qué se decidió:** formalizar checklist de cierre en `docs/hito3_checklist.md` con criterios técnicos, pruebas y documentación.
   - **Por qué:** reducir ambigüedad sobre qué significa “terminar Hito 3”.
   - **Alternativas consideradas:** gestionar avances sólo en conversaciones/PRs sin checklist persistente.
   - **Impacto / trade-offs:** mayor claridad y trazabilidad; requiere mantener checklist actualizado en cada avance.

2. **Mantener el hito en progreso hasta completar hardening e integración endpoint**
   - **Qué se decidió:** mantener el estado del hito como “En progreso” aunque el `LiteLLMVisionAdapter` ya tenga una implementación funcional inicial.
   - **Por qué:** aún faltan timeouts/límites e integración del endpoint con `provider=llm_router` para declarar cierre total.
   - **Alternativas consideradas:** cerrar el hito al completar solo la implementación base del adapter.
   - **Impacto / trade-offs:** cronograma más estricto, pero mejor calidad de salida y menor retrabajo.

### Evidencia parcial

- PR(s): actualización documental de ejecución de Hito 3 + implementación funcional inicial del adapter LiteLLM con hardening básico (timeouts/límites) y prueba de integración del endpoint.
- Checks ejecutados: `ruff check .`, `pytest -q`.
- Riesgos pendientes: monitoreo en producción de variabilidad por proveedor LLM.
- Siguiente hito habilitado: Fase 4 — Ejecución Local (SmolVLM2).
