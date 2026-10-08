from typing import Dict


def calculate_agreement(ocr_text: str, vlm_text: str) -> float:
    """
    Calculate a simple normalized agreement score.

    This is a hackathon heuristic, not a calibrated probability.
    """

    ocr_text = (ocr_text or "").strip().lower()
    vlm_text = (vlm_text or "").strip().lower()

    if not ocr_text and not vlm_text:
        return 0.0

    if ocr_text == vlm_text:
        return 1.0

    if not ocr_text or not vlm_text:
        return 0.0

    # Character-level overlap heuristic.
    max_length = max(len(ocr_text), len(vlm_text))

    if max_length == 0:
        return 0.0

    matches = sum(
        1
        for a, b in zip(ocr_text, vlm_text)
        if a == b
    )

    return matches / max_length


def calculate_confidence(
    ocr_confidence: float,
    vlm_confidence: float,
    agreement_score: float,
) -> float:
    """
    Evidence-fusion confidence.

    We intentionally keep this interpretable:

    OCR      = 40%
    VLM      = 35%
    Agreement = 25%

    This should later be calibrated against the hackathon
    development dataset.
    """

    score = (
        (ocr_confidence * 0.40)
        + (vlm_confidence * 0.35)
        + (agreement_score * 0.25)
    )

    return round(max(0.0, min(1.0, score)), 3)


def classify_confidence(confidence: float) -> str:

    if confidence >= 0.80:
        return "verified"

    if confidence >= 0.50:
        return "review"

    return "uncertain"


def uncertainty_reason(
    ocr_text: str,
    vlm_text: str,
    confidence: float,
) -> str:

    if not ocr_text and not vlm_text:
        return "No recognition evidence available."

    if ocr_text and vlm_text:
        if ocr_text.strip().lower() != vlm_text.strip().lower():
            return "Recognition models disagree."

    if confidence < 0.50:
        return "Low recognition confidence."

    if confidence < 0.80:
        return "Moderate confidence; human review recommended."

    return "Strong evidence agreement."