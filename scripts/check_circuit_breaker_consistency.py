"""Consistency checker for distributed circuit-breaker documentation."""

from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    checks: list[tuple[str, str]] = [
        ("README.md", "Acta de consistencia documental"),
        ("TODO.md", "Cierres recientes"),
        ("docs/hitos_avances.md", "circuit breaker distribuido ya implementado"),
        ("docs/milestone_decisions.md", "Estado del riesgo:** **cerrado**"),
        ("docs/circuit_breaker_distribuido.md", "Estado: Implementada"),
    ]

    failures: list[str] = []
    for path, expected_snippet in checks:
        content = _read(path)
        if expected_snippet not in content:
            failures.append(f"- {path}: missing snippet '{expected_snippet}'")

    if failures:
        print("❌ Circuit breaker consistency check failed:")
        print("\n".join(failures))
        return 1

    print("✅ Circuit breaker consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
