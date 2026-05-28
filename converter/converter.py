import fitz  # PyMuPDF

from .models.task import ConvertTask
from .services.office_converter import convert_to_pdf
from .services.thumbnail_service import create_thumbnail
from .services.catalog_service import create_catalog
from .services.callback_service import send_callback
from .utils.file_utils import validate_src_path, validate_tar_path, validate_callback_url
from .utils.logger import get_logger

logger = get_logger()


class DocumentConverter:

    def run(self, task: ConvertTask) -> None:
        logger.info(f"TASK START : {task.taskId}")

        try:
            self._validate(task)

            pdf_path = convert_to_pdf(task.srcPath, task.tarPath)

            img_path = None
            catalog_path = None

            page_count = self._get_page_count(pdf_path)

            if task.isThumbNail:
                img_path = create_thumbnail(pdf_path, task.tarPath, task.width, task.height)

            if task.isCatalog:
                catalog_path = create_catalog(pdf_path, task.tarPath)

            send_callback(
                url=task.callBack,
                task_id=task.taskId,
                success=True,
                file_path=pdf_path,
                img_path=img_path,
                catalog_img_path=catalog_path,
                page_count=page_count,
            )

        except Exception as exc:
            logger.error(f"TASK FAILED : {task.taskId} - {exc}")
            try:
                send_callback(
                    url=task.callBack,
                    task_id=task.taskId,
                    success=False,
                    message=str(exc),
                )
            except Exception as cb_exc:
                logger.error(f"CALLBACK ERROR : {cb_exc}")
            raise

        logger.info("TASK END")

    def _validate(self, task: ConvertTask) -> None:
        validate_src_path(task.srcPath)
        validate_tar_path(task.tarPath)
        validate_callback_url(task.callBack)

    def _get_page_count(self, pdf_path: str) -> int:
        doc = fitz.open(pdf_path)
        count = doc.page_count
        doc.close()
        return count


def run(task: ConvertTask) -> None:
    DocumentConverter().run(task)
