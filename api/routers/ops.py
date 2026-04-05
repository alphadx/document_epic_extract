"""Operational endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from adapters.llm.resilience import get_circuit_breaker_metrics_snapshot

router = APIRouter()


@router.get("/circuit-breaker/metrics")
async def circuit_breaker_metrics() -> dict[str, dict[str, int]]:
    """Return in-process circuit-breaker metrics snapshot."""
    return get_circuit_breaker_metrics_snapshot()
