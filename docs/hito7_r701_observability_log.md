# Hito 7 — R7-01 Observability Log (2026-04-06 a 2026-04-12)

Fecha de creación: **2026-04-06**  
Riesgo asociado: **R7-01 — Regresión de contrato API no detectada en consumo real**  
Referencia: `docs/hito7_risk_register.md`

## Objetivo
Registrar evidencia diaria sin gaps durante la ventana **2026-04-06** a **2026-04-12 (UTC)** con dos gates fijos:

- **Gate A (release readiness):** `make release-readiness` (alternativa operativa válida: `scripts/release_readiness.sh`).
- **Gate B (contrato en consumo real):** verificación del contrato consumido vs estado esperado del release mediante:
  - `pytest -q tests/integration/test_openapi_contract.py tests/integration/test_openapi_signature_snapshot.py`
  - `python scripts/generate_openapi_signature.py`
  - `git diff --exit-code tests/fixtures/openapi_signature.json`

## Plan de observación diaria (UTC)

| Fecha | Ventana sugerida (UTC) | Gate A | Gate B | Entregable diario | Regla de decisión |
| --- | --- | --- | --- | --- | --- |
| 2026-04-06 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia completa | Drift => incidente severidad alta; sin drift => continuar |
| 2026-04-07 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia completa | Drift => incidente severidad alta; sin drift => continuar |
| 2026-04-08 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia completa | Drift => incidente severidad alta; sin drift => continuar |
| 2026-04-09 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia completa | Drift => incidente severidad alta; sin drift => continuar |
| 2026-04-10 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia completa | Drift => incidente severidad alta; sin drift => continuar |
| 2026-04-11 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia completa | Drift => incidente severidad alta; sin drift => continuar |
| 2026-04-12 | 00:00–23:59 | `make release-readiness` | contrato + snapshot + diff sin cambios | Fila de evidencia + corte final | Drift => incidente severidad alta; sin drift => evaluar cierre |

## Plantilla de evidencia diaria

| Fecha/hora UTC | Commit SHA evaluado | Resultado Gate A (pass/fail + resumen) | Resultado Gate B (drift/no drift + endpoint afectado si aplica) | Decisión del día (continuar observación / abrir incidente / escalar) |
| --- | --- | --- | --- | --- |
| 2026-04-06T00:23:15Z | `c4466186469b4cb9d37478966abc98d145a7c01d` | **PASS** — `make release-readiness`: `ruff check .` OK, `pytest -q` 94 passed, consistency check OK, snapshot OpenAPI actualizado sin diff pendiente. | **NO DRIFT** — contratos en consumo real validados (`test_openapi_contract` + `test_openapi_signature_snapshot`: 6 passed); endpoint afectado: N/A. | **Continuar observación** |
| 2026-04-07 | _pendiente (ejecutar en fecha real)_ | _pendiente_ | _pendiente_ | _pendiente_ |
| 2026-04-08 | _pendiente (ejecutar en fecha real)_ | _pendiente_ | _pendiente_ | _pendiente_ |
| 2026-04-09 | _pendiente (ejecutar en fecha real)_ | _pendiente_ | _pendiente_ | _pendiente_ |
| 2026-04-10 | _pendiente (ejecutar en fecha real)_ | _pendiente_ | _pendiente_ | _pendiente_ |
| 2026-04-11 | _pendiente (ejecutar en fecha real)_ | _pendiente_ | _pendiente_ | _pendiente_ |
| 2026-04-12 | _pendiente (ejecutar en fecha real)_ | _pendiente_ | _pendiente_ | _pendiente_ |



## Registro automático de corridas (append-only)

Comando operativo para avanzar corrida diaria:

```bash
make r701-observe
# opcional: sobreescribir ventana
make r701-observe R701_WINDOW_START=2026-04-06 R701_WINDOW_END=2026-04-12
# opcional: fecha explícita y re-ejecución controlada
make r701-observe R701_ARGS="--date 2026-04-07"
make r701-observe R701_ARGS="--date 2026-04-07 --force"
# opcional: permitir ejecución con working tree sucio
make r701-observe R701_ARGS="--date 2026-04-07 --allow-dirty"
# equivalente directo
bash scripts/r701_observation_run.sh --append
# opcional: fijar fecha de la ventana
bash scripts/r701_observation_run.sh --append --date 2026-04-07
# opcional: permitir re-ejecución del mismo día
bash scripts/r701_observation_run.sh --append --date 2026-04-07 --force
```

> El runner bloquea duplicados por fecha de ventana (una corrida por día), salvo que se use `--force`.
> Por defecto exige working tree limpio; para bypass explícito usar `--allow-dirty`.
> Este bloque agrega una fila por ejecución real sin alterar la tabla base de planificación.

| Fecha/hora UTC | Commit SHA evaluado | Resultado Gate A (pass/fail + resumen) | Resultado Gate B (drift/no drift + endpoint afectado si aplica) | Decisión del día (continuar observación / abrir incidente / escalar) |
| --- | --- | --- | --- | --- |
<!-- AUTO-RUNS-START -->
| 2026-04-06T00:45:38Z | `226827c356ae5bfbd9ad52a2cb69a1b88d371348` | **PASS** — make release-readiness OK. | **NO DRIFT** — contrato/snapshot en estado esperado; endpoint afectado: por determinar. | **continuar observación** |
<!-- AUTO-RUNS-END -->

## Estado de cierre (snapshot)

- Fecha de snapshot: **2026-04-06 (UTC)**.
- Corridas AUTO-RUNS (raw): **1**.
- Corridas efectivas (última por día) en ventana 2026-04-06..2026-04-12: **1 ejecución(es) / 1 de 7 días cubiertos**.
- Gate A acumulado: **1 PASS / 0 FAIL**.
- Gate B acumulado: **1 NO DRIFT / 0 DRIFT**.
- Estado R7-01 al snapshot: **Abierto (en observación)**; no cerrable hasta completar los 7 días de ventana sin drift.

## Protocolo ante drift

Si Gate B detecta drift contractual:

1. Abrir incidente interno **severidad alta** (referencia cruzada en este documento y en `docs/hito7_risk_register.md`).
2. Bloquear cierre de riesgo R7-01 hasta corrección verificada.
3. Registrar plan de corrección mínimo con:
   - endpoint(s) afectado(s),
   - tipo de drift (breaking / non-breaking),
   - owner y ETA,
   - evidencia de remediación (nueva corrida A/B en verde).

## Corte final (ejecución requerida el 2026-04-12)

Comando de consolidación ejecutiva:

```bash
make r701-sync-snapshot R701_CUT_DATE=2026-04-12
make r701-final-cut
# opcional: sobreescribir ventana y fecha de corte
make r701-final-cut R701_CUT_DATE=2026-04-06 R701_WINDOW_START=2026-04-06 R701_WINDOW_END=2026-04-12
# opcional: corte preliminar en fecha distinta
make r701-final-cut R701_CUT_DATE=2026-04-06
# equivalente directo
python scripts/r701_final_cut.py --today 2026-04-12
```

Completar al cierre de ventana:

- **Número de corridas ejecutadas:** _pendiente_
- **% pass Gate A:** _pendiente_
- **% sin drift Gate B:** _pendiente_
- **Incidentes abiertos (si aplica):** _pendiente_
- **Decisión final R7-01:** _pendiente_ (`Cerrado` o `Abierto (con extensión)`).
- **Nueva fecha objetivo (si extensión):** _pendiente_

> Nota operativa: al momento de creación (2026-04-06), solo es posible registrar corridas ejecutadas hasta la fecha actual; las filas futuras quedan precreadas para asegurar evidencia diaria sin gaps durante el resto de la ventana.
