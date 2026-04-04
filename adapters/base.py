"""Abstract base class for all engine adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from api.schemas.request import ExtractionRequest
from api.schemas.response import StandardizedExtraction


class BaseAdapter(ABC):
    """
    All engine adapters must implement this interface.

    The :meth:`extract` method receives a validated :class:`ExtractionRequest`
    and must return a :class:`StandardizedExtraction` — the unified output schema
    shared across every provider.
    """

    @abstractmethod
    async def extract(self, request: ExtractionRequest) -> StandardizedExtraction:
        """
        Perform document extraction and return a standardized result.

        Args:
            request: The validated extraction request containing the document,
                     engine configuration, and extraction target.

        Returns:
            A :class:`StandardizedExtraction` with raw text, key-value fields,
            tables, and optional bounding boxes.
        """
