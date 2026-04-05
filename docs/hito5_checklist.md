# Hito 5 — Checklist de ejecución y cierre (Demo Front-end)

Estado: **Cerrado (operativo)**  
Última actualización: **2026-04-05 (cierre técnico + documental)**

## Objetivo del hito
Cerrar un demo de producto **operativo, reproducible y verificable** en Streamlit que permita comparar motores de extracción (OCR, LLM Router y Local), detectar errores de integración temprano y servir como puerta de entrada para contribuciones.

## Alcance obligatorio (DoD de Hito 5)

### 1) UX mínima de operación (flujo completo)
- [x] Cargar documento (imagen/PDF) desde UI.
- [x] Configurar Engine A (`provider`, `model`, `api_key`) y ejecutar extracción.
- [x] Permitir comparación side-by-side con Engine B opcional.
- [x] Soportar `document_type` prebuilt y modo `free` con `custom_fields`.
- [x] Mostrar errores HTTP/API con mensajes accionables (status code + causa) en vez de fallo genérico.
- [x] Evitar duplicar requests por rerender y mantener resultados en `st.session_state`.

### 2) Visualización y legibilidad de resultados
- [x] Render de campos y JSON completo por motor.
- [x] Visualización de bounding boxes sobre la imagen original.
- [x] Fallback claro cuando el archivo no sea imagen (ej. PDF sin rasterización disponible).
- [x] Formatear tabla de campos con columnas estables y confidence robusto (`0.0` no debe verse como vacío).

### 3) Contrato técnico UI ↔ API
- [x] Payload de `POST /extract` alineado con esquema actual (`document`, `engine_config`, `extraction_target`).
- [x] Validar explícitamente errores de contrato (`422`) y credenciales (`401`/`403`) con mensajes guiados.
- [x] Documentar matriz de compatibilidad demo por provider/modelo en README.

### 4) Pruebas y calidad del demo
- [x] Añadir tests unitarios para componentes demo críticos (`encode_document`, `render_bboxes`, normalización de fields).
- [x] Añadir al menos un test de integración de UI lógica (con funciones puras o helpers) sin depender de red externa.
- [x] Mantener quality gates globales en verde (`ruff check .`, `pytest -q`).

### 5) Documentación de cierre
- [x] Publicar guía de uso del demo (setup, ejemplos, troubleshooting) en `docs/`.
- [x] Actualizar `README.md` con estado de Hito 5 y comandos de verificación.
- [x] Registrar decisiones del hito en `docs/milestone_decisions.md` con evidencia de cierre.

## Riesgos de seguimiento
- Render de PDF: `bbox_renderer` asume imagen raster y puede fallar con PDF binario.
- Diferencias entre proveedores pueden producir salidas incompletas y confundir UX sin mensajes guiados.
- Falta de estado persistente de sesión puede degradar experiencia en comparaciones repetidas.

## Criterio para avanzar al siguiente hito
Hito 5 se considera cerrado cuando el demo pueda ejecutarse de forma reproducible, manejar errores comunes de integración sin ambigüedad, conservar resultados en sesión y contar con pruebas/documentación mínima de operación.

## Evidencia de cierre
- Quality gates verificados en entorno local con `ruff check .` y `pytest -q`.
- Documentación de transición a Fase 6 publicada en `docs/hito6_checklist.md`.
