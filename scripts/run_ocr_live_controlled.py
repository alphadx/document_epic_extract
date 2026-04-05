"""Execute controlled live OCR run and write a dated markdown report.

This script runs safe scenarios automatically when enough configuration exists,
and marks manual-required scenarios explicitly when the environment does not
provide outage/timeout controls.
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import httpx


@dataclass
class ScenarioResult:
    provider: str
    scenario: str
    status: str
    http_code: int | None
    detail: str


def _now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _api_base() -> str:
    return os.getenv("OCR_API_BASE", "http://127.0.0.1:8000").rstrip("/")


def _doc_b64() -> str:
    text = os.getenv("OCR_DOC_TEXT", "invoice_number: INV-LIVE-1\ntotal_amount: 123.45")
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def _provider_ready(provider: str) -> tuple[bool, list[str]]:
    if provider == "aws":
        req = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
    elif provider == "gcp":
        req = ["GOOGLE_APPLICATION_CREDENTIALS", "GCP_PROJECT_ID", "GCP_PROCESSOR_ID"]
    else:
        req = ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    missing = [k for k in req if not os.getenv(k)]
    return len(missing) == 0, missing


def _build_payload(provider: str, scenario: str) -> dict[str, Any]:
    model = {"aws": "textract", "gcp": "docai", "azure": "prebuilt-invoice"}[provider]
    api_keys: dict[str, str] = {}

    if provider == "gcp":
        if scenario == "invalid_credentials":
            api_keys.update(
                {
                    "gcp_project_id": "bad-project",
                    "gcp_location": "us",
                    "gcp_processor_id": "bad-processor",
                }
            )
        else:
            if os.getenv("GCP_PROJECT_ID"):
                api_keys["gcp_project_id"] = os.getenv("GCP_PROJECT_ID", "")
            if os.getenv("GCP_LOCATION"):
                api_keys["gcp_location"] = os.getenv("GCP_LOCATION", "us")
            if os.getenv("GCP_PROCESSOR_ID"):
                api_keys["gcp_processor_id"] = os.getenv("GCP_PROCESSOR_ID", "")

    if provider == "azure":
        if scenario == "invalid_credentials":
            api_keys.update({"azure_endpoint": "https://invalid.local/", "azure_key": "bad-key"})
        else:
            api_keys.update(
                {
                    "azure_endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
                    "azure_key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
                }
            )

    document = _doc_b64()
    if scenario in {"timeout", "provider_down"}:
        override = os.getenv(f"OCR_{provider.upper()}_{scenario.upper()}_DOC_URL", "").strip()
        if override:
            document = override

    return {
        "document": document,
        "engine_config": {"provider": provider, "model": model, "api_keys": api_keys},
        "extraction_target": {"document_type": "invoice"},
    }


def _call_extract(payload: dict[str, Any]) -> tuple[int | None, str]:
    try:
        response = httpx.post(f"{_api_base()}/extract", json=payload, timeout=35.0)
    except Exception as exc:  # noqa: BLE001
        return None, f"request_error: {exc}"

    detail = ""
    try:
        body = response.json()
        detail = str(body.get("detail", ""))
    except Exception:  # noqa: BLE001
        detail = response.text[:300]

    return response.status_code, detail


def _run_provider(provider: str) -> list[ScenarioResult]:
    configured, missing = _provider_ready(provider)
    results: list[ScenarioResult] = []

    for scenario in ("valid_credentials", "invalid_credentials", "timeout", "provider_down"):
        if not configured and scenario == "valid_credentials":
            results.append(
                ScenarioResult(provider, scenario, "SKIPPED", None, f"missing credentials: {', '.join(missing)}")
            )
            continue

        if scenario in {"timeout", "provider_down"}:
            key = f"OCR_{provider.upper()}_{scenario.upper()}_DOC_URL"
            if not os.getenv(key):
                results.append(
                    ScenarioResult(provider, scenario, "MANUAL_REQUIRED", None, f"set {key} to run this scenario")
                )
                continue

        if provider == "aws" and scenario == "invalid_credentials":
            results.append(
                ScenarioResult(
                    provider,
                    scenario,
                    "MANUAL_REQUIRED",
                    None,
                    "aws invalid credentials must be injected in API runtime env",
                )
            )
            continue

        payload = _build_payload(provider, scenario)
        code, detail = _call_extract(payload)
        status = "PASS" if code == 200 and scenario == "valid_credentials" else "OBSERVED"
        if scenario != "valid_credentials" and code == 502:
            status = "PASS"
        if code is None:
            status = "ERROR"
        results.append(ScenarioResult(provider, scenario, status, code, detail))

    return results


def _write_report(results: list[ScenarioResult]) -> Path:
    today = date.today().isoformat()
    path = Path(f"docs/ocr_live_run_controlled_{today}.md")
    lines = [
        f"# Corrida live controlada OCR — {today}",
        "",
        f"Generado: {_now_utc()}",
        f"API base: `{_api_base()}`",
        "",
        "| Proveedor | Escenario | Estado | HTTP | Detalle |",
        "|---|---|---|---|---|",
    ]
    for row in results:
        code = "-" if row.http_code is None else str(row.http_code)
        detail = row.detail.replace("|", "/").replace("\n", " ")[:180]
        lines.append(f"| {row.provider.upper()} | {row.scenario} | {row.status} | {code} | {detail} |")

    lines.extend(
        [
            "",
            "## Nota",
            "",
            "- `MANUAL_REQUIRED` indica que falta configuración controlada para simular timeout/proveedor caído.",
            "- `SKIPPED` indica credenciales ausentes para ejecutar live con proveedor real.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    all_results: list[ScenarioResult] = []
    for provider in ("aws", "gcp", "azure"):
        all_results.extend(_run_provider(provider))
    out = _write_report(all_results)
    print(f"Report written to {out}")


if __name__ == "__main__":
    main()
