from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Job(Base):
    """
    Persistent handwriting digitization job.

    One database row represents one uploaded handwriting
    image and its processing lifecycle.
    """

    __tablename__ = "jobs"

    # -----------------------------------------------------
    # Primary key
    # -----------------------------------------------------

    job_id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        index=True,
    )

    # -----------------------------------------------------
    # Uploaded file information
    # -----------------------------------------------------

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    image_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    # -----------------------------------------------------
    # Job status
    # -----------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="queued",
        index=True,
    )

    # -----------------------------------------------------
    # Timestamps
    # -----------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -----------------------------------------------------
    # Pipeline result
    # -----------------------------------------------------

    result_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # -----------------------------------------------------
    # Error information
    # -----------------------------------------------------

    error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )