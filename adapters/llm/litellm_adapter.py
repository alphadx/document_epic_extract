"""LiteLLM Vision adapter — routes LLM requests and parses structured output."""

from __future__ import annotations

from adapters.base import BaseAdapter
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction


class LiteLLMVisionAdapter(BaseAdapter):
    """
    Adapter for LLM-based extraction via LiteLLM.

    Supports 100+ models (OpenAI, Anthropic, Google, DeepSeek, Qwen,
    Mistral, and more) through a unified LiteLLM interface.

    Workflow:
        1. Look up the prebuilt template for the requested document_type.
        2. Assemble the prompt: [System Prompt] + [JSON Schema] + [Image].
        3. Call litellm.acompletion() with the assembled messages.
        4. Parse the JSON response into StandardizedExtraction.

    Requirements:
        litellm >= 1.30  (add to pyproject.toml)
    """

    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        # TODO: Implement Phase 3 — LiteLLM Vision integration
        # 1. Load prebuilt template via PrebuiltService.
        # 2. Build messages: system prompt + image content.
        # 3. Call litellm.acompletion(model=..., messages=..., response_format=...).
        # 4. Parse JSON response into StandardizedExtraction.
        raise NotImplementedError(
            "LiteLLMVisionAdapter is not yet implemented. "
            "Tracked in Phase 3 of the project roadmap."
        )
