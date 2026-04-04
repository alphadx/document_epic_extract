"""OmniExtract Gateway — Streamlit Demo Application."""

import streamlit as st

st.set_page_config(
    page_title="OmniExtract Gateway Demo",
    page_icon="📄",
    layout="wide",
)

st.title("📄 OmniExtract Gateway — Demo")
st.caption(
    "Unified document extraction: compare OCR cloud providers and LLMs "
    "side-by-side with a single standardized output schema."
)

# ── Sidebar: Engine Configuration ────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Engine Configuration")

    st.subheader("Engine A")
    engine_a_provider = st.selectbox(
        "Provider A",
        ["aws", "gcp", "azure", "llm_router", "local"],
        key="engine_a_provider",
    )
    engine_a_model = st.text_input("Model A", value="claude-3-5-sonnet-20241022", key="engine_a_model")
    engine_a_key = st.text_input("API Key A", type="password", key="engine_a_key")

    st.divider()

    st.subheader("Engine B (optional)")
    enable_b = st.checkbox("Enable side-by-side comparison", value=False)
    if enable_b:
        engine_b_provider = st.selectbox(
            "Provider B",
            ["aws", "gcp", "azure", "llm_router", "local"],
            key="engine_b_provider",
        )
        engine_b_model = st.text_input("Model B", value="gpt-4o", key="engine_b_model")
        engine_b_key = st.text_input("API Key B", type="password", key="engine_b_key")

    st.divider()
    api_url = st.text_input("API Gateway URL", value="http://localhost:8000")

# ── Main Area ─────────────────────────────────────────────────────────────────
col_upload, col_target = st.columns([2, 1])

with col_upload:
    st.subheader("1. Upload Document")
    uploaded_file = st.file_uploader(
        "Upload an image or PDF",
        type=["png", "jpg", "jpeg", "pdf", "tiff", "webp"],
    )

with col_target:
    st.subheader("2. Extraction Target")
    doc_type = st.selectbox(
        "Document Type (Prebuilt)",
        ["invoice", "receipt", "id_card", "bank_statement", "customs_declaration", "free"],
    )
    custom_fields_input = ""
    if doc_type == "free":
        custom_fields_input = st.text_area(
            "Custom fields (one per line)",
            placeholder="field_name_1\nfield_name_2",
        )

# ── Extraction Button ─────────────────────────────────────────────────────────
st.divider()
if st.button("🚀 Extract", type="primary", disabled=uploaded_file is None):
    from demo.components.uploader import encode_document
    from demo.components.bbox_renderer import render_bboxes
    from demo.components.comparison_panel import show_comparison

    with st.spinner("Extracting..."):
        import base64
        import httpx

        doc_b64 = encode_document(uploaded_file)
        custom_fields = (
            [f.strip() for f in custom_fields_input.splitlines() if f.strip()]
            if doc_type == "free"
            else None
        )

        payload = {
            "document": doc_b64,
            "engine_config": {
                "provider": engine_a_provider,
                "model": engine_a_model,
                "api_keys": {engine_a_provider: engine_a_key} if engine_a_key else {},
            },
            "extraction_target": {
                "document_type": doc_type,
                "custom_fields": custom_fields,
            },
        }

        try:
            resp_a = httpx.post(f"{api_url}/extract", json=payload, timeout=60)
            result_a = resp_a.json()
        except Exception as exc:
            st.error(f"Engine A failed: {exc}")
            result_a = None

        result_b = None
        if enable_b and result_a:
            payload_b = {**payload}
            payload_b["engine_config"] = {
                "provider": engine_b_provider,
                "model": engine_b_model,
                "api_keys": {engine_b_provider: engine_b_key} if engine_b_key else {},
            }
            try:
                resp_b = httpx.post(f"{api_url}/extract", json=payload_b, timeout=60)
                result_b = resp_b.json()
            except Exception as exc:
                st.warning(f"Engine B failed: {exc}")

    if result_a:
        st.success("Extraction complete!")
        show_comparison(
            uploaded_file=uploaded_file,
            result_a=result_a,
            result_b=result_b,
            label_a=f"{engine_a_provider} / {engine_a_model}",
            label_b=f"{engine_b_provider} / {engine_b_model}" if enable_b else None,
        )
else:
    if uploaded_file is None:
        st.info("👆 Upload a document to get started.")
