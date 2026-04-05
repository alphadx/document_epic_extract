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
