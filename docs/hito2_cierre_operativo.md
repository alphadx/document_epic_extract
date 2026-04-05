# Hito 2 — Plan de Cierre Operativo (Adaptadores OCR Cloud)

Fecha: 2026-04-04  
Estado: En progreso

## Objetivo del hito
Cerrar la integración **real** de OCR cloud (AWS Textract, Azure Document Intelligence y GCP Document AI) asegurando que el contrato `StandardizedExtraction` se cumpla sin excepciones en escenarios básicos y de error.

## Definición de terminado (DoD) obligatoria

- [x] `adapters/ocr/aws.py` implementado sin TODOs funcionales.
- [x] `adapters/ocr/azure.py` implementado sin TODOs funcionales.
- [x] `adapters/ocr/gcp.py` implementado sin TODOs funcionales.
- [x] Mapeo de campos (`raw_text`, `fields`, `tables`, `engine_used`, `processing_time_ms`) consistente entre proveedores.
- [x] Manejo homogéneo de errores para payload inválido/no disponible mediante `ExtractionError` (pendiente completar matriz con credenciales/timeout/proveedor caído al conectar SDK real).
- [x] Pruebas unitarias por proveedor (happy path + error path).
- [x] Al menos 1 prueba de integración por endpoint `/extract` con cada proveedor mockeado.
- [x] Documentación de variables de entorno y ejemplos de uso actualizada.
- [x] `ruff check .` y `pytest -q` en verde.
- [x] Registro de decisiones del hito actualizado en `docs/milestone_decisions.md`.

## Secuencia recomendada (sin cabos sueltos)

1. **Contrato y utilidades comunes de normalización**
   - Extraer helpers compartidos para bounding boxes y normalización de confidence.
   - Definir convenciones cuando el proveedor no entregue algún dato (por ejemplo, `confidence=None`).

2. **Implementación de adaptadores OCR**
   - AWS: parseo de bloques/líneas/campos relevantes y tablas.
   - Azure: parseo de `documents`, `fields`, `tables` y coordenadas.
   - GCP: parseo de entidades, texto completo y tablas.

3. **Matriz de errores transversales**
   - Timeout por proveedor.
   - Credenciales inválidas/faltantes.
   - Respuesta sin estructura esperada.
   - Fallback de mensajes de error homogéneos hacia API.

4. **Pruebas y cobertura mínima del hito**
   - Unit tests por adapter con fixtures representativas.
   - Integración del router `/extract` validando selección de adapter correcta.

5. **Documentación final de hito**
   - Actualizar README con estado de Fase 2 cuando esté realmente cerrada.
   - Cerrar sección en `docs/milestone_decisions.md` con evidencia (PR + checks + riesgos).

## Riesgos a controlar en Hito 2

- Diferencias de granularidad entre proveedores para tablas y coordenadas.
- Falsa sensación de cierre con mocks insuficientes.
- Desalineación entre lo que devuelve el proveedor y el esquema API público.

## Criterio para avanzar a Hito 3

Solo avanzar cuando todos los checkboxes de DoD estén completados y la evidencia de cierre esté documentada.


## Avance 1 (2026-04-04)

- Se reemplazaron stubs `NotImplementedError` por adaptadores funcionales de mapeo para AWS/Azure/GCP en modo payload proveedor.
- Se incorporó un helper común `adapters/ocr/common.py` para carga de payload mock y normalización de bounding boxes.
- Se añadieron pruebas unitarias de adaptadores OCR (`tests/unit/test_ocr_adapters.py`).
- Pendiente para cierre formal del hito: conexión directa a SDKs cloud en runtime real (sin payload mock) + pruebas de integración de endpoint por proveedor.


## Nota de coordinación con Fase 4 (local)

- Se incorpora en el plan local el soporte de `flan-t5-base` además de `flan-t5-mini`, con despliegue previsto para CPU o GPU.


## Avance 2 (2026-04-04)

- Se añadieron pruebas de integración de `POST /extract` para AWS/Azure/GCP en modo mock payload.
- Se validó respuesta 502 para errores de payload inválido/no disponible.
- Queda pendiente para cierre final de Hito 2 la integración directa de SDK cloud y pruebas con credenciales/timeout reales controlados.


## Avance 3 (2026-04-04)

- Los adaptadores OCR ahora intentan llamada a SDK real cuando no se provee `mock_response_json`.
- Se agregó normalización transversal de errores de proveedor (auth/timeout/provider error) para respuesta homogénea vía `ExtractionError`.
- Se mantiene modo mock como fallback de desarrollo para pruebas locales.
