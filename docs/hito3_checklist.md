# Hito 3 — Checklist de ejecución y cierre

Estado: **Completado técnicamente (pendiente cierre formal)**  
Última actualización: **2026-04-04**

## Objetivo del hito
Implementar el meta-gateway LLM con LiteLLM y cerrar el flujo end-to-end de extracción basada en prebuilts.

## Alcance obligatorio (DoD de Hito 3)

### 1) Integración funcional de `LiteLLMVisionAdapter`
- [x] Cargar prebuilt desde `PrebuiltService` según `document_type`.
- [x] Construir mensajes para LiteLLM (`system` + input multimodal/documento).
- [x] Ejecutar `litellm.acompletion(...)` con configuración de modelo y credenciales.
- [x] Parsear respuesta JSON al esquema `StandardizedExtraction`.
- [x] Fallback de robustez cuando el modelo devuelva texto no JSON estricto.

### 2) Contrato y validación
- [x] Validar que `engine_config.provider == "llm_router"` enrute correctamente.
- [x] Asegurar que `engine_used` refleje proveedor/modelo efectivo.
- [x] Conservar `processing_time_ms` desde `router_service`.

### 3) Manejo de errores y seguridad
- [x] Errores explícitos para prebuilt inexistente y respuesta inválida del LLM.
- [x] No loggear secretos (`api_keys`) en excepciones ni trazas.
- [x] Timeouts y límites razonables para llamadas al proveedor.

### 4) Pruebas mínimas de cierre
- [x] Unit tests del adapter (mocks de LiteLLM).
- [x] Unit tests de parseo/fallback JSON.
- [x] Integración básica del endpoint `/extract` con `provider=llm_router` (mock).
- [x] `ruff check .` y `pytest -q` en verde.

### 5) Documentación de cierre
- [x] Actualizar `README.md` con estado de Fase 3 y comandos de verificación.
- [x] Registrar decisiones del hito en `docs/milestone_decisions.md`.
- [x] Añadir ejemplos de request/response LLM en `docs/openapi.md`.

## Riesgos a cerrar antes de declarar “terminado”
- Ambigüedad de formato de salida en modelos de visión heterogéneos.
- Diferencias de capacidades multimodales entre proveedores.
- Costo y latencia por reintentos/fallback de parsing.

## Criterio para avanzar al siguiente hito
Se puede avanzar a Hito 4 sólo cuando **todos** los checks del DoD estén marcados y exista evidencia en tests + documentación.
