"""Demo component: document uploader utilities."""

from __future__ import annotations

import base64
from io import BytesIO

from streamlit.runtime.uploaded_file_manager import UploadedFile


def encode_document(uploaded_file: UploadedFile) -> str:
    """Return the uploaded file as a Base64-encoded string."""
    return base64.b64encode(uploaded_file.read()).decode("utf-8")
