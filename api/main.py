"""OmniExtract Gateway — FastAPI application entrypoint."""

from fastapi import FastAPI

from api.routers import extract, prebuilts, registry

app = FastAPI(
    title="OmniExtract Gateway",
    description=(
        "Unified document extraction meta-gateway. "
        "Route extraction requests to AWS Textract, Azure Document Intelligence, "
        "GCP Document AI, LiteLLM-powered LLMs, or local vision models — "
        "all returning the same standardized JSON schema."
    ),
    version="0.1.0",
    license_info={"name": "MIT"},
)

app.include_router(extract.router, prefix="/extract", tags=["Extraction"])
app.include_router(prebuilts.router, prefix="/prebuilts", tags=["Prebuilts"])
app.include_router(registry.router, prefix="/registry", tags=["Registry"])


@app.get("/health", tags=["Health"])
async def health() -> dict:
    return {"status": "ok"}
