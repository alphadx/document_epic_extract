#!/usr/bin/env bash
set -euo pipefail

APPEND_MODE="false"
FORCE_APPEND="false"
ALLOW_DIRTY="false"
RUN_DATE="$(date -u +"%Y-%m-%d")"
WINDOW_START="${R701_WINDOW_START:-2026-04-06}"
WINDOW_END="${R701_WINDOW_END:-2026-04-12}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --append)
      APPEND_MODE="true"
      ;;
    --force)
      FORCE_APPEND="true"
      ;;
    --allow-dirty)
      ALLOW_DIRTY="true"
      ;;
    --date)
      shift
      RUN_DATE="${1:?--date requiere valor YYYY-MM-DD}"
      ;;
    *)
      echo "Uso: bash scripts/r701_observation_run.sh [--append] [--force] [--allow-dirty] [--date YYYY-MM-DD] (ventana por env: R701_WINDOW_START/R701_WINDOW_END)" >&2
      exit 1
      ;;
  esac
  shift
done

if [[ "$RUN_DATE" < "$WINDOW_START" || "$RUN_DATE" > "$WINDOW_END" ]]; then
  echo "Fecha fuera de ventana R7-01 (permitidas: ${WINDOW_START}..${WINDOW_END}): $RUN_DATE" >&2
  exit 1
fi

# Early duplicate guard: avoid running expensive gates if append for an already-covered day.
if [[ "$APPEND_MODE" == "true" && "$FORCE_APPEND" != "true" ]]; then
  export R701_DATE="$RUN_DATE"
  python - <<'PY'
from pathlib import Path
import os

run_date = os.environ["R701_DATE"]
text = Path("docs/hito7_r701_observability_log.md").read_text()
if f"| {run_date}T" in text:
    raise SystemExit(
        f"Ya existe corrida para {run_date}. Usa --force solo si necesitas registrar re-ejecución del día."
    )
PY
fi


if [[ "$ALLOW_DIRTY" != "true" ]] && [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree con cambios sin commitear. Usa --allow-dirty si necesitas correr observación en este estado." >&2
  exit 3
fi

time_utc="$(date -u +"%H:%M:%SZ")"
timestamp="${RUN_DATE}T${time_utc}"
sha="$(git rev-parse HEAD)"

# Gate A
set +e
out_a="$(make release-readiness 2>&1)"
code_a=$?
set -e

if [[ $code_a -eq 0 ]]; then
  gate_a="PASS"
  gate_a_summary="make release-readiness OK"
else
  gate_a="FAIL"
  gate_a_summary="make release-readiness falló"
fi

# Gate B
set +e
out_b1="$(pytest -q tests/integration/test_openapi_contract.py tests/integration/test_openapi_signature_snapshot.py 2>&1)"
code_b1=$?
out_b2="$(python scripts/generate_openapi_signature.py 2>&1)"
code_b2=$?
out_b3="$(git diff --exit-code tests/fixtures/openapi_signature.json 2>&1)"
code_b3=$?
set -e

if [[ $code_b1 -eq 0 && $code_b2 -eq 0 && $code_b3 -eq 0 ]]; then
  gate_b="NO DRIFT"
  gate_b_summary="contrato/snapshot en estado esperado"
  decision="continuar observación"
else
  gate_b="DRIFT"
  gate_b_summary="drift detectado (revisar tests/snapshot)"
  decision="abrir incidente (severidad alta) y escalar"
fi

row="| ${timestamp} | \`${sha}\` | **${gate_a}** — ${gate_a_summary}. | **${gate_b}** — ${gate_b_summary}; endpoint afectado: por determinar. | **${decision}** |"
echo "$row"

if [[ "$APPEND_MODE" == "true" ]]; then
  export R701_ROW="$row"
  python - <<'PY'
from pathlib import Path
import os

log_file = Path("docs/hito7_r701_observability_log.md")
row = os.environ["R701_ROW"]
text = log_file.read_text()
start = "<!-- AUTO-RUNS-START -->"
end = "<!-- AUTO-RUNS-END -->"
if start not in text or end not in text:
    raise SystemExit("No se encontraron marcadores AUTO-RUNS en el log.")
text = text.replace(end, row + "\n" + end)
log_file.write_text(text)
PY
fi

printf "\n[gate-a:%s]\n%s\n" "$code_a" "$out_a"
printf "\n[gate-b-tests:%s]\n%s\n" "$code_b1" "$out_b1"
printf "\n[gate-b-signature:%s]\n%s\n" "$code_b2" "$out_b2"
printf "\n[gate-b-diff:%s]\n%s\n" "$code_b3" "$out_b3"

if [[ "$gate_b" == "DRIFT" || "$gate_a" == "FAIL" ]]; then
  exit 2
fi
