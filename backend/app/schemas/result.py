from typing import List, Optional
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: float = Field(..., description="Left coordinate")
    y: float = Field(..., description="Top coordinate")
    width: float = Field(..., description="Bounding box width")
    height: float = Field(..., description="Bounding box height")


class RegionResult(BaseModel):
    region_id: str
    bbox: Optional[BoundingBox] = None

    ocr_text: str = ""
    vlm_text: str = ""
    corrected_text: str = ""

    ocr_confidence: float = 0.0
    vlm_confidence: float = 0.0
    agreement_score: float = 0.0
    final_confidence: float = 0.0

    status: str = "uncertain"

    reason: Optional[str] = None


class UncertainRegion(BaseModel):
    region_id: str
    text: str = ""
    confidence: float = 0.0
    reason: str


class PipelineEvidence(BaseModel):
    ocr_text: str = ""
    vlm_text: str = ""
    corrected_text: str = ""

    ocr_available: bool = False
    vlm_available: bool = False
    llm_available: bool = False


class DigitizationResult(BaseModel):
    text: str = ""

    overall_confidence: float = 0.0

    status: str = "uncertain"

    regions: List[RegionResult] = Field(default_factory=list)

    uncertain_regions: List[UncertainRegion] = Field(default_factory=list)

    evidence: PipelineEvidence

    preprocessing: dict = Field(default_factory=dict)