from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="HNX26EPS04 - Extreme Bad-Handwriting Digitizing Stack",
    version="0.1.0",
    description=(
        "Backend pipeline for digitizing extremely difficult "
        "handwriting using OCR, vision-language models, "
        "evidence fusion, contextual correction and "
        "explicit uncertainty."
    ),
    lifespan=lifespan,
)

app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    jobs_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "name": "HNX26EPS04 Bad-Handwriting Digitizer",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
    }