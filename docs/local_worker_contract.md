# Contrato final del Worker local (`/infer`)

Estado: **Activo**  
Última actualización: **2026-04-05**

## Endpoint

- Método: `POST`
- Ruta: `/infer`
- Servicio: `adapters.local.worker_app:app` (puerto `8001` en Docker)

## Request (JSON)

```json
{
  "document": "<base64_or_url>",
  "engine_config": {
    "provider": "local",
    "model": "smolvlm2-2.2b-instruct",
    "custom_endpoint": null
  },
  "extraction_target": {
    "document_type": "invoice",
    "custom_fields": ["invoice_number", "total_amount"]
  }
}
```

## Response (JSON)

```json
{
  "result": {
    "raw_text": "invoice_number: INV-100\ntotal_amount: 125.00",
    "fields": [
      { "key": "invoice_number", "value": "INV-100", "confidence": null, "bounding_box": null },
      { "key": "total_amount", "value": "125.00", "confidence": null, "bounding_box": null }
    ],
    "tables": [],
    "engine_used": "local_worker:smolvlm2-2.2b-instruct",
    "processing_time_ms": null
  },
  "backend": "heuristic",
  "device": "cpu"
}
```

## Comportamiento de backend (CPU/GPU)

- `LOCAL_WORKER_BACKEND=heuristic` (default): sin dependencias pesadas; útil para smoke tests y pipelines locales.
- `LOCAL_WORKER_BACKEND=smolvlm2`: intenta cargar SmolVLM2 vía `transformers`.
- `LOCAL_WORKER_DEVICE=auto|cpu|cuda`:
  - `auto`: usa CUDA si está disponible, si no CPU.
  - `cpu`: fuerza ejecución CPU.
  - `cuda`: fuerza GPU (requiere runtime NVIDIA habilitado).

## Variables de entorno del Worker

- `LOCAL_WORKER_BACKEND` (default: `heuristic`)
- `LOCAL_WORKER_DEVICE` (default: `auto` en backend SmolVLM2)
- `LOCAL_WORKER_MODEL_ID` (default: `HuggingFaceTB/SmolVLM2-2.2B-Instruct`)
- `LOCAL_WORKER_MAX_NEW_TOKENS` (default: `256`)

## Errores esperados

- `502` en API core (`/extract`) cuando el Worker no responde, devuelve HTTP error o payload inválido.
- `422` para errores de validación de esquema request en `/infer`.
