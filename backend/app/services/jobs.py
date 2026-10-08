import json
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.db.database import SessionLocal
from app.db.models import Job


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _job_to_dict(job: Job) -> dict:
    """
    Convert SQLAlchemy Job object into the dictionary format
    already expected by our API layer.
    """

    result = None

    if job.result_json:
        try:
            result = json.loads(job.result_json)
        except json.JSONDecodeError:
            result = None

    return {
        "job_id": job.job_id,
        "filename": job.filename,
        "image_path": job.image_path,
        "status": job.status,
        "created_at": (
            job.created_at.isoformat()
            if job.created_at
            else None
        ),
        "started_at": (
            job.started_at.isoformat()
            if job.started_at
            else None
        ),
        "completed_at": (
            job.completed_at.isoformat()
            if job.completed_at
            else None
        ),
        "result": result,
        "error": job.error,
    }


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_job(
    filename: str,
    image_path: str,
):
    """
    Create and persist a new handwriting processing job.
    """

    job_id = str(uuid4())

    job = Job(
        job_id=job_id,
        filename=filename,
        image_path=image_path,
        status="queued",
        created_at=_utc_now(),
        started_at=None,
        completed_at=None,
        result_json=None,
        error=None,
    )

    db = SessionLocal()

    try:

        db.add(job)

        db.commit()

        db.refresh(job)

        return _job_to_dict(job)

    finally:

        db.close()


# ---------------------------------------------------------
# Read
# ---------------------------------------------------------

def get_job(
    job_id: str,
) -> Optional[dict]:
    """
    Retrieve a persistent job by ID.
    """

    db = SessionLocal()

    try:

        job = db.get(
            Job,
            job_id,
        )

        if job is None:
            return None

        return _job_to_dict(job)

    finally:

        db.close()


# ---------------------------------------------------------
# Generic update
# ---------------------------------------------------------

def update_job(
    job_id: str,
    **updates,
):
    """
    Update selected fields on a job.

    Supported fields:

    status
    started_at
    completed_at
    result
    error
    """

    db = SessionLocal()

    try:

        job = db.get(
            Job,
            job_id,
        )

        if job is None:
            return None

        if "status" in updates:
            job.status = updates["status"]

        if "started_at" in updates:
            job.started_at = updates["started_at"]

        if "completed_at" in updates:
            job.completed_at = updates["completed_at"]

        if "result" in updates:
            job.result_json = json.dumps(
                updates["result"],
                ensure_ascii=False,
            )

        if "error" in updates:
            job.error = updates["error"]

        db.commit()

        db.refresh(job)

        return _job_to_dict(job)

    finally:

        db.close()


# ---------------------------------------------------------
# Processing
# ---------------------------------------------------------

def mark_processing(
    job_id: str,
):
    """
    Mark a job as actively processing.
    """

    return update_job(
        job_id,
        status="processing",
        started_at=_utc_now(),
        error=None,
    )


# ---------------------------------------------------------
# Completed
# ---------------------------------------------------------

def mark_completed(
    job_id: str,
    result: dict,
):
    """
    Store the final pipeline result and mark the job
    as completed.
    """

    return update_job(
        job_id,
        status="completed",
        completed_at=_utc_now(),
        result=result,
        error=None,
    )


# ---------------------------------------------------------
# Failed
# ---------------------------------------------------------

def mark_failed(
    job_id: str,
    error: str,
):
    """
    Store a pipeline failure.
    """

    return update_job(
        job_id,
        status="failed",
        completed_at=_utc_now(),
        error=error,
    )