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
| R7-01 | Regresión de contrato API no detectada en consumo real | Alta | Abierto (en observación) | Ejecutar gates diarios A/B en ventana 2026-04-06 a 2026-04-12 y registrar evidencia en `docs/hito7_r701_observability_log.md` | **Cerrado solo si** existen corridas periódicas completas en la ventana definida y no hay evidencia de drift contractual en consumo real; en caso contrario, **Abierto (con extensión)** + nueva fecha objetivo |
| R7-02 | Decisión de canal PyPI/TestPyPI indefinida | Media | Mitigado | Decisión de diferimiento documentada + preflight técnico en `make publish-testpypi-preflight` para validar credenciales/artefactos antes de upload | Decisión aprobada y documentada |
| R7-03 | Publicación de paquete sin validación de artefactos | Media | Mitigado | Ejecutados `python -m build` y `twine check dist/*`; metadata de licencia ajustada para build limpio; evidencia en `docs/hito7_packaging_validation.md` | Build + twine en verde con evidencia |
| R7-04 | Falsa señal de calidad por entorno de tests async inconsistente | Baja | Mitigado | Fallback async en `tests/conftest.py` + ejecución `pytest -q` | Suite reproducible en entorno mínimo |


## Evidencia vinculada (R7-01)
- Bitácora diaria de observabilidad: `docs/hito7_r701_observability_log.md`
- Gate A: `make release-readiness` (alternativa: `scripts/release_readiness.sh`)
- Gate B: `pytest -q tests/integration/test_openapi_contract.py tests/integration/test_openapi_signature_snapshot.py` + snapshot OpenAPI sin diff

## Evidencia de avance actual
- Snapshot de observación R7-01 al 2026-04-06 (UTC): **1 AUTO-RUNS (raw), 1/7 días cubiertos (última corrida por día)**, drift detectado: 0.
- `ruff check .` en verde.
- `pytest -q` en verde.
- Fallback async incorporado en `tests/conftest.py` para entornos sin plugin async.

## Próxima actualización
Actualizar este registro al finalizar la ventana de observación o ante evento crítico, lo que ocurra primero.
