"""Registry service — reads the dynamic model registry from YAML."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from api.core.config import settings


@lru_cache(maxsize=1)
def _load_registry() -> dict:
    path = Path(settings.registry_path)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


async def get_all_models() -> dict:
    """Return the full model registry grouped by provider."""
    return _load_registry()
