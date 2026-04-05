# Corrida live controlada OCR — 2026-04-05

Generado: 2026-04-05T08:14:25Z
API base: `http://127.0.0.1:8000`

| Proveedor | Escenario | Estado | HTTP | Detalle |
|---|---|---|---|---|
| AWS | valid_credentials | SKIPPED | - | missing credentials: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION |
| AWS | invalid_credentials | MANUAL_REQUIRED | - | aws invalid credentials must be injected in API runtime env |
| AWS | timeout | MANUAL_REQUIRED | - | set OCR_AWS_TIMEOUT_DOC_URL to run this scenario |
| AWS | provider_down | MANUAL_REQUIRED | - | set OCR_AWS_PROVIDER_DOWN_DOC_URL to run this scenario |
| GCP | valid_credentials | SKIPPED | - | missing credentials: GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_PROCESSOR_ID |
| GCP | invalid_credentials | ERROR | - | request_error: [Errno 111] Connection refused |
| GCP | timeout | MANUAL_REQUIRED | - | set OCR_GCP_TIMEOUT_DOC_URL to run this scenario |
| GCP | provider_down | MANUAL_REQUIRED | - | set OCR_GCP_PROVIDER_DOWN_DOC_URL to run this scenario |
| AZURE | valid_credentials | SKIPPED | - | missing credentials: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY |
| AZURE | invalid_credentials | ERROR | - | request_error: [Errno 111] Connection refused |
| AZURE | timeout | MANUAL_REQUIRED | - | set OCR_AZURE_TIMEOUT_DOC_URL to run this scenario |
| AZURE | provider_down | MANUAL_REQUIRED | - | set OCR_AZURE_PROVIDER_DOWN_DOC_URL to run this scenario |

## Nota

- `MANUAL_REQUIRED` indica que falta configuración controlada para simular timeout/proveedor caído.
- `SKIPPED` indica credenciales ausentes para ejecutar live con proveedor real.
