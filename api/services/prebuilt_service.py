"""Prebuilt template service — loads YAML templates and builds LLM prompts."""

from __future__ import annotations

from pathlib import Path

import yaml

from api.core.config import settings
from api.core.exceptions import PrebuiltNotFoundError

_PREBUILT_DIR = Path(settings.prebuilts_path)


async def get_all_prebuilts() -> list[dict]:
    """Return metadata for all available prebuilt templates."""
    templates = []
    for path in sorted(_PREBUILT_DIR.glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
            templates.append(
                {
                    "id": data.get("id", path.stem),
                    "display_name": data.get("display_name", path.stem),
                    "version": data.get("version", "1.0"),
                    "required_fields": data.get("required_fields", []),
                }
            )
    return templates


async def load_prebuilt(document_type: str) -> dict:
    """
    Load a single prebuilt template by its ID.

    Raises:
        PrebuiltNotFoundError: If the template file does not exist.
    """
    path = _PREBUILT_DIR / f"{document_type}.yaml"
    if not path.exists():
        # Also check custom subdirectory
        path = _PREBUILT_DIR / "custom" / f"{document_type}.yaml"
    if not path.exists():
        raise PrebuiltNotFoundError(document_type)

    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


async def register_custom_prebuilt(id: str, display_name: str, fields: list[str]) -> dict:
    """
    Auto-generate an LLM prompt for a custom prebuilt and persist it.

    Returns the generated template dict.

    Raises:
        ValueError: If the provided id contains invalid characters.
    """
    # Sanitize id: only allow alphanumeric characters, underscores, and hyphens.
    import re

    if not re.fullmatch(r"[a-zA-Z0-9_\-]+", id):
        raise ValueError(
            "Custom prebuilt id must contain only alphanumeric characters, "
            "underscores, or hyphens."
        )

    fields_list = "\n".join(f"  - {f}" for f in fields)
    system_prompt = (
        "You are a specialized document extraction engine. "
        f"Extract the following fields from the document image and return a JSON object "
        f"strictly conforming to the StandardizedExtraction schema.\n"
        f"Required fields:\n{fields_list}\n"
        "For each field, provide the value and, if the model supports spatial reasoning, "
        "include normalized bounding_box coordinates [0, 1]."
    )

    template = {
        "id": id,
        "display_name": display_name,
        "version": "1.0",
        "system_prompt": system_prompt,
        "required_fields": fields,
        "output_schema": "StandardizedExtraction",
    }

    custom_dir = _PREBUILT_DIR / "custom"
    custom_dir.mkdir(parents=True, exist_ok=True)
    out_path = (custom_dir / f"{id}.yaml").resolve()
    # Ensure the resolved path is still inside the custom directory (defense in depth).
    if not str(out_path).startswith(str(custom_dir.resolve())):
        raise ValueError("Invalid custom prebuilt id: path traversal detected.")
    with out_path.open("w", encoding="utf-8") as fh:
        yaml.dump(template, fh, allow_unicode=True, sort_keys=False)

    return template
