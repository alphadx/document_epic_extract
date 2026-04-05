# Demo Streamlit — Guía de uso y troubleshooting

Última actualización: **2026-04-05**

## Objetivo
Documentar una guía rápida para operar el demo, validar el flujo UI↔API y resolver errores comunes sin ambigüedad.

## Setup mínimo

1. Instalar dependencias de desarrollo:

```bash
pip install -e ".[dev,demo]"
```

2. Levantar API local:

```bash
uvicorn api.main:app --reload --port 8000
```

3. Ejecutar demo:

```bash
streamlit run demo/app.py
```

## Flujo recomendado de validación

1. Cargar una imagen de documento (invoice/receipt).
2. Configurar `Engine A` con un provider soportado (ej. `aws` o `llm_router`).
3. Ejecutar extracción y verificar:
   - tabla de campos
   - JSON estandarizado
   - render de bounding boxes (si aplica)
4. Activar comparación con `Engine B` para validar side-by-side.

## Troubleshooting rápido

### Error `422 Unprocessable Entity`
- Revisar que el payload tenga `document`, `engine_config` y `extraction_target`.
- Confirmar que `document_type=free` incluya `custom_fields`.

### Error `401` / `403`
- Validar API key del proveedor en la UI.
- Confirmar que la key tenga permisos para el modelo seleccionado.

### Preview de PDF no renderiza bounding boxes
- Comportamiento esperado: para PDF sin rasterización disponible se muestra fallback sin overlay.
- Recomendación: validar bounding boxes con imagen (`png`/`jpg`) al depurar layout.

### No responde la extracción
- Verificar que la API esté arriba en `http://localhost:8000`.
- Revisar logs de Streamlit y API para timeout o errores de red.

## Comandos de verificación del demo

```bash
ruff check .
pytest -q
```
