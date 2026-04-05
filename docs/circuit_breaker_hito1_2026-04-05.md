# Hito 1 (Fase A) — Circuit Breaker Distribuido

Fecha: 2026-04-05  
Estado: Cerrado  
Owner: Equipo Core OmniExtract (API/Plataforma)

## Objetivo del hito

Entregar la base técnica para soportar circuit breaker con backend distribuido opcional (Redis), manteniendo compatibilidad con fallback local en memoria.

## Cambios implementados

1. Se definió contrato de store compartido para circuit breaker.
2. Se separó backend en memoria (`InMemoryCircuitBreakerStore`) para modo local/fallback.
3. Se agregó backend Redis (`RedisCircuitBreakerStore`) con clave prefijada y estado persistente por modelo.
4. Se incorporó factoría de inicialización (`create_circuit_breaker_store`) con fallback automático a memoria cuando Redis no está disponible.
5. Se agregaron flags de configuración para backend y prefijo de claves:
   - `llm_circuit_breaker_backend` (`memory` por defecto)
   - `llm_circuit_breaker_redis_url`
   - `llm_circuit_breaker_redis_prefix`

## Activación

Para usar backend Redis:

```bash
export LLM_CIRCUIT_BREAKER_BACKEND=redis
export LLM_CIRCUIT_BREAKER_REDIS_URL=redis://redis:6379/0
export LLM_CIRCUIT_BREAKER_REDIS_PREFIX=cb:llm_router:
```

Si Redis no responde o falta dependencia, el sistema registra el incidente y vuelve a backend en memoria para no interrumpir la operación.

## Evidencia de pruebas

- Tests unitarios de backend en memoria (open/reset).
- Test de fallback a memoria cuando backend Redis falla.
- Test de transición básica en backend Redis con cliente simulado.

Archivo de referencia: `tests/unit/test_llm_resilience.py`.
