"""Demo component: bounding box renderer over the original image."""

from __future__ import annotations

from io import BytesIO

import streamlit as st
from PIL import Image, ImageDraw, UnidentifiedImageError


def render_bboxes(image_bytes: bytes, fields: list[dict]) -> None:
    """
    Overlay bounding boxes on the original image and display it.

    Args:
        image_bytes: Raw bytes of the original document image.
        fields: List of ExtractedField dicts with optional bounding_box.
    """
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        st.info("Preview no disponible para este archivo (ej. PDF sin rasterización).")
        return

    draw = ImageDraw.Draw(img)
    w, h = img.size

    for field in fields:
        bb = field.get("bounding_box")
        if not bb:
            continue
        x0, y0, x1, y1 = bb["x0"] * w, bb["y0"] * h, bb["x1"] * w, bb["y1"] * h
        draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
        draw.text((x0 + 2, y0 + 2), field.get("key", ""), fill="red")

    st.image(img, use_column_width=True)
