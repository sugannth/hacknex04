from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_PATH = DATA_DIR / "hnx26eps04.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# =========================================================
# SQLALCHEMY ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# =========================================================
# SQLALCHEMY BASE
# =========================================================

class Base(DeclarativeBase):
    pass


# =========================================================
# DATABASE SESSION
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():
    """
    Create all database tables.

    The model import is intentionally inside this function
    to avoid circular imports between database.py and models.py.
    """

    from app.db.models import Job

    Base.metadata.create_all(
        bind=engine,
    )


# =========================================================
# FASTAPI DATABASE DEPENDENCY
# =========================================================

def get_db():
    """
    Provide a database session for FastAPI routes/services.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()