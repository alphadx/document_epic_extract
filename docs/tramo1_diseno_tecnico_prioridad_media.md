# Tramo 1 — Descubrimiento y diseño técnico (Prioridad media)

Fecha: 2026-04-05  
Estado: Completado (descubrimiento + diseño)

## 1) Hallazgos de arquitectura actual

### 1.1 Flujo local (`provider=local`)
- El router enruta `provider=local` a `SmolVLM2Adapter` mediante `_ADAPTER_MAP`.
- `SmolVLM2Adapter` delega inferencia al worker en `/infer` y valida contrato `StandardizedExtraction`.
- El worker soporta backend `heuristic` y `smolvlm2`, pero aún no existe backend explícito para FLAN-T5.

**Implicación:** para soportar FLAN-T5 mini/base hay que resolver dos piezas:
1. Nuevo adapter local dedicado o un adapter local genérico por modelo.
2. Extensión del worker para ruta/selección de backend FLAN-T5.

### 1.2 Resiliencia LLM y circuit breaker
- Existe `CircuitBreakerStore` en memoria de proceso (por clave de modelo).
- El LLM adapter consume ese store in-memory y aplica threshold/cooldown por settings.

**Implicación:** en multi-réplica no hay estado compartido; cada réplica abre/cierra circuitos de forma independiente.

### 1.3 OCR cloud real
- AWS/GCP/Azure adapters intentan SDK real cuando no hay mock payload.
- Ya existe normalización transversal de errores vía `normalize_provider_error(...)`.
- Pendiente formal: evidencia reproducible de escenarios credenciales/timeout/proveedor caído para cada proveedor.

## 2) Diseño propuesto para `FlanT5Adapter` + hardening de colas

## 2.1 Diseño de integración local FLAN-T5

### Decisión A — Adapter nuevo dedicado (`FlanT5Adapter`)
- **Se propone crear** `adapters/local/flant5.py` para separar responsabilidades respecto de `SmolVLM2Adapter`.
- El router mapeará `provider=local` a un adapter local unificado (manteniendo compatibilidad) o se agregará una regla de selección por modelo.

### Decisión B — Selección de backend en worker por familia de modelo
- Si `engine_config.model` contiene `flan-t5-mini` o `flan-t5-base`, worker ejecuta backend FLAN.
- Si contiene `smolvlm2`, mantiene backend actual.
- Se preserva `LOCAL_WORKER_BACKEND=heuristic` para pruebas rápidas.

### Decisión C — Contrato de salida uniforme
- FLAN-T5 en worker siempre devuelve `WorkerInferResponse` con `result` validable por `StandardizedExtraction`.
- Cuando no haya tablas/cajas, mantener valores vacíos (`tables=[]`, `bounding_box=None`) para consistencia de contrato.

## 2.2 Hardening de colas asíncronas del worker

### Objetivos técnicos
1. **Backpressure:** tamaño máximo de cola configurable.
2. **Timeout por job:** cancela ejecución larga y responde error homogéneo.
3. **Reintentos acotados:** sólo para errores transientes identificables.
4. **Aislamiento por modelo:** evitar hambruna de una familia de modelo sobre otra.

### Estrategia mínima viable (MVP)
- Introducir cola `asyncio.Queue(maxsize=N)` por backend (`smolvlm2`, `flan_t5`).
- Worker interno consumidor por backend con semáforo de concurrencia.
- Respuesta `ExtractionError` normalizada cuando la cola esté llena o timeout vencido.

## 3) Matriz de pruebas objetivo (para siguientes tramos)

## 3.1 Local FLAN-T5 + cola
- Unit: parsing payload FLAN, compatibilidad de contrato, fallback de `engine_used`.
- Unit: cola llena -> error esperado.
- Unit: timeout/cancelación -> error esperado.
- Integración: `POST /extract` con `provider=local`, `model=flan-t5-mini` y `flan-t5-base`.

## 3.2 OCR cloud real (AWS/GCP/Azure)
Escenarios por proveedor:
1. Credenciales válidas (o entorno de sandbox con secreto vigente).
2. Credenciales faltantes/incorrectas.
3. Timeout controlado.
4. Error de proveedor/servicio no disponible.

Evidencia requerida:
- salida de tests,
- mensaje de error normalizado,
- referencia de configuración usada.

## 3.3 Circuit breaker distribuido
- Test de diseño (documental) para política con estado compartido.
- Prueba de integración futura con backend de estado (Redis) y múltiples réplicas lógicas.

## 4) Variables de entorno/configuración propuestas

### Local worker / colas
- `LOCAL_WORKER_QUEUE_SIZE` (default sugerido: 32)
- `LOCAL_WORKER_JOB_TIMEOUT_MS` (default sugerido: 20000)
- `LOCAL_WORKER_MAX_RETRIES` (default sugerido: 1)
- `LOCAL_WORKER_MAX_CONCURRENCY` (default sugerido: 1 o 2 por backend)

### OCR cloud (evidencia real)
- AWS: credenciales estándar de SDK (envs AWS).
- GCP: `GCP_PROJECT_ID`, `GCP_LOCATION`, `GCP_PROCESSOR_ID`.
- Azure: `azure_endpoint`, `azure_key` en `api_keys` de request.

### Circuit breaker distribuido (propuesta)
- `LLM_CIRCUIT_BACKEND=memory|redis`
- `LLM_CIRCUIT_REDIS_URL`
- `LLM_CIRCUIT_OPEN_TTL_MS`

## 5) Riesgos y mitigaciones
- **Riesgo:** romper compatibilidad del flujo local actual.
  - **Mitigación:** mantener tests actuales de `SmolVLM2Adapter` e integración local.
- **Riesgo:** incrementar latencia por cola.
  - **Mitigación:** métricas de cola + timeouts explícitos.
- **Riesgo:** falsa cobertura cloud por entornos sin credenciales reales.
  - **Mitigación:** marcar claramente pruebas con dependencia de secretos y separar modo mock/real.

## 6) Salida de Tramo 1 y pase de etapa

Se considera completado este tramo porque:
- Se definió diseño técnico para FLAN-T5 local y hardening de cola.
- Se definió matriz de pruebas para OCR cloud real.
- Se delineó política técnica base para circuit breaker distribuido.

**Siguiente tramo sugerido:** Tramo 2 — Implementación local (`FlanT5Adapter` + hardening worker).
