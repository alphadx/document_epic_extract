# OmniExtract Gateway

> Extrae datos estructurados de documentos con una sola API, cambiando de motor (OCR cloud, LLM o modelos locales) sin reescribir tu integración.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)

## TL;DR

- **Qué resuelve:** API unificada (`POST /extract`) para OCR + LLM + local worker.
- **Por qué importa:** evita lock-in y entrega un JSON estándar (`StandardizedExtraction`).
- **Cómo arrancar:** modo **rápido** con Docker o modo **lento/controlado** paso a paso.
- **Transparencia:** este README separa lo que ya está validado de la deuda técnica pendiente.

## ¿Qué tiene de bueno? (bondades)

- **Sin lock-in de proveedor:** AWS/Azure/GCP, LiteLLM y modelos locales detrás del mismo contrato.
- **Contrato de salida único:** misma estructura de respuesta para motores deterministas o probabilísticos.
- **Extensible por configuración:** catálogo de modelos (`registry/models.yaml`) y prebuilts YAML.
- **Listo para demo y dev local:** FastAPI + Streamlit + docker compose.

## Estado verificado (2026-04-05)

Se ejecutaron checks locales y están en verde:

- `ruff check .`
- `pytest -q`
- `make release-readiness` (incluye firma OpenAPI y verificación de snapshot)

> Esto valida calidad de código, suite automatizada y estabilidad del contrato OpenAPI en el estado actual del repo.

## Lo que sí hace hoy

- Endpoint unificado de extracción (`/extract`) con router por proveedor/modelo.
- Endpoints de catálogo (`/registry/models`) y prebuilts (`/prebuilts`, `POST /prebuilts/custom`).
- Adaptadores OCR cloud (AWS/GCP/Azure), LLM vía LiteLLM y worker local.
- Demo de comparación visual y flujo end-to-end en local.

## Deuda técnica abierta (honesta y explícita)

Estas tareas **no se marcan como hechas** hasta tener evidencia operativa:

1. **Circuit breaker distribuido multi-réplica**
   - Estado actual: política definida, implementación distribuida aún incremental.
   - Falta: store Redis activo + pruebas de concurrencia + métricas/runbook cerrados.
2. **Observación post-release de riesgos residuales**
   - Estado actual: riesgo R7-01 todavía abierto en registro de riesgos.
   - Falta: cerrar ventana de observación con evidencia sostenida de no-regresión en consumo real.
3. **Decisión final de publicación de paquete**
   - Estado actual: publicación diferida (no publicar aún).
   - Falta: reevaluación en fecha comprometida y ejecución (o nuevo diferimiento documentado).

Ver backlog vivo y deuda técnica: [`TODO.md`](TODO.md).

## Comenzar rápido (modo recomendado)

```bash
git clone https://github.com/alphadx/document_epic_extract.git
cd document_epic_extract
cp .env.example .env
# editar .env con tus credenciales

docker compose up -d
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Demo: http://localhost:8501

## Comenzar lento (modo controlado, paso a paso)

Ideal para entender cada componente y depurar:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Terminal 1 (API):

```bash
source .venv/bin/activate
uvicorn api.main:app --reload --port 8000
```

Terminal 2 (Demo):

```bash
source .venv/bin/activate
streamlit run demo/app.py
```

Luego valida con:

```bash
ruff check .
pytest -q
make release-readiness
```

## Documentación

- Portal docs: [`docs/README.md`](docs/README.md)
- Getting Started detallado: [`docs/getting_started.md`](docs/getting_started.md)
- Arquitectura y roadmap: [`plan.md`](plan.md)
- Avances por hitos: [`docs/hitos_avances.md`](docs/hitos_avances.md)
- TODO + deuda técnica: [`TODO.md`](TODO.md)

## Contribuir

Consulta [`CONTRIBUTING.md`](CONTRIBUTING.md) para guías de contribución.
