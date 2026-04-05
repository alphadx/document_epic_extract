# Hito 3 (Fase C) — Observabilidad y operación

Fecha: 2026-04-05  
Estado: Cerrado  
Owner: Equipo Core OmniExtract (API/Plataforma)

## Objetivo del hito

Habilitar observabilidad operativa mínima del circuit breaker distribuido con métricas y eventos de transición trazables para operación on-call.

## Implementación

### 1) Métricas internas

Se incorporó `CircuitBreakerTelemetry` con snapshot programático de:

- `cb_state{provider,key}` (0=`closed`, 1=`open`, 2=`half_open`)
- `cb_open_total{provider,key}`
- `cb_reject_total{provider,key}`
- `cb_half_open_probe_total{provider,key,result}`

Acceso por helper: `get_circuit_breaker_metrics_snapshot()`.

Exposición operativa (MVP): endpoint `GET /ops/circuit-breaker/metrics`.

### 2) Logs estructurados de transición

Se emite evento con formato:

`event=cb_transition provider=<...> key=<...> from_state=<...> to_state=<...> reason=<...> cooldown_ms=<...> failures=<...>`

Casos cubiertos en este hito:
- transición hacia `open` por fallo de provider,
- transición a `closed` por recuperación exitosa.

### 3) Integración en adapter LiteLLM

En `LiteLLMVisionAdapter` se instrumentó:
- incremento de `cb_reject_total` cuando `is_open(...)` rechaza llamadas;
- incremento de `cb_open_total` y log de transición al abrir circuito;
- actualización de `cb_state` tras fallos y reset exitoso.

## Evidencia de pruebas

- `tests/unit/test_llm_resilience.py`
  - validación de estructura/valores del snapshot de métricas.
- `tests/unit/test_litellm_adapter.py`
  - validación de incrementos `cb_open_total` y `cb_reject_total` en flujo de apertura + rechazo.

## Diseño de tablero operativo (MVP)

Paneles sugeridos:

1. **Estado actual de circuitos**
   - Fuente: `cb_state`
   - Agrupación: `provider`, `key`
2. **Aperturas por ventana**
   - Fuente: `cb_open_total` (delta por 5m/15m)
3. **Rechazos por circuito abierto**
   - Fuente: `cb_reject_total` (delta por 5m/15m)
4. **Half-open probes**
   - Fuente: `cb_half_open_probe_total` por `result`

Alertas mínimas:
- `cb_reject_total` creciendo de forma sostenida durante 3 ventanas.
- `cb_open_total` anómalo para un mismo `provider/key`.
