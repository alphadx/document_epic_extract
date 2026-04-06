#!/usr/bin/env python3
"""Sync snapshot counters in observability/risk docs from AUTO-RUNS rows."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def parse_rows(text: str) -> list[str]:
    start = "<!-- AUTO-RUNS-START -->"
    end = "<!-- AUTO-RUNS-END -->"
    if start not in text or end not in text:
        return []
    chunk = text.split(start, 1)[1].split(end, 1)[0]
    return [ln.strip() for ln in chunk.splitlines() if ln.strip().startswith("|")]


def latest_by_day(rows: list[str]) -> dict[str, str]:
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
    parser.add_argument("--log", default="docs/hito7_r701_observability_log.md")
    parser.add_argument("--risk", default="docs/hito7_risk_register.md")
    parser.add_argument("--snapshot-date", default=date.today().isoformat())
    parser.add_argument("--window-start", default="2026-04-06")
    parser.add_argument("--window-end", default="2026-04-12")
    args = parser.parse_args()

    log_path = Path(args.log)
    risk_path = Path(args.risk)

    window_start = date.fromisoformat(args.window_start)
    window_end = date.fromisoformat(args.window_end)

    log_text = log_path.read_text()
    rows = parse_rows(log_text)

    total_runs = len(rows)
    by_day = latest_by_day(rows)
    effective_rows = list(by_day.values())
    pass_count = sum("**PASS**" in r for r in effective_rows)
    fail_count = sum("**FAIL**" in r for r in effective_rows)
    no_drift_count = sum("**NO DRIFT**" in r for r in effective_rows)
    drift_count = sum("**DRIFT**" in r for r in effective_rows)

    covered_days = {
        date.fromisoformat(day)
        for day in by_day
    }
    in_window_days = {d for d in covered_days if window_start <= d <= window_end}
    total_days = (window_end - window_start).days + 1

    state = (
        "Cerrable" if len(in_window_days) == total_days and drift_count == 0 and fail_count == 0 else "Abierto (en observación)"
    )

    snapshot_section = f"""## Estado de cierre (snapshot)\n\n- Fecha de snapshot: **{args.snapshot_date} (UTC)**.\n- Corridas AUTO-RUNS (raw): **{total_runs}**.\n- Corridas efectivas (última por día) en ventana {args.window_start}..{args.window_end}: **{len(effective_rows)} ejecución(es) / {len(in_window_days)} de {total_days} días cubiertos**.\n- Gate A acumulado: **{pass_count} PASS / {fail_count} FAIL**.\n- Gate B acumulado: **{no_drift_count} NO DRIFT / {drift_count} DRIFT**.\n- Estado R7-01 al snapshot: **{state}**; no cerrable hasta completar los {total_days} días de ventana sin drift.\n\n"""

    log_text = re.sub(
        r"## Estado de cierre \(snapshot\)\n.*?\n## Protocolo ante drift\n",
        snapshot_section + "## Protocolo ante drift\n",
        log_text,
        flags=re.S,
    )
    log_path.write_text(log_text)

    risk_text = risk_path.read_text()
    risk_text = re.sub(
        r"- Snapshot de observación R7-01 al .*",
        f"- Snapshot de observación R7-01 al {args.snapshot_date} (UTC): **{total_runs} AUTO-RUNS (raw), {len(in_window_days)}/{total_days} días cubiertos (última corrida por día)**, drift detectado: {drift_count}.",
        risk_text,
    )
    risk_path.write_text(risk_text)

    print("Synced snapshot counters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
