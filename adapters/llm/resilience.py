"""Resilience primitives for LLM adapter flows."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class CircuitBreakerStore:
    """In-memory circuit-breaker state keyed by model/provider identifier."""

    state: dict[str, dict[str, float | int]] = field(default_factory=dict)

    def clear(self) -> None:
        self.state.clear()

    def is_open(self, key: str) -> bool:
        entry = self.state.get(key)
        if not entry:
            return False

        opened_until = float(entry.get("opened_until", 0))
        now = time.monotonic()
        if opened_until <= now:
            entry["opened_until"] = 0
            entry["failures"] = 0
            return False

        return True

    def record_failure(self, key: str, threshold: int, cooldown_ms: int) -> None:
        safe_threshold = max(1, threshold)
        safe_cooldown_ms = max(0, cooldown_ms)

        entry = self.state.setdefault(key, {"failures": 0, "opened_until": 0.0})
        entry["failures"] = int(entry.get("failures", 0)) + 1
        if int(entry["failures"]) >= safe_threshold:
            entry["opened_until"] = time.monotonic() + (safe_cooldown_ms / 1000)

    def reset(self, key: str) -> None:
        self.state[key] = {"failures": 0, "opened_until": 0.0}


circuit_breaker_store = CircuitBreakerStore()
