from __future__ import annotations

import subprocess


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "scripts/r701_observation_run.sh", *args],
        check=False,
        text=True,
        capture_output=True,
    )


def test_rejects_date_outside_window_before_running_gates() -> None:
    cp = _run("--date", "2026-05-01")

    assert cp.returncode == 1
    assert "Fecha fuera de ventana R7-01" in cp.stderr


def test_rejects_unknown_argument_with_usage() -> None:
    cp = _run("--unknown-flag")

    assert cp.returncode == 1
    assert "Uso: bash scripts/r701_observation_run.sh" in cp.stderr
