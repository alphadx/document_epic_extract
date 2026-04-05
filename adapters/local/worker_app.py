"""Local Worker FastAPI app for CPU/GPU document inference."""

from __future__ import annotations

import base64
import os
import re
from functools import lru_cache
from io import BytesIO
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from api.core.exceptions import ExtractionError
from api.schemas.response import StandardizedExtraction

app = FastAPI(
    title="OmniExtract Local Worker",
    version="0.1.0",
    description="Worker service for local model inference (CPU/GPU).",
)


class WorkerEngineConfig(BaseModel):
    provider: str = "local"
    model: str
    custom_endpoint: str | None = None


class WorkerExtractionTarget(BaseModel):
    document_type: str
    custom_fields: list[str] | None = None


class WorkerInferRequest(BaseModel):
    document: str = Field(..., description="Base64 document payload or URL.")
    engine_config: WorkerEngineConfig
    extraction_target: WorkerExtractionTarget


class WorkerInferResponse(BaseModel):
    result: StandardizedExtraction
    backend: str
    device: str


def _is_probable_url(document: str) -> bool:
    return document.startswith("http://") or document.startswith("https://")


def _decode_base64_text(document: str) -> str:
    try:
        decoded = base64.b64decode(document, validate=True)
    except Exception:  # noqa: BLE001
        return ""
    try:
        return decoded.decode("utf-8", errors="ignore").strip()
    except Exception:  # noqa: BLE001
        return ""


def _extract_kv_fields(raw_text: str) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    for line in raw_text.splitlines():
        match = re.match(r"^\s*([A-Za-z0-9_\- ]{2,60})\s*[:=]\s*(.+?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        fields.append({"key": key.strip().lower().replace(" ", "_"), "value": value.strip()})
    return fields


@lru_cache(maxsize=1)
def _load_smolvlm2_pipeline() -> tuple[Any, Any, str] | None:
    try:
        import torch
        from transformers import AutoModelForVision2Seq, AutoProcessor

        model_id = os.getenv("LOCAL_WORKER_MODEL_ID", "HuggingFaceTB/SmolVLM2-2.2B-Instruct")
        requested_device = os.getenv("LOCAL_WORKER_DEVICE", "auto").lower()
        if requested_device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            device = requested_device

        processor = AutoProcessor.from_pretrained(model_id)
        model = AutoModelForVision2Seq.from_pretrained(model_id)
        model.to(device)
        return processor, model, device
    except Exception:  # noqa: BLE001
        return None


def _smolvlm2_infer(document: str) -> tuple[str, str]:
    pipeline = _load_smolvlm2_pipeline()
    if pipeline is None:
        return "", "cpu"

    processor, model, device = pipeline
    try:
        import torch
        from PIL import Image
    except Exception as exc:  # noqa: BLE001
        raise ExtractionError("Pillow/torch are required for SmolVLM2 inference.") from exc

    if _is_probable_url(document):
        raise ExtractionError("Worker SmolVLM2 backend requires base64 image input.")

    try:
        raw = base64.b64decode(document, validate=True)
        image = Image.open(BytesIO(raw)).convert("RGB")
    except Exception as exc:  # noqa: BLE001
        raise ExtractionError("Invalid base64 image for local SmolVLM2 inference.") from exc

    prompt = "Extract document text and key fields."
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        output_tokens = model.generate(**inputs, max_new_tokens=int(os.getenv("LOCAL_WORKER_MAX_NEW_TOKENS", "256")))
    generated = processor.batch_decode(output_tokens, skip_special_tokens=True)
    text = generated[0].strip() if generated else ""
    return text, device


def _heuristic_infer(document: str) -> tuple[str, str]:
    if _is_probable_url(document):
        return f"remote_document: {document}", os.getenv("LOCAL_WORKER_DEVICE", "cpu")
    return _decode_base64_text(document), os.getenv("LOCAL_WORKER_DEVICE", "cpu")


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/infer", response_model=WorkerInferResponse, tags=["Inference"])
async def infer(request: WorkerInferRequest) -> WorkerInferResponse:
    backend = os.getenv("LOCAL_WORKER_BACKEND", "heuristic").lower()

    if backend == "smolvlm2":
        raw_text, device = _smolvlm2_infer(request.document)
    else:
        raw_text, device = _heuristic_infer(request.document)

    result = StandardizedExtraction(
        raw_text=raw_text,
        fields=_extract_kv_fields(raw_text),
        tables=[],
        engine_used=f"local_worker:{request.engine_config.model}",
    )
    return WorkerInferResponse(result=result, backend=backend, device=device)
