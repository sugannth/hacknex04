from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    UploadFile,
)

from app.pipeline.orchestrator import pipeline
from app.services.jobs import (
    create_job,
    get_job,
    mark_completed,
    mark_failed,
    mark_processing,
)
from app.services.storage import save_upload


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


# =========================================================
# CONFIGURATION
# =========================================================

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


# =========================================================
# BACKGROUND PIPELINE WORKER
# =========================================================

def run_pipeline(
    job_id: str,
    image_path: str,
):
    """
    Run the handwriting pipeline in the FastAPI background
    task and persist the job state.

    Lifecycle:

        queued
          ↓
        processing
          ↓
        completed

    If anything fails:

        processing
          ↓
        failed
    """

    try:

        # -------------------------------------------------
        # Mark job as processing
        # -------------------------------------------------

        mark_processing(job_id)

        # -------------------------------------------------
        # Run handwriting pipeline
        # -------------------------------------------------

        result = pipeline.process(
            image_path=image_path,
        )

        # -------------------------------------------------
        # Persist successful result
        # -------------------------------------------------

        mark_completed(
            job_id=job_id,
            result=result,
        )

    except Exception as exc:

        # -------------------------------------------------
        # Persist failure
        # -------------------------------------------------

        mark_failed(
            job_id=job_id,
            error=str(exc),
        )


# =========================================================
# CREATE JOB / UPLOAD IMAGE
# =========================================================

@router.post("")
async def upload_handwriting(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
):
    """
    Upload a handwriting image.

    The image is stored locally and a persistent job is
    created in SQLite.

    Processing happens in a FastAPI background task.
    """

    # -----------------------------------------------------
    # Validate content type
    # -----------------------------------------------------

    if image.content_type not in ALLOWED_CONTENT_TYPES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image type. "
                "Only JPEG, PNG and WebP images are supported."
            ),
        )

    # -----------------------------------------------------
    # Read uploaded image
    # -----------------------------------------------------

    content = await image.read()

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty.",
        )

    # -----------------------------------------------------
    # Validate file size
    # -----------------------------------------------------

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail="Image is too large. Maximum size is 10 MB.",
        )

    # -----------------------------------------------------
    # Determine filename
    # -----------------------------------------------------

    filename = image.filename or "handwriting.jpg"

    # -----------------------------------------------------
    # Save image
    # -----------------------------------------------------

    image_path = save_upload(
        filename=filename,
        content=content,
    )

    # -----------------------------------------------------
    # Create persistent job
    # -----------------------------------------------------

    job = create_job(
        filename=filename,
        image_path=image_path,
    )

    job_id = job["job_id"]

    # -----------------------------------------------------
    # Schedule background processing
    # -----------------------------------------------------

    background_tasks.add_task(
        run_pipeline,
        job_id,
        image_path,
    )

    # -----------------------------------------------------
    # Return immediately to frontend
    # -----------------------------------------------------

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Handwriting image uploaded successfully.",
    }


# =========================================================
# GET JOB STATUS
# =========================================================

@router.get("/{job_id}")
async def get_job_status(
    job_id: str,
):
    """
    Return the current status of a handwriting job.
    """

    job = get_job(job_id)

    if job is None:

        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return {
        "job_id": job["job_id"],
        "status": job["status"],
    }


# =========================================================
# GET COMPLETE RESULT
# =========================================================

@router.get("/{job_id}/result")
async def get_job_result(
    job_id: str,
):
    """
    Return the complete handwriting digitization result.
    """

    job = get_job(job_id)

    if job is None:

        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "result": job["result"],
        "error": job["error"],
    }