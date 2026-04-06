from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_sync_snapshot_updates_log_and_risk_with_effective_metrics(tmp_path: Path) -> None:
    log_path = tmp_path / "log.md"
    risk_path = tmp_path / "risk.md"

    log_path.write_text(
        """
# Log
<!-- AUTO-RUNS-START -->
| 2026-04-06T00:00:00Z | `sha1` | **PASS** — ok. | **NO DRIFT** — ok. | **continuar observación** |
| 2026-04-06T12:00:00Z | `sha2` | **FAIL** — bad. | **DRIFT** — bad. | **escalar** |
| 2026-04-07T00:00:00Z | `sha3` | **PASS** — ok. | **NO DRIFT** — ok. | **continuar observación** |
<!-- AUTO-RUNS-END -->

## Estado de cierre (snapshot)

- placeholder

## Protocolo ante drift
""".strip()
        + "\n"
    )

    risk_path.write_text(
        """
# Risk
## Evidencia de avance actual
- Snapshot de observación R7-01 al 2026-04-06 (UTC): old.
""".strip()
        + "\n"
    )

    cmd = [
        sys.executable,
        "scripts/r701_sync_snapshot.py",
        "--log",
        str(log_path),
        "--risk",
        str(risk_path),
        "--snapshot-date",
        "2026-04-07",
        "--window-start",
        "2026-04-06",
        "--window-end",
        "2026-04-12",
    ]
    cp = subprocess.run(cmd, check=True, capture_output=True, text=True)
    assert "Synced snapshot counters." in cp.stdout

    log_out = log_path.read_text()
    risk_out = risk_path.read_text()

    assert "Corridas AUTO-RUNS (raw): **3**." in log_out
    assert "Corridas efectivas (última por día) en ventana 2026-04-06..2026-04-12: **2 ejecución(es) / 2 de 7 días cubiertos**." in log_out
    assert "Gate A acumulado: **1 PASS / 1 FAIL**." in log_out
    assert "Gate B acumulado: **1 NO DRIFT / 1 DRIFT**." in log_out

    assert "**3 AUTO-RUNS (raw), 2/7 días cubiertos (última corrida por día)**, drift detectado: 1." in risk_out
