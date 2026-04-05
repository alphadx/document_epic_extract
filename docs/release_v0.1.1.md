# Release Log — v0.1.1 (estable)

Fecha: **2026-04-05**  
Estado: **GO (release estable aprobado)**

## 1) Verificaciones ejecutadas

- [x] `make release-readiness`
- [x] `python -m build`
- [x] `twine check dist/*`
- [x] tag anotado `v0.1.1`

## 2) Decisión

Se promueve `v0.1.1` como release estable al cumplirse:
1. gate de calidad en verde;
2. snapshot OpenAPI sin drift;
3. artefactos de build válidos para distribución.

## 3) Riesgos residuales

- Publicación a TestPyPI/PyPI depende de estrategia final de credenciales/canal.
- Se recomienda monitoreo corto post-release para feedback de integradores.

## 4) Trazabilidad

- RC previo: `docs/release_rc_0.1.1-rc1.md`.
- Checklist de release: `docs/release_checklist.md`.
