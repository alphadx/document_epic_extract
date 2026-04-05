"""Unit tests for LLM parsing and prompt helper functions."""

from __future__ import annotations

import pytest

from adapters.llm.parsing import (
    extract_json_substring,
    parse_standardized_extraction,
    resolve_document_url,
    safe_api_kwargs,
)
from api.core.exceptions import ExtractionError


class TestParseStandardizedExtraction:
    def test_parses_plain_json(self):
        content = (
            '{"raw_text":"hello","fields":[],"tables":[],"engine_used":"llm_router:gpt-4o"}'
        )
        parsed = parse_standardized_extraction(content, engine_used="llm_router:gpt-4o")
        assert parsed.raw_text == "hello"
        assert parsed.engine_used == "llm_router:gpt-4o"

    def test_parses_json_embedded_in_text(self):
        content = (
            "Resultado:\n```json\n"
            '{"raw_text":"invoice","fields":[],"tables":[],"engine_used":""}'
            "\n```"
        )
        parsed = parse_standardized_extraction(content, engine_used="llm_router:mock")
        assert parsed.raw_text == "invoice"
        assert parsed.engine_used == "llm_router:mock"

    def test_raises_on_non_json(self):
        with pytest.raises(ExtractionError):
            parse_standardized_extraction("sin json", engine_used="llm_router:mock")

    def test_extract_json_substring_handles_braces_in_text(self):
        content = 'preface {not-json} and then {"raw_text":"x","fields":[],"tables":[],"engine_used":""}'
        extracted = extract_json_substring(content)
        assert extracted.startswith('{"raw_text"')

    def test_parse_normalizes_fields_dict(self):
        content = '{"raw_text":"x","fields":{"invoice_number":"123"},"tables":[],"engine_used":""}'
        parsed = parse_standardized_extraction(content, engine_used="llm_router:mock")
        assert parsed.fields[0].key == "invoice_number"
        assert parsed.fields[0].value == "123"


class TestHelpers:
    def test_resolve_document_url_keeps_data_url(self):
        data_url = "data:image/jpeg;base64,abc"
        assert resolve_document_url(data_url) == data_url

    def test_safe_api_kwargs_filters_reserved(self):
        payload = {
            "api_key": "k",
            "model": "hack",
            "messages": "hack",
            "timeout": "hack",
            "custom_header": "ok",
        }
        safe = safe_api_kwargs(payload)
        assert "model" not in safe
        assert "messages" not in safe
        assert "timeout" not in safe
        assert safe["api_key"] == "k"
        assert safe["custom_header"] == "ok"
