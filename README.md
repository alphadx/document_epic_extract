# OmniExtract Gateway

> Unified document extraction gateway: OCR cloud + LLMs + local models under a single API contract.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)

## ¿Qué es?

**OmniExtract Gateway** unifica la extracción de datos estructurados desde imágenes/PDFs en una sola API (`POST /extract`).

- Soporta OCR cloud (AWS/Azure/GCP), LLMs vía LiteLLM y modelos locales.
- Estandariza la salida en `StandardizedExtraction`.
- Permite usar prebuilts (invoice, receipt, id_card, etc.) o plantillas personalizadas.

## Propuesta de valor

- **Sin lock-in de proveedor**: cambia de motor sin romper integraciones.
- **Contrato de salida único**: mismo JSON para motores deterministas o probabilísticos.
- **Extensible por configuración**: registry dinámico de modelos y plantillas YAML.
- **Listo para demo y operación local**: API FastAPI + demo Streamlit + docker compose.

## Demo rápida

```bash
git clone https://github.com/alphadx/document_epic_extract.git
cd document_epic_extract
cp .env.example .env
# editar .env con credenciales
docker compose up -d
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Demo: http://localhost:8501

## Arquitectura (alto nivel)

```text
Demo UI (Streamlit)
        │
        ▼
API Core (FastAPI Meta-Gateway)
   ├── OCR adapters (AWS/Azure/GCP)
   ├── LLM router adapter (LiteLLM)
   └── Local adapter (Worker)
```

## Documentación

> El README queda orientado a producto. La documentación operativa/técnica vive en `docs/`.

- **Portal de documentación**: [`docs/README.md`](docs/README.md)
- **Getting Started**: [`docs/getting_started.md`](docs/getting_started.md)
- **Roadmap y arquitectura**: [`plan.md`](plan.md)
- **Avances de hitos**: [`docs/hitos_avances.md`](docs/hitos_avances.md)
- **Backlog/TODO consolidado**: [`TODO.md`](TODO.md)

## Estado del proyecto

- Release estable actual documentado: **v0.1.1**.
- Hito 7 en estado de **cierre propuesto** (pendiente aprobación explícita).
- Publicación en PyPI/TestPyPI definida como decisión explícita de roadmap (ver TODO y docs de hito 7).

## Contribuir

Consulta [`CONTRIBUTING.md`](CONTRIBUTING.md) para guías de contribución.
