# Changelog

Todos los cambios relevantes del proyecto se documentan en este archivo.

El formato está inspirado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el versionado sigue [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Added
- N/A.

### Changed
- N/A.

### Fixed
- N/A.

## [0.1.1] - 2026-04-05

### Added
- Evidencia de release estable documentada (`docs/release_v0.1.1.md`).

### Changed
- Promoción de versión desde `0.1.1rc1` a `0.1.1`.
- Consolidación de checklist de release con evidencia de build/twine.

### Fixed
- N/A.

## [0.1.1-rc1] - 2026-04-05

### Added
- Workflow dedicado de `release-readiness` para ejecución manual y por tags `v*`.
- Runbook de estabilización/release público y checklist de release OSS.

### Changed
- Versión del paquete actualizada a `0.1.1rc1` para corte de release candidate.
- Se formaliza gate único de pre-release: `make release-readiness`.

### Fixed
- N/A.

## [0.1.0] - 2026-04-05

### Added
- API base de extracción (`POST /extract`) con contrato unificado `StandardizedExtraction`.
- Adaptadores OCR cloud (AWS/GCP/Azure), ruta LLM con LiteLLM y adapter local SmolVLM2.
- Demo Streamlit con comparación side-by-side y visualización de resultados.

### Changed
- Gobernanza de contrato OpenAPI con snapshot y checks dedicados.

### Fixed
- Hardening incremental de errores y validaciones de payload en flujo demo/API.
