# Adding New Models to OmniExtract Gateway

OmniExtract Gateway uses a **dynamic model registry** (`registry/models.yaml`) so new models can be added via Pull Request — no code changes required.

## Quick Guide

1. Open `registry/models.yaml`.
2. Find the provider section or add a new one.
3. Add your model following this schema:

```yaml
providers:
  provider_name:
    models:
      - id: model-identifier          # used in ExtractionRequest.engine_config.model
        vision: true                  # true if model accepts image input
        context_window: 128000        # max tokens
```

4. Submit a PR with title: `registry: add <model-id>`.

## Guidelines

- `id` must match the identifier used by LiteLLM for that provider/model combination.
- Set `vision: true` only for models that accept image or document input (multimodal).
- For local models, add `requires_gpu: true/false`.

## Testing a New Model

After adding to the registry, you can test via the API:

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "document": "<base64_image>",
    "engine_config": {
      "provider": "llm_router",
      "model": "your-new-model-id",
      "api_keys": { "provider_name": "your-api-key" }
    },
    "extraction_target": { "document_type": "invoice" }
  }'
```

## Supported Providers

See `registry/models.yaml` for the full current list. Current providers include:

- `anthropic` — Claude family
- `openai` — GPT / o-series
- `google` — Gemini family
- `deepseek` — DeepSeek models
- `qwen` — Qwen/Alibaba models
- `mistral` — Mistral / Pixtral
- `meta` — Llama family
- `microsoft` — Phi family
- `cohere` — Command family
- `ai21` — Jamba family
- `local` — Self-hosted models (via Worker container)
