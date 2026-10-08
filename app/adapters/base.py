from abc import ABC, abstractmethod
from typing import Any, Dict


class OCRAdapter(ABC):

    @abstractmethod
    def recognize(self, image: Any) -> Dict:
        """
        Recognize handwriting/text from an image.
        """
        raise NotImplementedError


class VLMAdapter(ABC):

    @abstractmethod
    def analyze(self, image: Any, ocr_text: str = "") -> Dict:
        """
        Analyze handwriting using a vision-language model.
        """
        raise NotImplementedError


class LLMAdapter(ABC):

    @abstractmethod
    def correct(
        self,
        ocr_text: str,
        vlm_text: str,
        context: str = "",
    ) -> Dict:
        """
        Correct OCR/VLM output using contextual reasoning.

        Important:
        The LLM must not invent text when evidence is insufficient.
        """
        raise NotImplementedError