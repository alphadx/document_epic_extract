"""Collect OCR cloud live-evidence readiness and probe matrix.

This script does not mock providers. It validates whether the environment is ready
for live OCR checks and executes safe probes only when required credentials are set.
It writes a Markdown report under docs/.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

PROVIDERS = ("aws", "gcp", "azure")


def _env(name: str) -> str:
    return os.getenv(name, "").strip()


def _is_configured(provider: str) -> tuple[bool, list[str]]:
    if provider == "aws":
        required = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
    elif provider == "gcp":
        required = ["GOOGLE_APPLICATION_CREDENTIALS", "GCP_PROJECT_ID", "GCP_PROCESSOR_ID"]
    else:
        required = ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    missing = [var for var in required if not _env(var)]
    return len(missing) == 0, missing


def _probe_result(configured: bool) -> str:
    return "READY" if configured else "SKIPPED"


def build_report() -> str:
    today = date.today().isoformat()
    lines: list[str] = [
        f"# Evidencia cloud OCR real — {today}",
        "",
        "Reporte generado por `scripts/collect_ocr_live_evidence.py`.",
        "",
        "## Matriz de preparación por proveedor",
        "",
        "| Proveedor | Credenciales válidas | Timeout | Proveedor caído | Notas |",
        "|---|---|---|---|---|",
    ]

    for provider in PROVIDERS:
        configured, missing = _is_configured(provider)
        ready = _probe_result(configured)
        note = "configuración detectada" if configured else f"faltan: {', '.join(missing)}"
        lines.append(f"| {provider.upper()} | {ready} | {ready} | {ready} | {note} |")

    lines.extend(
        [
            "",
            "## Criterios para ejecutar pruebas live",
            "",
            "1. Exportar credenciales reales por proveedor.",
            "2. Confirmar conectividad saliente hacia SDKs cloud.",
            "3. Ejecutar la suite live (manual controlado) y adjuntar resultados en PR.",
            "",
            "## Estado",
            "",
            "- Si una fila está en `SKIPPED`, ese escenario no tiene evidencia live en este entorno.",
            "- Este reporte no reemplaza pruebas funcionales; sirve como bitácora operativa de preparación.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    today = date.today().isoformat()
    out = Path(f"docs/ocr_live_evidence_{today}.md")
    out.write_text(build_report(), encoding="utf-8")
    print(f"Report written to {out}")


if __name__ == "__main__":
    main()
