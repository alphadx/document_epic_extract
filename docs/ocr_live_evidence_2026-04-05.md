# Evidencia cloud OCR real — 2026-04-05

Reporte generado por `scripts/collect_ocr_live_evidence.py`.

## Matriz de preparación por proveedor

| Proveedor | Credenciales válidas | Timeout | Proveedor caído | Notas |
|---|---|---|---|---|
| AWS | SKIPPED | SKIPPED | SKIPPED | faltan: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION |
| GCP | SKIPPED | SKIPPED | SKIPPED | faltan: GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_PROCESSOR_ID |
| AZURE | SKIPPED | SKIPPED | SKIPPED | faltan: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY |

## Criterios para ejecutar pruebas live

1. Exportar credenciales reales por proveedor.
2. Confirmar conectividad saliente hacia SDKs cloud.
3. Ejecutar la suite live (manual controlado) y adjuntar resultados en PR.

## Estado

- Si una fila está en `SKIPPED`, ese escenario no tiene evidencia live en este entorno.
- Este reporte no reemplaza pruebas funcionales; sirve como bitácora operativa de preparación.
