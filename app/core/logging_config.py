import logging
import os

from logging.handlers import RotatingFileHandler


LOG_DIRECTORY = "logs"
LOG_FILE = os.path.join(
    LOG_DIRECTORY,
    "dei_backend.log"
)


def configure_logging() -> None:
    """
    Configura el sistema global de logging
    del backend DEI.
    """

    os.makedirs(
        LOG_DIRECTORY,
        exist_ok=True
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    root_logger = logging.getLogger()

    root_logger.setLevel(
        logging.INFO
    )
    
    logging.getLogger(
        "httpx"
    ).setLevel(
        logging.WARNING
    )

    logging.getLogger(
        "google_genai"
    ).setLevel(
        logging.WARNING
    )

    root_logger.addHandler(
        file_handler
    )