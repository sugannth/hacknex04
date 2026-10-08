import os
from typing import Any, Dict

import pytesseract

from app.adapters.base import OCRAdapter


class BasicOCRAdapter(OCRAdapter):
    def __init__(self):
        self.use_tesseract = (
            os.getenv("USE_TESSERACT", "false").strip().lower() == "true"
        )

    def recognize(self, image: Any) -> Dict:
        if not self.use_tesseract:
            return {
                "text": "",
                "confidence": 0.0,
                "available": False,
                "engine": "fallback",
                "message": "Tesseract OCR is disabled.",
            }

        try:
            version = str(pytesseract.get_tesseract_version())

            text = pytesseract.image_to_string(
                image,
                config="--psm 6",
            ).strip()

            if not text:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "available": True,
                    "engine": "tesseract",
                    "version": version,
                    "message": "Tesseract ran successfully but detected no text.",
                }

            return {
                "text": text,
                "confidence": 0.65,
                "available": True,
                "engine": "tesseract",
                "version": version,
            }

        except Exception as exc:
            return {
                "text": "",
                "confidence": 0.0,
                "available": False,
                "engine": "tesseract",
                "error": str(exc),
            }