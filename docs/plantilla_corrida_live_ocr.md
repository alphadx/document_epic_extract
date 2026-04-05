# Plantilla de corrida live controlada — OCR cloud (AWS/GCP/Azure)

Fecha base: 2026-04-05  
Owner sugerido: Equipo Core OmniExtract (API/Plataforma)

> Objetivo: ejecutar y evidenciar de forma controlada los escenarios **credenciales válidas**, **timeout** y **proveedor caído** por proveedor cloud, sin ambigüedad de configuración.

## 1) Pre-flight (obligatorio)

- [ ] API levantada localmente (`uvicorn api.main:app --host 0.0.0.0 --port 8000`).
- [ ] Dependencias cloud instaladas para provider bajo prueba.
- [ ] Conectividad saliente validada.
- [ ] Documento de prueba disponible en base64 (PDF o imagen soportada).

## 2) Variables de entorno mínimas

## 2.1 AWS (Textract)

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
```

## 2.2 GCP (Document AI)

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/service-account.json"
export GCP_PROJECT_ID="..."
export GCP_LOCATION="us"
export GCP_PROCESSOR_ID="..."
```

## 2.3 Azure (Document Intelligence)

```bash
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://<resource>.cognitiveservices.azure.com/"
export AZURE_DOCUMENT_INTELLIGENCE_KEY="..."
```

## 3) Payload base

```bash
export DOC_B64="<documento_en_base64>"
```

## 4) Corrida por proveedor

> Reemplaza `<API_BASE>` por `http://127.0.0.1:8000` (o tu endpoint).

## 4.1 Escenario A — Credenciales válidas (esperado: 200)

### AWS
```bash
curl -sS -X POST "<API_BASE>/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "document":"'"$DOC_B64"'",
    "engine_config":{"provider":"aws","model":"textract","api_keys":{}},
    "extraction_target":{"document_type":"invoice"}
  }'
```

### GCP
```bash
curl -sS -X POST "<API_BASE>/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "document":"'"$DOC_B64"'",
    "engine_config":{"provider":"gcp","model":"docai","api_keys":{}},
    "extraction_target":{"document_type":"invoice"}
  }'
```

### Azure
```bash
curl -sS -X POST "<API_BASE>/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "document":"'"$DOC_B64"'",
    "engine_config":{
      "provider":"azure",
      "model":"prebuilt-invoice",
      "api_keys":{
        "azure_endpoint":"'"$AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"'",
        "azure_key":"'"$AZURE_DOCUMENT_INTELLIGENCE_KEY"'"
      }
    },
    "extraction_target":{"document_type":"invoice"}
  }'
```

## 4.2 Escenario B — Timeout controlado (esperado: 502 + "timeout")

- Forzar timeout en entorno/red (por ejemplo mediante política de red o endpoint deliberadamente no alcanzable).
- Repetir llamadas del escenario A y registrar:
  - timestamp,
  - proveedor,
  - latencia observada,
  - mensaje de error devuelto.

## 4.3 Escenario C — Proveedor caído (esperado: 502 + "provider error")

- Ejecutar durante incidente real/simulado de indisponibilidad upstream.
- Repetir llamadas del escenario A y registrar:
  - código HTTP,
  - detalle devuelto,
  - duración de falla,
  - acción de mitigación aplicada.

## 4.4 Escenario D — Credenciales inválidas (esperado: 502 + "authentication error")

- Invalidar temporalmente credenciales (entorno de test) y repetir escenario A.
- Confirmar mensaje normalizado por proveedor.

## 5) Evidencia requerida por corrida

Adjuntar en PR o acta:

- [ ] Comandos ejecutados (copy/paste).
- [ ] Respuestas JSON (redactadas si contienen datos sensibles).
- [ ] Fecha/hora UTC de cada prueba.
- [ ] Resultado por proveedor y escenario.
- [ ] Riesgos encontrados + acción correctiva.

## 6) Tabla de resultados (rellenable)

| Fecha UTC | Proveedor | Escenario | HTTP | Resultado | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| YYYY-MM-DDTHH:MM:SSZ | AWS | Credenciales válidas | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AWS | Timeout | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AWS | Proveedor caído | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AWS | Credenciales inválidas | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | GCP | Credenciales válidas | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | GCP | Timeout | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | GCP | Proveedor caído | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | GCP | Credenciales inválidas | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AZURE | Credenciales válidas | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AZURE | Timeout | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AZURE | Proveedor caído | 200/502 | Pass/Fail | enlace/log | ... |
| YYYY-MM-DDTHH:MM:SSZ | AZURE | Credenciales inválidas | 200/502 | Pass/Fail | enlace/log | ... |

## 7) Criterio de cierre del pendiente cloud real

Se puede marcar como cerrado cuando:
- cada proveedor tenga evidencia en los 4 escenarios,
- errores estén normalizados (auth/timeout/provider),
- exista trazabilidad en `docs/hito2_cierre_operativo.md` y `TODO.md`.
