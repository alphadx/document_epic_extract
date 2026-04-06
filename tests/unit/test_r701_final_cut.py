from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _write_log(path: Path, rows: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "# log",
                "<!-- AUTO-RUNS-START -->",
                *rows,
                "<!-- AUTO-RUNS-END -->",
            ]
        )
        + "\n"
    )


def _run_final_cut(
    log_path: Path,
    today: str = "2026-04-12",
    window_start: str = "2026-04-06",
    window_end: str = "2026-04-12",
) -> str:
    cmd = [
        sys.executable,
        "scripts/r701_final_cut.py",
        "--log",
        str(log_path),
        "--today",
        today,
        "--window-start",
        window_start,
        "--window-end",
        window_end,
    ]
    cp = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return cp.stdout


def test_final_cut_stays_open_if_window_not_complete(tmp_path: Path) -> None:
    log = tmp_path / "log.md"
    _write_log(
        log,
        [
            "| 2026-04-06T00:45:38Z | `abc` | **PASS** — ok. | **NO DRIFT** — ok. | **continuar observación** |",
        ],
    )

    out = _run_final_cut(log)

    assert "Días cubiertos en ventana (2026-04-06..2026-04-12): **1/7**" in out
    assert "Decisión final sugerida: **Abierto (con extensión)**" in out


def test_final_cut_closes_if_all_days_no_drift(tmp_path: Path) -> None:
    log = tmp_path / "log.md"
    rows = []
    for day in range(6, 13):
        rows.append(
            f"| 2026-04-{day:02d}T00:00:00Z | `sha{day}` | **PASS** — ok. | **NO DRIFT** — ok. | **continuar observación** |"
        )
    _write_log(log, rows)

    out = _run_final_cut(log)

    assert "Días cubiertos en ventana (2026-04-06..2026-04-12): **7/7**" in out
    assert "Decisión final sugerida: **Cerrado**" in out


def test_final_cut_supports_non_april_window_dates(tmp_path: Path) -> None:
    log = tmp_path / "log_may.md"
    rows = []
    for day in range(1, 4):
        rows.append(
            f"| 2026-05-{day:02d}T00:00:00Z | `sha{day}` | **PASS** — ok. | **NO DRIFT** — ok. | **continuar observación** |"
        )
    _write_log(log, rows)

    out = _run_final_cut(log, today="2026-05-03", window_start="2026-05-01", window_end="2026-05-03")

    assert "Días cubiertos en ventana (2026-05-01..2026-05-03): **3/3**" in out
    assert "Decisión final sugerida: **Cerrado**" in out


def test_final_cut_uses_latest_run_per_day_for_effective_metrics(tmp_path: Path) -> None:
    log = tmp_path / "log_dupe.md"
    _write_log(
        log,
        [
            "| 2026-04-06T00:00:00Z | `sha1` | **PASS** — ok. | **NO DRIFT** — ok. | **continuar observación** |",
            "| 2026-04-06T12:00:00Z | `sha2` | **FAIL** — bad. | **DRIFT** — bad. | **escalar** |",
        ],
    )

    out = _run_final_cut(log, today="2026-04-06")

    assert "Número de corridas (raw AUTO-RUNS): **2**" in out
    assert "Número de corridas efectivas (última por día): **1**" in out
    assert "% PASS Gate A: **0.0%** (0 PASS / 1 FAIL)" in out
    assert "% NO DRIFT Gate B: **0.0%** (0 NO DRIFT / 1 DRIFT)" in out
