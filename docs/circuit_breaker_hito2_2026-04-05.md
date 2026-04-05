# Hito 2 (Fase B) — Consistencia distribuida y concurrencia

Fecha: 2026-04-05  
Estado: Cerrado  
Owner: Equipo Core OmniExtract (API/Plataforma)

## Objetivo del hito

Garantizar que las transiciones de estado del circuit breaker Redis se ejecuten de forma atómica en escenarios multi-réplica y con protección ante condiciones de carrera.

## Cambios implementados

1. **Atomicidad con Lua** en Redis:
   - `record_failure`: incremento + transición `closed/open` + `updated_at_ms` en una sola operación atómica.
   - `reset`: transición a `closed` con reseteo de contadores dentro de script Lua.
2. **CAS por versión (`updated_at_ms`)**:
   - Nuevo método `reset_if_version(key, expected_updated_at_ms=...)`.
   - Si la versión no coincide, el cierre no se aplica y se evita overwrite de otro nodo.
3. **Compatibilidad operativa**:
   - `reset(key)` se mantiene para el flujo existente y delega en el reset atómico sin CAS obligatorio.

## Cobertura de pruebas agregada

- Validación de CAS correcto/incorrecto para `reset_if_version`.
- Simulación de concurrencia paralela con múltiples workers sobre `record_failure` verificando ausencia de pérdida de incrementos.

Archivo de referencia: `tests/unit/test_llm_resilience.py`.

## Notas operativas

- Este hito cubre consistencia de transiciones principales en Fase B.
- La semántica completa `HALF_OPEN` y observabilidad ampliada queda para Hito 3 (Fase C).
