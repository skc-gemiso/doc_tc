import os

import fitz  # PyMuPDF
from PIL import Image

from ..utils.logger import get_logger

logger = get_logger()


def create_thumbnail(pdf_path: str, tar_path: str, width: int, height: int) -> str:
    """Render first page of PDF and save as JPG thumbnail."""
    stem = os.path.splitext(os.path.basename(tar_path))[0]
    tar_dir = os.path.dirname(tar_path)
    thumb_dir = os.path.join(tar_dir, "Thumbnail")
    os.makedirs(thumb_dir, exist_ok=True)

    thumb_path = os.path.join(thumb_dir, f"thumb_{stem}.jpg")

    doc = fitz.open(pdf_path)
    try:
        page = doc[0]
        zoom = _calc_zoom(page, width, height)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.resize((width, height), Image.LANCZOS)
        img.save(thumb_path, "JPEG", quality=90)
    finally:
        doc.close()

    return thumb_path


def _calc_zoom(page: fitz.Page, target_w: int, target_h: int) -> float:
    rect = page.rect
    if rect.width == 0 or rect.height == 0:
        return 1.0
    zoom_w = target_w / rect.width
    zoom_h = target_h / rect.height
    return max(zoom_w, zoom_h)
