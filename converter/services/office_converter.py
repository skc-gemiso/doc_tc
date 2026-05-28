import os
import shutil
import subprocess
import tempfile
import uuid

from ..utils.logger import get_logger

logger = get_logger()

LIBREOFFICE_BIN = shutil.which("libreoffice") or shutil.which("soffice") or "libreoffice"


def convert_to_pdf(src_path: str, tar_path: str) -> str:
    """Convert document to PDF using LibreOffice headless."""
    src_ext = os.path.splitext(src_path)[1].lower()
    tar_dir = os.path.dirname(tar_path)
    os.makedirs(tar_dir, exist_ok=True)

    if src_ext == ".pdf":
        if os.path.abspath(src_path) != os.path.abspath(tar_path):
            shutil.copy2(src_path, tar_path)
        return tar_path

    worker_id = uuid.uuid4().hex
    user_profile = f"/tmp/libreoffice_worker_{worker_id}"

    with tempfile.TemporaryDirectory() as tmp_dir:
        cmd = [
            LIBREOFFICE_BIN,
            "--headless",
            f"-env:UserInstallation=file://{user_profile}",
            "--convert-to", "pdf",
            src_path,
            "--outdir", tmp_dir,
        ]
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
            )
            if result.returncode != 0:
                err = result.stderr.decode(errors="replace")
                raise RuntimeError(f"LibreOffice failed (rc={result.returncode}): {err}")

            src_stem = os.path.splitext(os.path.basename(src_path))[0]
            tmp_pdf = os.path.join(tmp_dir, src_stem + ".pdf")
            if not os.path.exists(tmp_pdf):
                raise RuntimeError(f"PDF not found after conversion: {tmp_pdf}")

            shutil.move(tmp_pdf, tar_path)
        finally:
            shutil.rmtree(user_profile, ignore_errors=True)

    return tar_path
