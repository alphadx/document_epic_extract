"""Resilience primitives for LLM adapter flows."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Protocol

from api.core.config import settings

logger = logging.getLogger(__name__)

_RECORD_FAILURE_LUA = """
local key = KEYS[1]
local threshold = tonumber(ARGV[1])
local cooldown_ms = tonumber(ARGV[2])
local now_ms = tonumber(ARGV[3])

local failures = redis.call('HINCRBY', key, 'failures', 1)
if failures >= threshold then
  redis.call('HSET', key,
    'state', 'open',
    'opened_until_ms', now_ms + cooldown_ms,
    'half_open_tokens', 0,
    'updated_at_ms', now_ms
  )
else
  redis.call('HSET', key,
    'state', 'closed',
    'updated_at_ms', now_ms
  )
end

return failures
"""

_RESET_LUA = """
local key = KEYS[1]
local expected_updated_at_ms = tonumber(ARGV[1])
local now_ms = tonumber(ARGV[2])

local current_updated_at_ms = tonumber(redis.call('HGET', key, 'updated_at_ms') or '0')
if expected_updated_at_ms > 0 and current_updated_at_ms ~= expected_updated_at_ms then
  return 0
end

redis.call('HSET', key,
  'state', 'closed',
  'failures', 0,
  'opened_until_ms', 0,
  'half_open_tokens', 0,
  'updated_at_ms', now_ms
)
return 1
"""

_IS_OPEN_LUA = """
local key = KEYS[1]
local now_ms = tonumber(ARGV[1])
local half_open_max_calls = tonumber(ARGV[2])

local state = redis.call('HGET', key, 'state') or 'closed'
if state == 'open' then
  local opened_until_ms = tonumber(redis.call('HGET', key, 'opened_until_ms') or '0')
  if opened_until_ms > now_ms then
    return 1
  end

  redis.call('HSET', key,
    'state', 'half_open',
    'half_open_tokens', half_open_max_calls,
    'updated_at_ms', now_ms
  )
  state = 'half_open'
end

if state == 'half_open' then
  local tokens = tonumber(redis.call('HGET', key, 'half_open_tokens') or '0')
  if tokens <= 0 then
    return 1
  end
  redis.call('HINCRBY', key, 'half_open_tokens', -1)
  redis.call('HSET', key, 'updated_at_ms', now_ms)
  return 0
end

return 0
"""


class CircuitBreakerStore(Protocol):
    """Shared contract for circuit-breaker backends."""

    def clear(self) -> None:
        """Remove all tracked state."""

    def is_open(self, key: str) -> bool:
        """Return whether circuit is currently open for `key`."""

    def get_state(self, key: str) -> str:
        """Return current state (`closed|open|half_open`) for `key`."""

    def record_failure(self, key: str, threshold: int, cooldown_ms: int) -> None:
        """Register failed call and open the circuit when threshold is reached."""

    def reset(self, key: str) -> None:
        """Set circuit state back to closed for `key`."""


@dataclass
class InMemoryCircuitBreakerStore:
    """In-memory circuit-breaker state keyed by model/provider identifier."""

    state: dict[str, dict[str, float | int]] = field(default_factory=dict)

    def clear(self) -> None:
        self.state.clear()

    def is_open(self, key: str) -> bool:
        entry = self.state.setdefault(
            key,
            {"state": "closed", "failures": 0, "opened_until": 0.0, "half_open_tokens": 0},
        )
        if not entry:
            return False

        state = str(entry.get("state", "closed"))
        if state == "half_open":
            tokens = int(entry.get("half_open_tokens", 0))
            if tokens <= 0:
                return True
            entry["half_open_tokens"] = tokens - 1
            return False

        opened_until = float(entry.get("opened_until", 0))
        now = time.monotonic()
        if state == "open" and opened_until > now:
            return True
        if state == "open" and opened_until <= now:
            entry["state"] = "half_open"
            entry["half_open_tokens"] = max(1, settings.llm_circuit_breaker_half_open_max_calls)
            entry["opened_until"] = 0
            tokens = int(entry.get("half_open_tokens", 0))
            if tokens <= 0:
                return True
            entry["half_open_tokens"] = tokens - 1
            return False
        if opened_until <= now:
            entry["opened_until"] = 0
            entry["failures"] = 0
            entry["state"] = "closed"
            return False

        return False

    def get_state(self, key: str) -> str:
        entry = self.state.get(key)
        if not entry:
            return "closed"
        return str(entry.get("state", "closed"))

    def record_failure(self, key: str, threshold: int, cooldown_ms: int) -> None:
        safe_threshold = max(1, threshold)
        safe_cooldown_ms = max(0, cooldown_ms)

        entry = self.state.setdefault(
            key,
            {"state": "closed", "failures": 0, "opened_until": 0.0, "half_open_tokens": 0},
        )
        state = str(entry.get("state", "closed"))
        if state == "half_open":
            entry["state"] = "open"
            entry["failures"] = safe_threshold
            entry["opened_until"] = time.monotonic() + (safe_cooldown_ms / 1000)
            entry["half_open_tokens"] = 0
            return

        entry["failures"] = int(entry.get("failures", 0)) + 1
        if int(entry["failures"]) >= safe_threshold:
            entry["state"] = "open"
            entry["opened_until"] = time.monotonic() + (safe_cooldown_ms / 1000)

    def reset(self, key: str) -> None:
        self.state[key] = {"state": "closed", "failures": 0, "opened_until": 0.0, "half_open_tokens": 0}


@dataclass
class RedisCircuitBreakerStore:
    """Redis-backed circuit-breaker state for multi-replica deployments."""

    redis_client: Any
    key_prefix: str = "cb:llm_router:"

    def _redis_key(self, key: str) -> str:
        return f"{self.key_prefix}{key}"

    def clear(self) -> None:
        for key in self.redis_client.scan_iter(match=f"{self.key_prefix}*"):
            self.redis_client.delete(key)

    def is_open(self, key: str) -> bool:
        redis_key = self._redis_key(key)
        now_ms = int(time.time() * 1000)
        result = int(
            self.redis_client.eval(
                _IS_OPEN_LUA,
                1,
                redis_key,
                now_ms,
                max(1, settings.llm_circuit_breaker_half_open_max_calls),
            )
        )
        return bool(result)

    def get_state(self, key: str) -> str:
        redis_key = self._redis_key(key)
        entry = self.redis_client.hgetall(redis_key)
        if not entry:
            return "closed"
        return str(entry.get("state", "closed"))

    def record_failure(self, key: str, threshold: int, cooldown_ms: int) -> None:
        safe_threshold = max(1, threshold)
        safe_cooldown_ms = max(0, cooldown_ms)
        now_ms = int(time.time() * 1000)
        redis_key = self._redis_key(key)
        previous_state = self.get_state(key)

        self.redis_client.eval(
            _RECORD_FAILURE_LUA,
            1,
            redis_key,
            safe_threshold,
            safe_cooldown_ms,
            now_ms,
        )
        if previous_state == "half_open":
            self.redis_client.hset(redis_key, mapping={"half_open_tokens": 0})
        if safe_cooldown_ms > 0:
            ttl_seconds = max(60, int((safe_cooldown_ms / 1000) * 2))
            self.redis_client.expire(redis_key, ttl_seconds)

    def reset(self, key: str) -> None:
        self.reset_if_version(key)

    def reset_if_version(self, key: str, expected_updated_at_ms: int | None = None) -> bool:
        now_ms = int(time.time() * 1000)
        redis_key = self._redis_key(key)
        cas_token = expected_updated_at_ms or 0
        updated = int(
            self.redis_client.eval(
                _RESET_LUA,
                1,
                redis_key,
                cas_token,
                now_ms,
            )
        )
        return bool(updated)


def _build_redis_store(redis_url: str, key_prefix: str) -> CircuitBreakerStore:
    try:
        from redis import Redis
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("Redis backend requested but 'redis' dependency is not installed.") from exc

    client = Redis.from_url(redis_url, decode_responses=True, socket_timeout=1, socket_connect_timeout=1)
    client.ping()
    return RedisCircuitBreakerStore(redis_client=client, key_prefix=key_prefix)


def create_circuit_breaker_store(
    backend: str | None = None,
    redis_url: str | None = None,
    key_prefix: str | None = None,
) -> CircuitBreakerStore:
    selected_backend = (backend or settings.llm_circuit_breaker_backend).strip().lower()
    if selected_backend == "redis":
        target_redis_url = redis_url or settings.llm_circuit_breaker_redis_url
        target_key_prefix = key_prefix or settings.llm_circuit_breaker_redis_prefix
        try:
            return _build_redis_store(target_redis_url, target_key_prefix)
        except Exception:  # noqa: BLE001
            logger.exception(
                "Circuit breaker Redis backend unavailable, falling back to in-memory store.",
            )
    return InMemoryCircuitBreakerStore()


@dataclass
class CircuitBreakerTelemetry:
    """In-process counters/gauges for circuit-breaker observability."""

    state: dict[tuple[str, str], int] = field(default_factory=dict)
    open_total: dict[tuple[str, str], int] = field(default_factory=dict)
    reject_total: dict[tuple[str, str], int] = field(default_factory=dict)
    half_open_probe_total: dict[tuple[str, str, str], int] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock)

    def _provider_key(self, key: str) -> tuple[str, str]:
        if ":" in key:
            provider, _rest = key.split(":", 1)
            return provider, key
        return "unknown", key

    def set_state(self, key: str, state: str) -> None:
        state_value = {"closed": 0, "open": 1, "half_open": 2}.get(state, 0)
        with self._lock:
            self.state[self._provider_key(key)] = state_value

    def increment_open(self, key: str) -> None:
        with self._lock:
            pk = self._provider_key(key)
            self.open_total[pk] = self.open_total.get(pk, 0) + 1

    def increment_reject(self, key: str) -> None:
        with self._lock:
            pk = self._provider_key(key)
            self.reject_total[pk] = self.reject_total.get(pk, 0) + 1

    def increment_half_open_probe(self, key: str, result: str) -> None:
        with self._lock:
            provider, normalized_key = self._provider_key(key)
            metric_key = (provider, normalized_key, result)
            self.half_open_probe_total[metric_key] = self.half_open_probe_total.get(metric_key, 0) + 1

    def emit_transition_log(
        self,
        *,
        key: str,
        from_state: str,
        to_state: str,
        reason: str,
        cooldown_ms: int | None,
        failures: int | None,
    ) -> None:
        provider, normalized_key = self._provider_key(key)
        logger.info(
            "event=cb_transition provider=%s key=%s from_state=%s to_state=%s reason=%s cooldown_ms=%s failures=%s",
            provider,
            normalized_key,
            from_state,
            to_state,
            reason,
            cooldown_ms if cooldown_ms is not None else "na",
            failures if failures is not None else "na",
        )

    def snapshot(self) -> dict[str, dict[str, int]]:
        with self._lock:
            flat_state = {f"{provider}|{key}": value for (provider, key), value in self.state.items()}
            flat_open = {f"{provider}|{key}": value for (provider, key), value in self.open_total.items()}
            flat_reject = {f"{provider}|{key}": value for (provider, key), value in self.reject_total.items()}
            flat_probe = {
                f"{provider}|{key}|{result}": value
                for (provider, key, result), value in self.half_open_probe_total.items()
            }
            return {
                "cb_state": flat_state,
                "cb_open_total": flat_open,
                "cb_reject_total": flat_reject,
                "cb_half_open_probe_total": flat_probe,
            }


def get_circuit_breaker_metrics_snapshot() -> dict[str, dict[str, int]]:
    return circuit_breaker_telemetry.snapshot()


circuit_breaker_telemetry = CircuitBreakerTelemetry()
circuit_breaker_store = create_circuit_breaker_store()
