FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including git for model downloads)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[worker]"

# Copy worker sources (worker app depends on shared API schemas/exceptions)
COPY api/ ./api/
COPY adapters/ ./adapters/

# Pre-download model weights at build time (optional, speeds up startup)
# RUN python -c "from transformers import AutoProcessor, AutoModelForVision2Seq; \
#     AutoProcessor.from_pretrained('HuggingFaceTB/SmolVLM2-2.2B-Instruct'); \
#     AutoModelForVision2Seq.from_pretrained('HuggingFaceTB/SmolVLM2-2.2B-Instruct')"

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["uvicorn", "adapters.local.worker_app:app", "--host", "0.0.0.0", "--port", "8001"]
