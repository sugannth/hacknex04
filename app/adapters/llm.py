import os
from typing import Dict

from app.adapters.base import LLMAdapter


class BasicLLMAdapter(LLMAdapter):
    """
    Context-aware correction adapter.

    Important design rule:

    The LLM is NOT allowed to freely rewrite handwriting.

    It should only correct text when OCR/VLM evidence supports
    the correction. Otherwise uncertainty is preserved.
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "none")

    def correct(
        self,
        ocr_text: str,
        vlm_text: str,
        context: str = "",
    ) -> Dict:

        ocr_text = (ocr_text or "").strip()
        vlm_text = (vlm_text or "").strip()

        if not ocr_text and not vlm_text:
            return {
                "text": "",
                "confidence": 0.0,
                "available": False,
                "changed": False,
                "engine": "fallback",
                "reason": "No OCR or VLM evidence available.",
            }

        # Strong evidence agreement:
        if ocr_text and vlm_text and ocr_text.lower() == vlm_text.lower():
            return {
                "text": ocr_text,
                "confidence": 0.90,
                "available": False,
                "changed": False,
                "engine": "evidence-fusion",
                "reason": "OCR and VLM outputs agree.",
            }

        # If only OCR exists, preserve it rather than hallucinating.
        if ocr_text and not vlm_text:
            return {
                "text": ocr_text,
                "confidence": 0.55,
                "available": False,
                "changed": False,
                "engine": "ocr-preservation",
                "reason": "Only OCR evidence available.",
            }

        # If only VLM exists, preserve it but lower confidence.
        if vlm_text and not ocr_text:
            return {
                "text": vlm_text,
                "confidence": 0.55,
                "available": False,
                "changed": False,
                "engine": "vlm-preservation",
                "reason": "Only VLM evidence available.",
            }

        # Disagreement:
        # Do NOT arbitrarily choose one.
        return {
            "text": ocr_text,
            "confidence": 0.35,
            "available": False,
            "changed": False,
            "engine": "uncertain-fusion",
            "reason": "OCR and VLM disagree; correction withheld.",
        }