# Getting Started

Guía rápida para ejecutar OmniExtract Gateway en local y validar el flujo end-to-end.

## Requisitos

- Docker + Docker Compose v2+
- Python 3.11+ (si ejecutas sin Docker)
- Credenciales de proveedor (opcionales según motor)

## Opción A — Stack completo con Docker (recomendado)

```bash
git clone https://github.com/alphadx/document_epic_extract.git
cd document_epic_extract
cp .env.example .env
# editar .env
docker compose up -d
```

Servicios:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Demo Streamlit: `http://localhost:8501`

## Opción B — Desarrollo local sin Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn api.main:app --reload --port 8000
```

En otra terminal:

```bash
source .venv/bin/activate
streamlit run demo/app.py
```

## Variables de entorno OCR cloud (referencia)

- AWS Textract: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
- GCP Document AI: `GCP_PROJECT_ID`, `GCP_LOCATION`, `GCP_PROCESSOR_ID`, `GOOGLE_APPLICATION_CREDENTIALS`
- Azure Document Intelligence: `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT`, `AZURE_DOCUMENT_INTELLIGENCE_KEY`

## Primer request (LLM router)

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "document": "<base64_or_url>",
    "engine_config": {
      "provider": "llm_router",
      "model": "claude-3-5-sonnet-20241022",
      "api_keys": {"anthropic": "sk-ant-..."}
    },
    "extraction_target": {
      "document_type": "invoice"
    }
  }'
```

## Request de prueba mock (OCR cloud sin SDK real)

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "document": "ignored",
    "engine_config": {
      "provider": "aws",
      "model": "textract",
      "api_keys": {
        "mock_response_json": "{\"Blocks\":[{\"Id\":\"l1\",\"BlockType\":\"LINE\",\"Text\":\"Factura 100\"}]}"
      }
    },
    "extraction_target": {"document_type": "invoice"}
  }'
```

## Checks recomendados antes de PR

```bash
ruff check .
pytest -q
make release-readiness
```

## Siguientes pasos

- Ver [Custom Prebuilts](custom_prebuilts.md)
- Ver [Agregar modelos](adding_models.md)
- Ver [TODO consolidado](../TODO.md)
