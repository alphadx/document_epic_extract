"""Demo component: side-by-side comparison panel."""

from __future__ import annotations

import streamlit as st

from demo.components.bbox_renderer import render_bboxes


def show_comparison(
    uploaded_file,
    result_a: dict,
    result_b: dict | None,
    label_a: str,
    label_b: str | None,
) -> None:
    """
    Render extraction results in a side-by-side layout.

    Displays the annotated image, extracted fields, and raw JSON
    for each engine result.
    """
    image_bytes = uploaded_file.getvalue()

    if result_b and label_b:
        col_a, col_b = st.columns(2)
    else:
        col_a = st.container()
        col_b = None

    with col_a:
        st.subheader(f"Engine A: {label_a}")
        _show_result(image_bytes, result_a)

    if col_b and result_b:
        with col_b:
            st.subheader(f"Engine B: {label_b}")
            _show_result(image_bytes, result_b)


def _format_confidence(confidence: float | None) -> str:
    """Format confidence preserving valid `0.0` values."""
    if confidence is None:
        return "—"
    return f"{confidence:.0%}"


def _show_result(image_bytes: bytes, result: dict) -> None:
    tab_visual, tab_fields, tab_json = st.tabs(["🖼️ Visual", "📋 Fields", "{ } JSON"])

    with tab_visual:
        render_bboxes(image_bytes, result.get("fields", []))

    with tab_fields:
        fields = result.get("fields", [])
        if fields:
            st.dataframe(
                [
                    {
                        "Field": f.get("key"),
                        "Value": f.get("value"),
                        "Confidence": _format_confidence(f.get("confidence")),
                    }
                    for f in fields
                ]
            )
        else:
            st.info("No fields extracted.")

        tables = result.get("tables", [])
        for i, table in enumerate(tables):
            st.caption(f"Table {i + 1} — {table['rows']} rows × {table['cols']} cols")

    with tab_json:
        st.json(result)
        st.caption(f"⏱ {result.get('processing_time_ms', '—')} ms · engine: {result.get('engine_used', '—')}")
