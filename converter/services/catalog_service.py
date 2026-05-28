import os

import fitz  # PyMuPDF
from PIL import Image

from ..utils.logger import get_logger

logger = get_logger()

DEFAULT_DPI = 150


def create_catalog(pdf_path: str, tar_path: str) -> str:
    """Render all PDF pages and save as numbered JPGs in Catalog directory."""
    stem = os.path.splitext(os.path.basename(tar_path))[0]
    tar_dir = os.path.dirname(tar_path)
    catalog_dir = os.path.join(tar_dir, "Catalog")
    os.makedirs(catalog_dir, exist_ok=True)

    zoom = DEFAULT_DPI / 72
    mat = fitz.Matrix(zoom, zoom)

    doc = fitz.open(pdf_path)
    try:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(os.path.join(catalog_dir, f"{i}.jpg"), "JPEG", quality=85)
    finally:
        doc.close()

    logger.info("CATALOG CREATED")
    return catalog_dir
