from typing import Optional
from pydantic import BaseModel


class JobResponse(BaseModel):
    job_id: str
    filename: str
    status: str
    created_at: str


class JobStatusResponse(BaseModel):
    job_id: str
    filename: str
    status: str
    created_at: str
    error: Optional[str] = None


class JobResultResponse(BaseModel):
    job_id: str
    filename: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None