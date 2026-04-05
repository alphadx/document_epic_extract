# Hito 7 — Registro de Riesgos Post-release

Fecha de creación: **2026-04-05**  
Owner: Equipo Core OmniExtract

## Objetivo
Mantener un registro corto, verificable y accionable de riesgos residuales después del release estable `v0.1.1`, con estado y decisión explícita para el cierre de Hito 7.

## Ventana de observación
- Inicio: **2026-04-05**
- Fin objetivo: **2026-04-12**
- Cobertura: API (`/extract`), demo Streamlit y provider local (`worker /infer`).

## Riesgos activos

| ID | Riesgo | Severidad | Estado | Mitigación | Criterio de cierre |
| --- | --- | --- | --- | --- | --- |
| R7-01 | Regresión de contrato API no detectada en consumo real | Alta | Abierto | Ejecutar `make release-readiness` y revisar snapshot OpenAPI antes de cerrar hito | Sin drift de contrato + checks en verde |
| R7-02 | Decisión de canal PyPI/TestPyPI indefinida | Media | Mitigado | Decisión de diferimiento documentada + preflight técnico en `make publish-testpypi-preflight` para validar credenciales/artefactos antes de upload | Decisión aprobada y documentada |
| R7-03 | Publicación de paquete sin validación de artefactos | Media | Mitigado | Ejecutados `python -m build` y `twine check dist/*`; metadata de licencia ajustada para build limpio; evidencia en `docs/hito7_packaging_validation.md` | Build + twine en verde con evidencia |
| R7-04 | Falsa señal de calidad por entorno de tests async inconsistente | Baja | Mitigado | Fallback async en `tests/conftest.py` + ejecución `pytest -q` | Suite reproducible en entorno mínimo |

## Evidencia de avance actual
- `ruff check .` en verde.
- `pytest -q` en verde.
- Fallback async incorporado en `tests/conftest.py` para entornos sin plugin async.

## Próxima actualización
Actualizar este registro al finalizar la ventana de observación o ante evento crítico, lo que ocurra primero.
