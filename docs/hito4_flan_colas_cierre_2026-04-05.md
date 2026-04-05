# Hito 4 — Cierre formal de FlanT5 + hardening de colas locales

Fecha: 2026-04-05  
Estado: Cerrado
Owner: Equipo Core OmniExtract (API/Plataforma)

## Alcance cerrado

1. `FlanT5Adapter` implementado para flujo `provider=local`.
2. Enrutamiento por familia de modelo (`flan-t5`) hacia adapter dedicado.
3. Worker local con controles de cola/concurrencia/timeout:
   - `LOCAL_WORKER_QUEUE_SIZE`
   - `LOCAL_WORKER_MAX_CONCURRENCY`
   - `LOCAL_WORKER_JOB_TIMEOUT_MS`
4. Cobertura de pruebas unitarias e integración para ruta local FLAN y contrato API↔Worker.

## Evidencia

- Código adapter: `adapters/local/flant5.py`
- Worker hardening: `adapters/local/worker_app.py`
- Routing por modelo: `api/services/router_service.py`
- Tests unitarios: `tests/unit/test_flant5_adapter.py`, `tests/unit/test_worker_app.py`, `tests/unit/test_router_service.py`
- Test integración local: `tests/integration/test_extract_local_provider.py`

## Criterio de cierre aplicado

Se considera cerrado porque existe implementación funcional, pruebas automatizadas y trazabilidad documental del ítem local de prioridad media.
