import json
import time
from typing import Optional

import requests

from ..utils.logger import get_logger

logger = get_logger()

RETRY_COUNT = 3
TIMEOUT_SEC = 10


def send_callback(
    url: str,
    task_id: int,
    success: bool,
    file_path: Optional[str] = None,
    img_path: Optional[str] = None,
    catalog_img_path: Optional[str] = None,
    page_count: Optional[int] = None,
    message: str = "success",
) -> None:
    if success:
        payload = {
            "result": True,
            "message": message,
            "data": {
                "taskId": task_id,
                "filePath": file_path,
                "imgPath": img_path,
                "catalogImgPath": catalog_img_path,
                "pageCount": page_count,
            },
        }
    else:
        payload = {
            "result": False,
            "message": message,
            "data": {"taskId": task_id},
        }

    logger.info(f"CALLBACK URL : {url}")
    logger.info(f"CALLBACK PAYLOAD : {json.dumps(payload, ensure_ascii=False)}")

    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = requests.post(url, json=payload, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            logger.info(f"CALLBACK SUCCESS : status={resp.status_code}")
            return
        except requests.RequestException as e:
            logger.warning(f"Callback attempt {attempt}/{RETRY_COUNT} failed: {e}")
            if attempt < RETRY_COUNT:
                time.sleep(2)

    logger.error("CALLBACK FAILED after all retries")
    raise RuntimeError(f"Callback failed after {RETRY_COUNT} attempts")
