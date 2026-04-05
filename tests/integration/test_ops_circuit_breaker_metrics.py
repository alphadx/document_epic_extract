"""Integration tests for circuit breaker ops endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from adapters.llm.resilience import circuit_breaker_telemetry
from api.main import app

client = TestClient(app)


def test_ops_circuit_breaker_metrics_returns_expected_shape():
    circuit_breaker_telemetry.state.clear()
    circuit_breaker_telemetry.open_total.clear()
    circuit_breaker_telemetry.reject_total.clear()
    circuit_breaker_telemetry.half_open_probe_total.clear()
    circuit_breaker_telemetry.set_state("llm_router:gpt-4o", "open")

    resp = client.get("/ops/circuit-breaker/metrics")
    assert resp.status_code == 200
    payload = resp.json()
    assert set(payload.keys()) == {
        "cb_state",
        "cb_open_total",
        "cb_reject_total",
        "cb_half_open_probe_total",
    }
    assert payload["cb_state"]["llm_router|llm_router:gpt-4o"] == 1
