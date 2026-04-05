# Hito 6 — Checklist de ejecución y cierre (Documentación & Open Source)

Estado: **Cerrado (operativo)**  
Última actualización: **2026-04-05 (cierre documental)**

## Objetivo del hito
Cerrar la capa de documentación y release open source para que cualquier contribuidor pueda instalar, operar, extender y publicar el proyecto con mínima fricción.

## Alcance obligatorio (DoD de Hito 6)

### 1) Gobernanza y contribución OSS
- [x] `CONTRIBUTING.md` actualizado y alineado con flujo de PRs.
- [x] Regla de decisiones por hito documentada en `docs/milestone_decisions.md`.
- [x] Checklist de release OSS (pre-release, tagging, changelog, smoke checks).

### 2) Contrato API y documentación técnica
- [x] Especificación OpenAPI/Swagger documentada (`docs/openapi.md` + `/docs` runtime).
- [x] Snapshot del contrato API versionado y verificable por CI.
- [x] Guía de versionado de contrato (qué cambia en minor vs major).

### 3) Extensibilidad del gateway
- [x] Guía para agregar modelos al registry (`docs/adding_models.md`).
- [x] Guía de demo y troubleshooting publicada (`docs/demo_troubleshooting.md`).
- [x] Guía para crear Custom Prebuilts en `docs/`.

### 4) Validación de cierre
- [x] Quality gates en verde (`ruff check .`, `pytest -q`).
- [x] README reflejando estado final de Hito 6 y siguientes pasos.
- [x] Registro de decisiones de cierre en `docs/milestone_decisions.md`.

## Riesgos abiertos
- Publicación en PyPI sigue siendo opcional y dependerá de estrategia de distribución.
- Conviene incorporar validaciones con datasets reales antes de un release público amplio.

## Criterio para avanzar al siguiente hito
Hito 6 se considera cerrado cuando la documentación permita operar/extender/publicar el proyecto end-to-end y exista un proceso de release reproducible con evidencia de checks de calidad.

## Evidencia de cierre
- Guías añadidas: `docs/custom_prebuilts.md`, `docs/release_checklist.md`, `docs/contract_versioning.md`.
- Quality gates validados en verde (`ruff check .`, `pytest -q`).
