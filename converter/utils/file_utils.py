import os
import magic

ALLOWED_EXTENSIONS = {
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".odt", ".ods", ".odp", ".txt", ".csv", ".rtf",
    ".html", ".pdf",
}

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB


def validate_src_path(src_path: str) -> None:
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")

    ext = os.path.splitext(src_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {ext}")

    size = os.path.getsize(src_path)
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")

    try:
        mime = magic.from_file(src_path, mime=True)
        allowed_mimes = {
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.oasis.opendocument.text",
            "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.presentation",
            "text/plain",
            "text/csv",
            "text/rtf",
            "text/html",
            "application/pdf",
        }
        if mime not in allowed_mimes:
            raise ValueError(f"Invalid MIME type: {mime}")
    except ImportError:
        pass


def validate_tar_path(tar_path: str) -> None:
    tar_dir = os.path.dirname(tar_path)
    if tar_dir and not os.path.exists(tar_dir):
        os.makedirs(tar_dir, exist_ok=True)


def validate_callback_url(url: str) -> None:
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid callback URL: {url}")


def get_stem(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)
