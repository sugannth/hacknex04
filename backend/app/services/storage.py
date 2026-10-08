from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def save_upload(
    filename: str,
    content: bytes,
) -> str:

    original_extension = Path(filename).suffix.lower()

    if original_extension not in ALLOWED_EXTENSIONS:
        original_extension = ".jpg"

    file_id = uuid4().hex

    file_path = UPLOAD_DIR / f"{file_id}{original_extension}"

    file_path.write_bytes(content)

    return str(file_path)


def file_exists(
    file_path: str,
) -> bool:

    return Path(file_path).exists()


def delete_file(
    file_path: str,
) -> bool:

    path = Path(file_path)

    if not path.exists():
        return False

    path.unlink()

    return True