"""Unit tests for LLM resilience primitives."""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from adapters.llm.resilience import (
    _IS_OPEN_LUA,
    _RECORD_FAILURE_LUA,
    _RESET_LUA,
    CircuitBreakerTelemetry,
    InMemoryCircuitBreakerStore,
    RedisCircuitBreakerStore,
    create_circuit_breaker_store,
)


def test_circuit_breaker_opens_and_resets_after_cooldown():
    store = InMemoryCircuitBreakerStore()
    key = "llm_router:gpt-4o"

    store.record_failure(key, threshold=1, cooldown_ms=1)
    assert store.is_open(key)

    time.sleep(0.01)
    assert not store.is_open(key)


def test_circuit_breaker_reset_clears_failures():
    store = InMemoryCircuitBreakerStore()
    key = "llm_router:gpt-4o"

    store.record_failure(key, threshold=5, cooldown_ms=1000)
    store.reset(key)

    assert not store.is_open(key)


def test_factory_falls_back_to_in_memory_when_redis_unavailable(monkeypatch):
    def broken_builder(redis_url: str, key_prefix: str):
        raise RuntimeError("redis down")

    monkeypatch.setattr("adapters.llm.resilience._build_redis_store", broken_builder)

    store = create_circuit_breaker_store(
        backend="redis",
        redis_url="redis://localhost:6379/0",
        key_prefix="cb:test:",
    )

    assert isinstance(store, InMemoryCircuitBreakerStore)


class _FakeRedis:
    def __init__(self):
        self.store: dict[str, dict[str, str | int]] = {}
        self._lock = Lock()

    def scan_iter(self, match: str):
        prefix = match[:-1] if match.endswith("*") else match
        for key in list(self.store.keys()):
            if key.startswith(prefix):
                yield key

    def delete(self, key: str):
        self.store.pop(key, None)

    def hgetall(self, key: str):
        with self._lock:
            return dict(self.store.get(key, {}))

    def hset(self, key: str, mapping: dict[str, str | int]):
        with self._lock:
            entry = self.store.setdefault(key, {})
            entry.update(mapping)

    def expire(self, key: str, seconds: int):
        return seconds

    def eval(self, script: str, num_keys: int, key: str, *args):
        with self._lock:
            if script == _RECORD_FAILURE_LUA:
                threshold = int(args[0])
                cooldown_ms = int(args[1])
                now_ms = int(args[2])
                entry = self.store.setdefault(key, {})
                failures = int(entry.get("failures", 0)) + 1
                entry["failures"] = failures
                if failures >= threshold:
                    entry["state"] = "open"
                    entry["opened_until_ms"] = now_ms + cooldown_ms
                    entry["half_open_tokens"] = 0
                    entry["updated_at_ms"] = now_ms
                else:
                    entry["state"] = "closed"
                    entry["updated_at_ms"] = now_ms
                return failures

            if script == _IS_OPEN_LUA:
                now_ms = int(args[0])
                half_open_max_calls = int(args[1])
                entry = self.store.setdefault(key, {})
                state = str(entry.get("state", "closed"))
                if state == "open":
                    opened_until_ms = int(entry.get("opened_until_ms", 0))
                    if opened_until_ms > now_ms:
                        return 1
                    entry["state"] = "half_open"
                    entry["half_open_tokens"] = half_open_max_calls
                    state = "half_open"
                if state == "half_open":
                    tokens = int(entry.get("half_open_tokens", 0))
                    if tokens <= 0:
                        return 1
                    entry["half_open_tokens"] = tokens - 1
                    return 0
                return 0

            if script == _RESET_LUA:
                expected_updated_at_ms = int(args[0])
                now_ms = int(args[1])
                entry = self.store.setdefault(key, {})
                current_updated_at_ms = int(entry.get("updated_at_ms", 0))
                if expected_updated_at_ms > 0 and current_updated_at_ms != expected_updated_at_ms:
                    return 0
                entry["state"] = "closed"
                entry["failures"] = 0
                entry["opened_until_ms"] = 0
                entry["half_open_tokens"] = 0
                entry["updated_at_ms"] = now_ms
                return 1

            raise AssertionError("Unexpected Lua script")


def test_redis_store_opens_and_resets_circuit():
    fake_redis = _FakeRedis()
    store = RedisCircuitBreakerStore(redis_client=fake_redis, key_prefix="cb:test:")
    key = "gpt-4o"

    store.record_failure(key, threshold=1, cooldown_ms=5)
    assert store.is_open(key)

    time.sleep(0.01)
    assert not store.is_open(key)


def test_in_memory_transition_closed_open_half_open_closed():
    store = InMemoryCircuitBreakerStore()
    key = "llm_router:gpt-4o"

    store.record_failure(key, threshold=1, cooldown_ms=5)
    assert store.get_state(key) == "open"
    assert store.is_open(key)

    time.sleep(0.01)
    assert not store.is_open(key)
    assert store.get_state(key) == "half_open"

    store.reset(key)
    assert store.get_state(key) == "closed"


def test_redis_transition_closed_open_half_open_closed():
    fake_redis = _FakeRedis()
    store = RedisCircuitBreakerStore(redis_client=fake_redis, key_prefix="cb:test:")
    key = "gpt-4o"

    store.record_failure(key, threshold=1, cooldown_ms=5)
    assert store.get_state(key) == "open"
    assert store.is_open(key)

    time.sleep(0.01)
    assert not store.is_open(key)
    assert store.get_state(key) == "half_open"

    store.reset(key)
    assert store.get_state(key) == "closed"


def test_redis_store_reset_with_version_enforces_cas():
    fake_redis = _FakeRedis()
    store = RedisCircuitBreakerStore(redis_client=fake_redis, key_prefix="cb:test:")
    key = "gpt-4o"

    store.record_failure(key, threshold=1, cooldown_ms=50)
    redis_key = "cb:test:gpt-4o"
    current_version = int(fake_redis.hgetall(redis_key)["updated_at_ms"])

    assert not store.reset_if_version(key, expected_updated_at_ms=current_version - 1)
    assert store.is_open(key)
    assert store.reset_if_version(key, expected_updated_at_ms=current_version)
    assert not store.is_open(key)


def test_redis_store_record_failure_is_atomic_under_parallel_calls():
    fake_redis = _FakeRedis()
    store = RedisCircuitBreakerStore(redis_client=fake_redis, key_prefix="cb:test:")
    key = "gpt-4o"
    redis_key = "cb:test:gpt-4o"

    def worker():
        store.record_failure(key, threshold=500, cooldown_ms=50)

    with ThreadPoolExecutor(max_workers=12) as executor:
        list(executor.map(lambda _: worker(), range(120)))

    entry = fake_redis.hgetall(redis_key)
    assert int(entry["failures"]) == 120


def test_circuit_breaker_telemetry_snapshot_shape():
    telemetry = CircuitBreakerTelemetry()
    key = "llm_router:gpt-4o"

    telemetry.set_state(key, "open")
    telemetry.increment_open(key)
    telemetry.increment_reject(key)
    telemetry.increment_half_open_probe(key, "failure")

    snapshot = telemetry.snapshot()
    assert snapshot["cb_state"]["llm_router|llm_router:gpt-4o"] == 1
    assert snapshot["cb_open_total"]["llm_router|llm_router:gpt-4o"] == 1
    assert snapshot["cb_reject_total"]["llm_router|llm_router:gpt-4o"] == 1
    assert snapshot["cb_half_open_probe_total"]["llm_router|llm_router:gpt-4o|failure"] == 1
