from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter


def preprocess_image(image_path: str) -> dict:
    """
    Preprocess a handwriting image.

    The hackathon pipeline keeps preprocessing lightweight:
    - validate image
    - convert to RGB
    - grayscale copy
    - contrast enhancement
    - mild sharpening

    The original uploaded image is never modified.
    """

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(path)

    original_width, original_height = image.size

    rgb_image = image.convert("RGB")

    grayscale = ImageOps.grayscale(rgb_image)

    contrast = ImageEnhance.Contrast(grayscale).enhance(1.4)

    sharpened = contrast.filter(ImageFilter.SHARPEN)

    return {
        "original_width": original_width,
        "original_height": original_height,
        "mode": image.mode,
        "format": image.format,
        "processed_image": sharpened,
        "processed_width": sharpened.width,
        "processed_height": sharpened.height,
    }