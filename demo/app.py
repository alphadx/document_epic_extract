"""OmniExtract Gateway — Streamlit Demo Application."""

import streamlit as st

from demo.components.api_client import build_extract_payload, call_extract
from demo.components.comparison_panel import show_comparison
from demo.components.uploader import encode_document

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

if "extraction_result" not in st.session_state:
    st.session_state.extraction_result = None

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
    engine_b_provider = ""
    engine_b_model = ""
    engine_b_key = ""
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
    with st.spinner("Extracting..."):
        doc_b64 = encode_document(uploaded_file)
        custom_fields = (
            [f.strip() for f in custom_fields_input.splitlines() if f.strip()]
            if doc_type == "free"
            else None
        )

        payload_a = build_extract_payload(
            document_b64=doc_b64,
            provider=engine_a_provider,
            model=engine_a_model,
            api_key=engine_a_key,
            document_type=doc_type,
            custom_fields=custom_fields,
        )

        response_a = call_extract(api_url=api_url, payload=payload_a)
        result_a = response_a.payload if response_a.ok else None

        if not response_a.ok:
            st.error(f"Engine A failed: {response_a.error}")

        result_b = None
        response_b_error = None
        if enable_b and result_a:
            payload_b = build_extract_payload(
                document_b64=doc_b64,
                provider=engine_b_provider,
                model=engine_b_model,
                api_key=engine_b_key,
                document_type=doc_type,
                custom_fields=custom_fields,
            )
            response_b = call_extract(api_url=api_url, payload=payload_b)
            result_b = response_b.payload if response_b.ok else None
            if not response_b.ok:
                response_b_error = response_b.error
                st.warning(f"Engine B failed: {response_b.error}")

        st.session_state.extraction_result = {
            "uploaded_file": uploaded_file,
            "result_a": result_a,
            "result_b": result_b,
            "label_a": f"{engine_a_provider} / {engine_a_model}",
            "label_b": f"{engine_b_provider} / {engine_b_model}" if enable_b else None,
            "error_a": response_a.error if not response_a.ok else None,
            "error_b": response_b_error,
        }

stored = st.session_state.extraction_result
if stored and stored.get("result_a"):
    st.success("Extraction complete!")
    show_comparison(
        uploaded_file=stored["uploaded_file"],
        result_a=stored["result_a"],
        result_b=stored.get("result_b"),
        label_a=stored["label_a"],
        label_b=stored.get("label_b"),
    )
elif uploaded_file is None:
    st.info("👆 Upload a document to get started.")
