# plan.md: Documento de Arquitectura y Plan Maestro para OmniExtract Gateway

**Estado:** Borrador Inicial  
**Rol:** Arquitectura Central y Abstracción de Datos  
**Licencia Propuesta:** MIT o Apache 2.0 (Alineado a la filosofía Open Source)

---

## 1. Visión General del Proyecto

**OmniExtract Gateway** es un meta-gateway de extracción documental unificado, contenerizado y de código abierto. Su propósito es abstraer la complejidad de extraer datos estructurados (texto, pares clave-valor, tablas y coordenadas) de imágenes o documentos, utilizando un único punto de entrada (API).

El gateway trata a proveedores deterministas (AWS Textract, Azure Document Intelligence, GCP Document AI), modelos locales (SmolVLM2) y una extensa red de LLMs comerciales y de código abierto como **"Motores de Inferencia Intercambiables"**. El núcleo del sistema es agnóstico al motor; su responsabilidad es enrutar, inyectar contexto (mediante plantillas *prebuilt*) y estandarizar la salida en un esquema JSON predecible.

### Estado de Hitos (resumen)

- **Hito 0 (Kickoff de repositorio):** base legal y editorial del proyecto (licencia OSS, README/CONTRIBUTING y lineamientos iniciales).
- **Hito 1+:** implementación incremental de API core, adaptadores y demo.

---

## 2. Arquitectura del Sistema (Docker & Topología)

El sistema se distribuye en una arquitectura de microservicios orientada a contenedores, separando la carga de red de la carga de cómputo.

### 2.1. Contenedores Principales

| Contenedor | Descripción | Tecnologías Base |
| :--- | :--- | :--- |
| **API Core (Meta-Gateway)** | Siempre en ejecución. Recibe peticiones, valida *api keys*, enruta llamadas a la nube o a los nodos locales, y estandariza las respuestas. | FastAPI, Pydantic, LiteLLM (como router subyacente de LLMs). |
| **Motor Local (Worker)** | Opcional. Ejecuta modelos que requieren GPU/CPU intensiva (Ej: SmolVLM2, flan-t5). Separado de la API para evitar bloqueos por carga térmica/memoria. | vLLM o Hugging Face Inference Endpoints (vía Docker). |
| **Demo Client** | Aplicación cliente interactiva. Genera los *inputs*, muestra los resultados, y permite gestionar el estado del arte de las conexiones. | Streamlit o Gradio. |
| **DB / Cache** | Almacenamiento ligero para los *prompts* personalizados de los "Documentos Prebuilt" y caché de respuestas para evitar sobrecostes. | Redis / SQLite. |

### 2.2. Diagrama de Topología

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

---

## 3. Diseño de la Interfaz y Abstracción (API Core)

Para que el gateway sea verdaderamente agnóstico, se implementa el patrón de diseño **Adapter** y **Factory**. El usuario o cliente interactúa con una única interfaz, y el gateway decide cómo traducir esa petición.

### 3.1. Esquemas de Datos Unificados (Pydantic Models)

El contrato de salida debe ser estricto. Un LLM probabilístico y un OCR determinista deben devolver el mismo objeto.

#### Modelo de Entrada (`ExtractionRequest`)

```python
class EngineConfig(BaseModel):
    provider: Literal["aws", "gcp", "azure", "local", "llm_router"]
    model: str                          # e.g. "anthropic.claude-3-sonnet-20240229-v1:0"
    api_keys: dict[str, str] = {}       # credentials injected per session

class ExtractionTarget(BaseModel):
    document_type: str                  # e.g. "invoice", "receipt", "custom_table"
    custom_fields: list[str] | None = None

class ExtractionRequest(BaseModel):
    document: str                       # Base64-encoded image or URL
    engine_config: EngineConfig
    extraction_target: ExtractionTarget
```

#### Modelo de Salida (`StandardizedExtraction`)

```python
class BoundingBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float

class ExtractedField(BaseModel):
    key: str
    value: str
    confidence: float | None = None
    bounding_box: BoundingBox | None = None

class TableCell(BaseModel):
    row: int
    col: int
    value: str
    bounding_box: BoundingBox | None = None

class ExtractedTable(BaseModel):
    rows: int
    cols: int
    cells: list[TableCell]

class StandardizedExtraction(BaseModel):
    raw_text: str
    fields: list[ExtractedField]
    tables: list[ExtractedTable]
    engine_used: str
    processing_time_ms: float | None = None
```

### 3.2. Adaptadores de Motor (*Engine Adapters*)

Se crean interfaces abstractas que cada motor debe cumplir:

1. **OCR Adapter** — Traduce la salida propietaria de AWS/GCP/Azure al esquema `StandardizedExtraction`.
2. **LLM Vision Adapter** — Utiliza **LiteLLM** para enrutar la petición al modelo correspondiente (OpenAI, Anthropic, DeepSeek, Qwen, Mistral, Docling, etc.). El desafío es forzar al LLM a devolver coordenadas mediante el *Prebuilt Template Engine*.
3. **Local Adapter** — Envía la imagen y el tensor al contenedor *Worker* y formatea la salida de modelos como SmolVLM2.

```
adapters/
├── base.py           ← BaseAdapter ABC
├── ocr/
│   ├── aws.py        ← AWSTextractAdapter
│   ├── gcp.py        ← GCPDocumentAIAdapter
│   └── azure.py      ← AzureDocIntelligenceAdapter
├── llm/
│   └── litellm_adapter.py  ← LiteLLMVisionAdapter
└── local/
    └── smolvlm2.py   ← SmolVLM2Adapter
```

---

## 4. Motor de Plantillas (Prebuilt Management)

Los OCRs clásicos tienen endpoints como `/prebuilt/invoice`. Para emular esto en los LLMs, el gateway implementa un **Motor de Inyección de Contexto**.

### 4.1. Funcionamiento del "Prebuilt" para LLMs

Cuando el cliente selecciona un documento prebuilt y elige un motor LLM, el API Core:

1. Busca en su biblioteca interna (o base de datos de usuario) la plantilla (ej. `invoice.yaml`).
2. El archivo YAML contiene el **System Prompt** maestro diseñado para forzar salidas JSON estructuradas y solicitar inferencia de coordenadas espaciales si el modelo de visión lo soporta (Qwen2.5-VL, Llama-3.2-Vision, etc.).
3. Ensambla el payload final: `[System Prompt] + [JSON Schema] + [Imagen]`.

#### Estructura de un Prebuilt (YAML)

```yaml
# prebuilts/invoice.yaml
id: invoice
display_name: "Factura / Invoice"
version: "1.0"
system_prompt: |
  You are a specialized document extraction engine. Extract all fields from the
  invoice image and return a JSON object strictly conforming to the schema below.
  For each field, provide the value and, if the model supports spatial reasoning,
  include bounding_box coordinates normalized to [0,1].
required_fields:
  - invoice_number
  - issue_date
  - due_date
  - vendor_name
  - vendor_address
  - total_amount
  - tax_amount
  - line_items
output_schema: "StandardizedExtraction"
```

### 4.2. Personalización Abierta (Custom Prebuilts)

El gateway permite registrar "Custom Prebuilts" vía API. Un desarrollador puede definir qué campos exactos busca (ej. `["patente_vehiculo", "fecha_siniestro"]`) y el gateway autogenerará el prompt óptimo, guardándolo en el catálogo persistente.

```
prebuilts/
├── invoice.yaml
├── receipt.yaml
├── id_card.yaml
├── bank_statement.yaml
├── customs_declaration.yaml
└── custom/         ← user-defined prebuilts (persisted via DB)
```

---

## 5. Integración del "Estado del Arte" (Soporte de Modelos)

### 5.1. Gestión Centralizada vía LiteLLM

Se delega la normalización de la API HTTP (retries, timeouts, mapeo de roles) a LiteLLM, integrado como sub-módulo dentro del API Core.

### 5.2. Registro Dinámico (Model Registry)

La lista de modelos permitidos no está *hardcodeada*. Se define en `registry/models.yaml`. Esto permite que la comunidad actualice endpoints mediante Pull Requests.

```yaml
# registry/models.yaml (extracto)
providers:
  anthropic:
    models:
      - id: claude-3-5-sonnet-20241022
        vision: true
        context_window: 200000
      - id: claude-3-7-sonnet-20250219
        vision: true
        context_window: 200000
  openai:
    models:
      - id: gpt-4o
        vision: true
        context_window: 128000
      - id: gpt-4.1
        vision: true
        context_window: 1000000
  google:
    models:
      - id: gemini-2.0-flash
        vision: true
        context_window: 1000000
  deepseek:
    models:
      - id: deepseek-v3
        vision: false
        context_window: 64000
  qwen:
    models:
      - id: qwen2.5-vl-72b-instruct
        vision: true
        context_window: 128000
  local:
    models:
      - id: smolvlm2-2.2b-instruct
        vision: true
        requires_gpu: false
```

### 5.3. Endpoint Personalizado (BYOE — Bring Your Own Endpoint)

El Demo y la API permiten introducir un modelo y endpoint personalizados no incluidos en la lista oficial, garantizando compatibilidad futura.

---

## 6. Aplicación Cliente: El Demo (Showcase)

### 6.1. Flujo del Usuario

1. Sube un documento (PDF/Imagen).
2. Selecciona el *Target* (Prebuilt Invoice, Tabla, Documento Libre).
3. Abre un panel de comparación: selecciona AWS Textract en Columna A y `qwen2.5-vl-72b-instruct` en Columna B.
4. Introduce sus API Keys temporalmente en la sesión del Demo.
5. Ejecuta y compara resultados.

### 6.2. Visualización

El Demo dibuja las *bounding boxes* (coordenadas) superpuestas en la imagen original, demostrando que ambos motores — a pesar de ser de naturalezas distintas — devuelven el esquema JSON unificado que la interfaz puede renderizar.

```
demo/
├── app.py              ← Streamlit / Gradio entrypoint
├── components/
│   ├── uploader.py     ← Document uploader component
│   ├── engine_selector.py
│   ├── bbox_renderer.py
│   └── comparison_panel.py
└── requirements.txt
```

---

## 7. Estructura del Repositorio (Skeleton)

```
document_epic_extract/
├── api/                        ← FastAPI Core (Meta-Gateway)
│   ├── main.py                 ← FastAPI app entrypoint
│   ├── routers/
│   │   ├── extract.py          ← POST /extract endpoint
│   │   ├── prebuilts.py        ← GET/POST /prebuilts endpoints
│   │   └── registry.py         ← GET /registry/models endpoint
│   ├── schemas/
│   │   ├── request.py          ← ExtractionRequest, EngineConfig, ExtractionTarget
│   │   └── response.py         ← StandardizedExtraction, ExtractedField, etc.
│   ├── services/
│   │   ├── router_service.py   ← Engine selection & routing logic
│   │   └── prebuilt_service.py ← Template lookup & prompt assembly
│   └── core/
│       ├── config.py           ← Settings (env vars via pydantic-settings)
│       └── exceptions.py       ← Custom HTTP exceptions
│
├── adapters/                   ← Engine Adapters
│   ├── base.py                 ← BaseAdapter ABC
│   ├── ocr/
│   │   ├── aws.py
│   │   ├── gcp.py
│   │   └── azure.py
│   ├── llm/
│   │   └── litellm_adapter.py
│   └── local/
│       └── smolvlm2.py
│
├── prebuilts/                  ← Prebuilt document templates
│   ├── invoice.yaml
│   ├── receipt.yaml
│   ├── id_card.yaml
│   ├── bank_statement.yaml
│   └── customs_declaration.yaml
│
├── registry/                   ← Model Registry
│   └── models.yaml
│
├── demo/                       ← Demo Client (Streamlit)
│   ├── app.py
│   ├── components/
│   └── requirements.txt
│
├── docker/                     ← Docker service configs
│   ├── api.Dockerfile
│   ├── worker.Dockerfile
│   └── demo.Dockerfile
│
├── docs/                       ← Documentation
│   ├── openapi.md
│   └── adding_models.md
│
├── tests/                      ← Test suite
│   ├── unit/
│   └── integration/
│
├── docker-compose.yml
├── pyproject.toml
├── CONTRIBUTING.md
├── README.md
└── plan.md
```

---

## 8. Plan de Ejecución y Milestones

### Fase 0 — Kickoff, Análisis y Base del Repositorio (Cierre requerido)
- [x] Licencia OSS explícita en el repositorio (`LICENSE`).
- [x] Roadmap visible con fases/hitos en `README.md`.
- [x] Documento de arquitectura inicial (`plan.md`) con alcance general.
- [x] Guía de contribución base (`CONTRIBUTING.md`).
- [x] **Definition of Done (DoD) de Hito 0** documentada y validada por el equipo.
- [x] **Análisis de seguridad inicial** documentado (amenazas, controles mínimos y límites de esta fase).

### Fase 1 — Fundación y Core
- [x] Configuración del repositorio y Docker Compose base.
- [x] Definición estricta de los esquemas Pydantic (`StandardizedExtraction`).
- [x] Endpoint `POST /extract` funcional con respuesta mock.
- [x] CI/CD básico (GitHub Actions: lint + tests).

### Fase 2 — Adaptadores Deterministas
- [ ] Implementación del `AWSTextractAdapter`.
- [ ] Implementación del `GCPDocumentAIAdapter`.
- [ ] Implementación del `AzureDocIntelligenceAdapter`.
- [ ] Mapeo de salidas propietarias al esquema unificado.
- [ ] Tests de integración contra las APIs de nube (mocked).

### Fase 3 — Meta-Gateway LLM & LiteLLM
- [ ] Integración de LiteLLM como router subyacente.
- [ ] Implementación del `LiteLLMVisionAdapter`.
- [ ] Motor de plantillas dinámicas (*Prebuilt Template Engine*).
- [ ] Pruebas de ingeniería de prompts con modelos clave (Claude 3.5 Sonnet, GPT-4o, Qwen-VL).
- [ ] Registro dinámico de modelos (`registry/models.yaml`).

### Fase 4 — Ejecución Local
- [ ] Contenerización de SmolVLM2.
- [ ] Implementación del `SmolVLM2Adapter`.
- [ ] Configuración de colas de tareas ligeras (Celery/Redis) para inferencia asíncrona.

### Fase 5 — Demo Front-end
- [ ] Construcción de la interfaz Streamlit/Gradio.
- [ ] Panel de comparación side-by-side.
- [ ] Visualizador de bounding boxes.
- [ ] Gestión segura de API keys en la sesión.

### Fase 6 — Documentación y Open Source
- [ ] Redacción de `CONTRIBUTING.md`.
- [ ] Especificación OpenAPI/Swagger completa.
- [ ] Guía para agregar nuevos modelos al *registry*.
- [ ] Guía para crear Custom Prebuilts.
- [ ] Publicación en PyPI (opcional).

---

## 9. Decisiones Técnicas Clave

| Decisión | Alternativas Consideradas | Justificación |
| :--- | :--- | :--- |
| **LiteLLM como router LLM** | Haystack, LangChain, implementación propia | LiteLLM tiene soporte nativo para 100+ modelos, manejo de rate limits y es ligero. |
| **FastAPI** | Flask, Django REST | Tipado nativo con Pydantic, async nativo, generación automática de OpenAPI. |
| **Pydantic v2** | Marshmallow, dataclasses | Validación de alto rendimiento, integración perfecta con FastAPI. |
| **YAML para prebuilts** | JSON, TOML, DB-only | Legible por humanos, fácil de editar por la comunidad via PR. |
| **Docker Compose** | Kubernetes, Docker Swarm | Simplicidad para desarrollo local y despliegues small-scale. |
| **Redis para caché** | Memcached, SQLite | Soporte nativo para TTL, estructuras de datos complejas y pub/sub para colas. |

---

## 10. Seguridad Inicial (Hito 0 — Análisis)

### 10.1. Objetivo de seguridad en esta fase

Definir una base de seguridad mínima para desarrollo y colaboración, sin introducir todavía controles de infraestructura avanzados (WAF, KMS multi-tenant, SIEM completo).

### 10.2. Superficie de riesgo identificada

- Exposición accidental de API keys en commits, logs o capturas de pantalla.
- Uso de credenciales de alto privilegio en entornos de desarrollo.
- Inyección de prompts no controlados en templates custom.
- Fuga de datos sensibles en payloads de pruebas/documentación.

### 10.3. Controles mínimos exigidos para cerrar Hito 0

- No versionar secretos en git (`.env` fuera de control de versiones).
- Uso de credenciales separadas por entorno (dev/stage/prod) y de privilegio mínimo.
- Documentar manejo temporal de API keys en demo/sesión (sin persistencia duradera).
- Evitar registrar documentos completos o secretos en logs de aplicación por defecto.
- Declarar explícitamente que este hito es de análisis y baseline documental (no hardening total).

### 10.4. Fuera de alcance de Hito 0

- Rotación automatizada de secretos.
- Cifrado de datos en reposo con gestión centralizada de llaves.
- Auditoría centralizada y alerting de seguridad en tiempo real.

### 10.5. Criterio de salida hacia Fase 1

Solo avanzar a Fase 1 cuando el equipo confirme que esta sección sigue vigente y que no hay bloqueantes de seguridad básica para desarrollo.

---

*Última actualización: 2026-04-04 — Fase de Diseño Inicial*
