from typing import Dict

from app.adapters.ocr import BasicOCRAdapter
from app.adapters.vlm import BasicVLMAdapter
from app.adapters.llm import BasicLLMAdapter

from app.pipeline.preprocessing import preprocess_image
from app.pipeline.uncertainty import (
    calculate_agreement,
    calculate_confidence,
    classify_confidence,
    uncertainty_reason,
)


class HandwritingPipeline:
    """
    Main handwriting digitization pipeline.

    Flow:

        Image
          ↓
        Preprocessing
          ↓
        OCR
          ↓
        VLM
          ↓
        Evidence Fusion
          ↓
        Contextual Correction
          ↓
        Confidence
          ↓
        Uncertainty
          ↓
        Structured Result
    """

    def __init__(self):
        self.ocr = BasicOCRAdapter()
        self.vlm = BasicVLMAdapter()
        self.llm = BasicLLMAdapter()

    def process(self, image_path: str) -> Dict:
        """
        Process one handwriting image and return
        a structured result.
        """

        # =====================================================
        # 1. PREPROCESSING
        # =====================================================

        preprocessing = preprocess_image(
            image_path=image_path
        )

        processed_image = preprocessing["processed_image"]

        preprocessing_metadata = {
            "original_width": preprocessing["original_width"],
            "original_height": preprocessing["original_height"],
            "processed_width": preprocessing["processed_width"],
            "processed_height": preprocessing["processed_height"],
            "format": preprocessing["format"],
        }

        # =====================================================
        # 2. OCR
        # =====================================================

        ocr_result = self.ocr.recognize(
            processed_image
        )

        ocr_text = (
            ocr_result.get("text") or ""
        ).strip()

        ocr_confidence = float(
            ocr_result.get(
                "confidence",
                0.0
            )
        )

        # =====================================================
        # 3. VLM
        # =====================================================

        vlm_result = self.vlm.analyze(
            processed_image,
            ocr_text=ocr_text,
        )

        vlm_text = (
            vlm_result.get("text") or ""
        ).strip()

        vlm_confidence = float(
            vlm_result.get(
                "confidence",
                0.0
            )
        )

        # =====================================================
        # 4. EVIDENCE AGREEMENT
        # =====================================================

        agreement_score = calculate_agreement(
            ocr_text=ocr_text,
            vlm_text=vlm_text,
        )

        # =====================================================
        # 5. CONTEXTUAL CORRECTION
        # =====================================================

        correction_result = self.llm.correct(
            ocr_text=ocr_text,
            vlm_text=vlm_text,
        )

        corrected_text = (
            correction_result.get("text")
            or ocr_text
            or vlm_text
            or ""
        ).strip()

        # =====================================================
        # 6. FINAL CONFIDENCE
        # =====================================================

        final_confidence = calculate_confidence(
            ocr_confidence=ocr_confidence,
            vlm_confidence=vlm_confidence,
            agreement_score=agreement_score,
        )

        status = classify_confidence(
            final_confidence
        )

        reason = uncertainty_reason(
            ocr_text=ocr_text,
            vlm_text=vlm_text,
            confidence=final_confidence,
        )

        # =====================================================
        # 7. REGION
        # =====================================================

        region = {
            "region_id": "region-1",

            "bbox": {
                "x": 0,
                "y": 0,
                "width": preprocessing["original_width"],
                "height": preprocessing["original_height"],
            },

            "ocr_text": ocr_text,

            "vlm_text": vlm_text,

            "corrected_text": corrected_text,

            "ocr_confidence": round(
                ocr_confidence,
                3
            ),

            "vlm_confidence": round(
                vlm_confidence,
                3
            ),

            "agreement_score": round(
                agreement_score,
                3
            ),

            "final_confidence": round(
                final_confidence,
                3
            ),

            "status": status,

            "reason": reason,
        }

        # =====================================================
        # 8. UNCERTAIN REGIONS
        # =====================================================

        uncertain_regions = []

        if status != "verified":

            uncertain_regions.append(
                {
                    "region_id": "region-1",
                    "text": corrected_text,
                    "confidence": round(
                        final_confidence,
                        3
                    ),
                    "reason": reason,
                }
            )

        # =====================================================
        # 9. FINAL RESULT
        # =====================================================

        result = {
            "text": corrected_text,

            "overall_confidence": round(
                final_confidence,
                3
            ),

            "status": status,

            "regions": [
                region
            ],

            "uncertain_regions": uncertain_regions,

            "evidence": {
                "ocr_text": ocr_text,
                "vlm_text": vlm_text,
                "corrected_text": corrected_text,

                "ocr_available": bool(
                    ocr_result.get(
                        "available",
                        False
                    )
                ),

                "vlm_available": bool(
                    vlm_result.get(
                        "available",
                        False
                    )
                ),

                "llm_available": bool(
                    correction_result.get(
                        "available",
                        False
                    )
                ),
            },

            "preprocessing": preprocessing_metadata,
        }

        return result


pipeline = HandwritingPipeline()