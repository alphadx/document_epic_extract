"""Unit tests for LLM resilience primitives."""

from __future__ import annotations

import time

from adapters.llm.resilience import CircuitBreakerStore


def test_circuit_breaker_opens_and_resets_after_cooldown():
    store = CircuitBreakerStore()
    key = "llm_router:gpt-4o"

    store.record_failure(key, threshold=1, cooldown_ms=1)
    assert store.is_open(key)

    time.sleep(0.01)
    assert not store.is_open(key)


def test_circuit_breaker_reset_clears_failures():
    store = CircuitBreakerStore()
    key = "llm_router:gpt-4o"

    store.record_failure(key, threshold=5, cooldown_ms=1000)
    store.reset(key)

    assert not store.is_open(key)
