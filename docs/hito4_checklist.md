# Hito 4 — Checklist de ejecución y cierre (Ejecución Local)

Estado: **Cerrado (operativo)**  
Última actualización: **2026-04-05 (cierre técnico de operación local)**

## Objetivo del hito
Implementar inferencia local robusta para documentos con `provider=local`, iniciando por `SmolVLM2Adapter` y dejando una base clara para `FlanT5Adapter`, con observabilidad, pruebas y documentación de operación CPU/GPU.

## Alcance obligatorio (DoD de Hito 4)

### 1) Adapter local funcional (`SmolVLM2Adapter`)
- [x] Implementar llamada HTTP asíncrona a Worker (`WORKER_BASE_URL`) con timeout configurable.
- [x] Mapear la respuesta del Worker al esquema `StandardizedExtraction`.
- [x] Manejar errores de red/timeout con excepciones explícitas y sin exponer secretos.
- [x] Asegurar `engine_used` consistente para trazabilidad (modelo local efectivo).

### 2) Contrato Worker ↔ API
- [x] Definir y documentar payload mínimo de `/infer` (request/response).
- [x] Validar compatibilidad del contrato en tests (caso OK + casos de error controlados).
- [x] Mantener estabilidad del contrato público de `POST /extract`.

### 3) Configuración y operación local
- [x] Documentar ejecución en CPU (camino mínimo reproducible).
- [x] Documentar ejecución en GPU (flags/perfiles Docker y prerequisitos).
- [x] Definir parámetros operativos mínimos: timeout, tamaño de payload, concurrencia esperada.

### 4) Pruebas mínimas de cierre
- [x] Unit tests del adapter local (éxito, timeout, respuesta inválida).
- [x] Integración de `POST /extract` con `provider=local` (mockeando Worker).
- [x] Integración de `POST /extract` con contrato real de Worker (sin `mock_response_json`).
- [x] Quality gates en verde: `ruff check .` y `pytest -q`.

### 5) Documentación de cierre
- [x] Actualizar `README.md` con estado de Hito 4 y guía de uso local.
- [x] Registrar decisiones del hito en `docs/milestone_decisions.md`.
- [x] Añadir guía técnica del flujo local (API ↔ Worker) en `docs/` si aplica.

## Riesgos de seguimiento (no bloqueantes para arranque)
- Coste de memoria/latencia en entornos sin GPU.
- Variabilidad de desempeño según hardware local.
- Gestión de colas para cargas concurrentes altas (etapa posterior).

## Criterio para avanzar al siguiente hito
Hito 4 se considera cerrado cuando `provider=local` funcione end-to-end con pruebas automatizadas, documentación operativa CPU/GPU y sin tareas abiertas del DoD.
