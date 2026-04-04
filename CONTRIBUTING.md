# Contributing to OmniExtract Gateway

First of all — thank you for your interest in contributing! 🎉

OmniExtract Gateway is an open-source project and we welcome contributions of all kinds: bug fixes, new engine adapters, new prebuilt templates, documentation improvements, and new model registry entries.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Adding a New Model to the Registry](#adding-a-new-model-to-the-registry)
5. [Creating a New Engine Adapter](#creating-a-new-engine-adapter)
6. [Adding a Prebuilt Template](#adding-a-prebuilt-template)
7. [Running Tests](#running-tests)
8. [Pull Request Guidelines](#pull-request-guidelines)

---

## Code of Conduct

Be respectful. See [Contributor Covenant](https://www.contributor-covenant.org/) for guidelines.

---

## How to Contribute

1. **Fork** the repository.
2. **Create a branch** from `main`: `git checkout -b feat/my-feature`.
3. Make your changes following the guidelines below.
4. **Run tests** and linting before opening a PR.
5. Open a **Pull Request** with a clear description of what you changed and why.

---

## Development Setup

```bash
# Clone your fork
git clone https://github.com/<your-username>/document_epic_extract.git
cd document_epic_extract

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with all dev dependencies
pip install -e ".[dev,api,aws,gcp,azure]"

# Copy environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the API locally
uvicorn api.main:app --reload
```

---

## Adding a New Model to the Registry

This is the simplest contribution and **requires no code changes**.

1. Open `registry/models.yaml`.
2. Find the relevant provider section (or add a new one).
3. Add your model entry:

```yaml
providers:
  my_provider:
    models:
      - id: my-model-name-v1
        vision: true        # Does it support image input?
        context_window: 128000
```

4. Open a PR with a title like `registry: add my-model-name-v1`.

---

## Creating a New Engine Adapter

1. Choose the appropriate subdirectory:
   - `adapters/ocr/` — Cloud OCR providers
   - `adapters/llm/` — LLM-based adapters
   - `adapters/local/` — Locally hosted models

2. Create your adapter class inheriting from `BaseAdapter`:

```python
# adapters/ocr/my_provider.py
from adapters.base import BaseAdapter
from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction

class MyProviderAdapter(BaseAdapter):
    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        # Your implementation here
        ...
```

3. Register the adapter in `api/services/router_service.py`:

```python
_ADAPTER_MAP = {
    ...
    "my_provider": "adapters.ocr.my_provider.MyProviderAdapter",
}
```

4. Add any new dependencies to the appropriate `pyproject.toml` optional group.

5. Add unit tests in `tests/unit/adapters/`.

---

## Adding a Prebuilt Template

1. Create a new YAML file in `prebuilts/`:

```yaml
# prebuilts/my_document.yaml
id: my_document
display_name: "My Document Type"
version: "1.0"
system_prompt: |
  You are a specialized document extraction engine...
  [Your optimized extraction prompt here]
required_fields:
  - field_one
  - field_two
output_schema: "StandardizedExtraction"
```

2. Test the template with at least one LLM (GPT-4o or Claude 3.5 Sonnet recommended).
3. Open a PR describing the document type and any prompt engineering choices.

---

## Running Tests

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=api --cov=adapters --cov-report=html

# Lint with ruff
ruff check .

# Type check with mypy
mypy api/ adapters/
```

---

## Pull Request Guidelines

- Keep PRs focused. One feature / fix per PR.
- Write a clear PR description explaining the motivation and approach.
- Ensure all tests pass and linting is clean.
- Add or update tests for any new behavior.
- For new adapters, include mock-based integration tests.
- For registry updates, no tests required — just verify the YAML is valid.

Thank you for making OmniExtract Gateway better! 🚀
