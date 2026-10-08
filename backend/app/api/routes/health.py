from fastapi import APIRouter

from app.pipeline.orchestrator import pipeline


router = APIRouter(
    tags=["health"],
)


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "hnx26eps04-backend",
        "pipeline": "ready",
    }


@router.get("/health/models")
def model_health():

    return {
        "ocr": {
            "available": pipeline.ocr.use_tesseract,
        },
        "vlm": {
            "provider": pipeline.vlm.provider,
        },
        "llm": {
            "provider": pipeline.llm.provider,
        },
    }