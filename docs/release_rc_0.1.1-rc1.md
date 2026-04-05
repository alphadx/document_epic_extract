# Release Candidate Log — v0.1.1-rc1

Fecha: **2026-04-05**  
Estado: **GO (RC aprobado)**

## 1) Ejecución de checklist (paso a paso)

### Pre-release técnico
- [x] `make release-readiness`
- [x] `ruff check .`
- [x] `pytest -q`
- [x] `make openapi-signature`
- [x] `git diff --exit-code tests/fixtures/openapi_signature.json`

### Revisión documental
- [x] README alineado con tramo de estabilización/release.
- [x] `docs/milestone_decisions.md` actualizado con evidencia del RC.
- [x] `CHANGELOG.md` actualizado con corte `0.1.1-rc1`.
- [x] Guías de release enlazadas desde README.

### Versionado y tag
- [x] Versión definida: `0.1.1-rc1`
- [x] `pyproject.toml` actualizado a `0.1.1rc1`
- [x] Tag anotado creado: `v0.1.1-rc1`

## 2) Decisión Go/No-Go

**Decisión:** GO para RC (`v0.1.1-rc1`).

Razones:
1. Quality gates en verde.
2. Snapshot OpenAPI consistente (sin diff).
3. Runbook/checklist de release disponible y trazable.

## 3) Riesgos residuales

- Publicación final en PyPI/TestPyPI sigue pendiente (fuera del corte RC).
- Falta validación con dataset ampliado multi-proveedor previo a release final.
- Se recomienda ventana corta de observación post-RC antes del tag estable.

## 4) Siguiente paso

Promover a release estable (`v0.1.1`) una vez completada la ventana de observación y decisión final de canal de publicación.
