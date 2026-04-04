# OmniExtract Gateway

> **Unified document extraction meta-gateway — open source, containerized, and engine-agnostic.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)

---

## ¿Qué es OmniExtract Gateway?

**OmniExtract Gateway** es un meta-gateway que unifica la extracción de datos estructurados (texto, pares clave-valor, tablas y coordenadas) desde imágenes y documentos en un único punto de entrada (API). Abstrae completamente la diferencia entre:

| Tipo de Motor | Ejemplos |
| :--- | :--- |
| **OCR Cloud (determinista)** | AWS Textract, Azure Document Intelligence, GCP Document AI |
| **LLMs Comerciales** | Claude 4, GPT-4.1, Gemini 2.0, DeepSeek V3, Mistral |
| **LLMs Open Source** | Qwen2.5-VL, Llama-3.2-Vision, Phi-4 |
| **Modelos Locales** | SmolVLM2, flan-t5 |

Todos los motores devuelven el **mismo esquema JSON estandarizado** (`StandardizedExtraction`). Tu aplicación no necesita saber si está hablando con un OCR clásico o con un LLM de última generación.

---

## Características Principales

- 🔌 **Agnóstico al Motor** — Cambia entre AWS Textract y Claude 3.5 Sonnet modificando un parámetro.
- 📄 **Prebuilt Templates** — Plantillas listas para facturas, recibos, DNIs, estados de cuenta, y más.
- 🧩 **Custom Prebuilts** — Define tus propios campos y el gateway genera el prompt óptimo automáticamente.
- 📦 **100% Contenerizado** — Docker Compose listo para usar en local o en producción.
- 🗂️ **Registro Dinámico de Modelos** — Añade nuevos modelos vía PR sin tocar código.
- 🖼️ **Demo Interactivo** — Interfaz Streamlit con comparación side-by-side y visualización de bounding boxes.
- 🔒 **Sin Lock-in** — BYOE (Bring Your Own Endpoint) para modelos y endpoints personalizados.

---

## Inicio Rápido

### Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/install/) v2+
- Python 3.11+ (para desarrollo local)

### Levantar el Stack Completo

```bash
# 1. Clonar el repositorio
git clone https://github.com/alphadx/document_epic_extract.git
cd document_epic_extract

# 2. Copiar variables de entorno y configurar tus API keys
cp .env.example .env
# Editar .env con tus credenciales (AWS, OpenAI, Anthropic, etc.)

# 3. Levantar todos los servicios
docker compose up -d

# API Core disponible en:  http://localhost:8000
# Demo UI disponible en:   http://localhost:8501
# Docs (Swagger) en:       http://localhost:8000/docs
```

### Ejemplo de Uso (cURL)

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "document": "<base64_encoded_image_or_url>",
    "engine_config": {
      "provider": "llm_router",
      "model": "claude-3-5-sonnet-20241022",
      "api_keys": { "anthropic": "sk-ant-..." }
    },
    "extraction_target": {
      "document_type": "invoice"
    }
  }'
```

### Respuesta Estandarizada

```json
{
  "raw_text": "FACTURA N° 0001-00045678\nFecha: 2026-01-15\n...",
  "fields": [
    {
      "key": "invoice_number",
      "value": "0001-00045678",
      "confidence": 0.98,
      "bounding_box": { "x0": 0.6, "y0": 0.05, "x1": 0.95, "y1": 0.10 }
    },
    {
      "key": "total_amount",
      "value": "1250.00",
      "confidence": 0.97,
      "bounding_box": { "x0": 0.7, "y0": 0.85, "x1": 0.95, "y1": 0.90 }
    }
  ],
  "tables": [],
  "engine_used": "claude-3-5-sonnet-20241022",
  "processing_time_ms": 1840.5
}
```

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Network                      │
│                                                         │
│  ┌──────────────┐     ┌──────────────────────────────┐  │
│  │  Demo Client │────▶│      API Core (Meta-GW)      │  │
│  │  (Streamlit) │     │  FastAPI + Pydantic + LiteLLM│  │
│  └──────────────┘     └──────────┬───────────────────┘  │
│                                  │                      │
│          ┌───────────────────────┼──────────────────┐   │
│          ▼                       ▼                  ▼   │
│  ┌──────────────┐  ┌─────────────────────┐  ┌──────────┐│
│  │  OCR Cloud   │  │  LLM Router (LiteLLM│  │  Worker  ││
│  │ AWS/GCP/Azure│  │  OpenAI/Anthropic/  │  │ SmolVLM2 ││
│  └──────────────┘  │  DeepSeek/Qwen/etc.)│  │  (local) ││
│                    └─────────────────────┘  └──────────┘│
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              DB / Cache (Redis / SQLite)          │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

Para más detalles, ver [plan.md](plan.md).

---

## Estructura del Proyecto

```
document_epic_extract/
├── api/                   ← FastAPI Core (Meta-Gateway)
│   ├── main.py
│   ├── routers/           ← /extract, /prebuilts, /registry
│   ├── schemas/           ← Pydantic models
│   ├── services/          ← Routing & template logic
│   └── core/              ← Config & exceptions
├── adapters/              ← Engine Adapters (OCR / LLM / Local)
├── prebuilts/             ← YAML templates (invoice, receipt, etc.)
├── registry/              ← models.yaml — dynamic model registry
├── demo/                  ← Streamlit Demo Client
├── docker/                ← Dockerfiles per service
├── docs/                  ← OpenAPI spec & guides
├── tests/                 ← Unit & integration tests
├── docker-compose.yml
├── pyproject.toml
├── CONTRIBUTING.md
├── plan.md                ← Full architecture & roadmap
└── README.md
```

---

## Motores Soportados

### OCR Cloud (Determinista)
| Proveedor | Adapter |
| :--- | :--- |
| AWS Textract | `adapters/ocr/aws.py` |
| Azure Document Intelligence | `adapters/ocr/azure.py` |
| GCP Document AI | `adapters/ocr/gcp.py` |

### LLMs (vía LiteLLM)
| Familia | Modelos Destacados |
| :--- | :--- |
| Anthropic | claude-3-5-sonnet, claude-3-7-sonnet, claude-opus-4 |
| OpenAI | gpt-4o, gpt-4.1, o3 |
| Google | gemini-2.0-flash, gemini-2.5-pro |
| DeepSeek | deepseek-v3, deepseek-r1 |
| Qwen | qwen2.5-vl-72b-instruct |
| Mistral | mistral-large, pixtral |
| + 90 modelos más via `registry/models.yaml` | |

### Modelos Locales
| Modelo | Adapter |
| :--- | :--- |
| SmolVLM2-2.2B-Instruct | `adapters/local/smolvlm2.py` |

---

## Prebuilts Disponibles

| ID | Descripción |
| :--- | :--- |
| `invoice` | Factura / Invoice |
| `receipt` | Boleta / Recibo |
| `id_card` | Documento de Identidad |
| `bank_statement` | Estado de Cuenta Bancario |
| `customs_declaration` | Declaración Aduanera |
| `custom` | Define tus propios campos vía API |

---

## Endpoints Principales

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/extract` | Extracción principal (enruta al motor elegido) |
| `GET` | `/prebuilts` | Lista de prebuilts disponibles |
| `POST` | `/prebuilts/custom` | Registrar un Custom Prebuilt |
| `GET` | `/registry/models` | Lista de modelos del registro dinámico |
| `GET` | `/health` | Health check |

Documentación interactiva disponible en `/docs` (Swagger UI) y `/redoc`.

---

## Desarrollo Local (sin Docker)

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -e ".[dev]"

# Ejecutar la API
uvicorn api.main:app --reload --port 8000

# Ejecutar el Demo
streamlit run demo/app.py
```

---

## Contribuir

¡Las contribuciones son bienvenidas! Lee [CONTRIBUTING.md](CONTRIBUTING.md) para saber cómo:

- Añadir un nuevo modelo al registro (`registry/models.yaml`).
- Crear un nuevo Engine Adapter.
- Proponer o mejorar un Prebuilt Template.
- Reportar bugs o solicitar features.

---

## Roadmap

Ver [plan.md](plan.md) para el plan completo de fases.

- **Fase 1** — Fundación: FastAPI core + Pydantic schemas *(en progreso)*
- **Fase 2** — Adaptadores OCR Cloud (AWS, GCP, Azure)
- **Fase 3** — Meta-Gateway LLM + LiteLLM + Prebuilt Engine
- **Fase 4** — Ejecución Local (SmolVLM2)
- **Fase 5** — Demo Front-end (Streamlit)
- **Fase 6** — Documentación & Open Source Release

---

## Licencia

Distribuido bajo licencia **MIT**. Ver [LICENSE](LICENSE) para más información.

---

*Construido con ❤️ por la comunidad — contributions welcome!*
