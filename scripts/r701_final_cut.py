#!/usr/bin/env python3
"""Compute executive final-cut summary for R7-01 observation window."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

def parse_auto_rows(text: str) -> list[str]:
    start = "<!-- AUTO-RUNS-START -->"
    end = "<!-- AUTO-RUNS-END -->"
    if start not in text or end not in text:
        return []
    chunk = text.split(start, 1)[1].split(end, 1)[0]
    return [ln.strip() for ln in chunk.splitlines() if ln.strip().startswith("|")]


def rows_by_latest_day(rows: list[str]) -> dict[str, str]:
    day_re = re.compile(r"\|\s*(\d{4}-\d{2}-\d{2})T")
    by_day: dict[str, str] = {}
    for row in rows:
        m = day_re.search(row)
        if not m:
            continue
        by_day[m.group(1)] = row
    return by_day


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="docs/hito7_r701_observability_log.md",
        help="Ruta del log R7-01",
    )
    parser.add_argument(
        "--today",
        default=date.today().isoformat(),
        help="Fecha de corte para el resumen (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--extension-date",
        default="2026-04-19",
        help="Nueva fecha objetivo si queda abierto",
    )
    parser.add_argument(
        "--window-start",
        default="2026-04-06",
        help="Inicio de ventana (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--window-end",
        default="2026-04-12",
        help="Fin de ventana (YYYY-MM-DD)",
    )
    args = parser.parse_args()

    window_start = date.fromisoformat(args.window_start)
    window_end = date.fromisoformat(args.window_end)
    if window_end < window_start:
        raise SystemExit("window-end no puede ser menor que window-start")

    text = Path(args.log).read_text()
    rows = parse_auto_rows(text)
    total_runs_raw = len(rows)
    latest_by_day = rows_by_latest_day(rows)
    effective_rows = list(latest_by_day.values())

    pass_count = sum("**PASS**" in r for r in effective_rows)
    fail_count = sum("**FAIL**" in r for r in effective_rows)
    no_drift_count = sum("**NO DRIFT**" in r for r in effective_rows)
    drift_count = sum("**DRIFT**" in r for r in effective_rows)

    covered_days = {
        date.fromisoformat(day)
        for day in latest_by_day
    }
    in_window_days = {
        d for d in covered_days if window_start <= d <= window_end
    }
    expected_days = (window_end - window_start).days + 1

    all_days_covered = len(in_window_days) == expected_days
    no_drift = drift_count == 0
    decision = "Cerrado" if (all_days_covered and no_drift and fail_count == 0) else "Abierto (con extensión)"

    effective_runs = len(effective_rows)
    pass_pct = (pass_count / effective_runs * 100) if effective_runs else 0.0
    no_drift_pct = (no_drift_count / effective_runs * 100) if effective_runs else 0.0

    print("# Corte ejecutivo R7-01")
    print(f"Fecha de corte: **{args.today}**")
    print(f"- Número de corridas (raw AUTO-RUNS): **{total_runs_raw}**")
    print(f"- Número de corridas efectivas (última por día): **{effective_runs}**")
    print(f"- Días cubiertos en ventana ({args.window_start}..{args.window_end}): **{len(in_window_days)}/{expected_days}**")
    print(f"- % PASS Gate A: **{pass_pct:.1f}%** ({pass_count} PASS / {fail_count} FAIL)")
    print(f"- % NO DRIFT Gate B: **{no_drift_pct:.1f}%** ({no_drift_count} NO DRIFT / {drift_count} DRIFT)")
    print(f"- Incidentes (drift): **{drift_count}**")
    print(f"- Decisión final sugerida: **{decision}**")
    if decision != "Cerrado":
        print(f"- Nueva fecha objetivo sugerida: **{args.extension_date}**")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
