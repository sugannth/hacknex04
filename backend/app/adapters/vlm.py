import os
from typing import Any, Dict

from app.adapters.base import VLMAdapter


class BasicVLMAdapter(VLMAdapter):
    """
    Vision-language model adapter.

    This is intentionally provider-neutral.

    During the hackathon we can connect a real VLM later without
    changing the API or pipeline contract.
    """

    def __init__(self):
        self.provider = os.getenv("VLM_PROVIDER", "none")

    def analyze(self, image: Any, ocr_text: str = "") -> Dict:

        if self.provider.lower() == "none":
            return {
                "text": "",
                "confidence": 0.0,
                "available": False,
                "engine": "fallback",
                "message": "VLM provider not configured.",
            }

        # Provider-specific implementation will be plugged in here.
        # The output contract stays unchanged.

        return {
            "text": "",
            "confidence": 0.0,
            "available": False,
            "engine": self.provider,
            "message": "VLM provider configured but adapter implementation is pending.",
        }