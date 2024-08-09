import logging
import sys
from typing import Dict, List

from loguru import logger

from config.config import settings


OVERRIDE_LEVEL_LOGGERS: Dict[str, str] = {
    "uvicorn": "INFO",
    "uvicorn.access": "INFO",
    "fastapi": "INFO",
}

DISABLED_LOGGERS: List[str] = [
    "prophet",
    # Отключение логов для сторонних библиотек
]

EXCLUDE_ENDPOINTS: List[str] = [
    "/healthz",
    # Отключение логов для эндпоинтов
]


def override_logger_levels(logger_levels: Dict[str, str]):
    for logger_name, level in logger_levels.items():
        logging.getLogger(logger_name).setLevel(level)


def disable_loggers(logger_names: List[str]):
    for name in logger_names:
        logging.getLogger(name).setLevel(logging.CRITICAL)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class EndpointFilter(logging.Filter):
    def __init__(self, exclude_endpoints: List[str]):
        super().__init__()
        self.exclude_endpoints = exclude_endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        return not any(endpoint in record.getMessage() for endpoint in self.exclude_endpoints)


def setup_logging():
    # Отключаем существующие логгеры
    logging.root.handlers = []
    logging.root.setLevel(logging.INFO)

    # Перехватываем все используемые библиотеками логгеры
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Создаем и применяем EndpointFilter
    endpoint_filter = EndpointFilter()

    # Настраиваем loguru (stdout/file)
    logging_level = logging.DEBUG if settings.debug else logging.INFO
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "level": logging_level, "filter": endpoint_filter.filter},
            # {"sink": Path("app.log"), "level": logging_level, "rotation": "500 MB"},
        ]
    )

    # Добавляем перехватчик для стандартного logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Применяем настройки для сторонних логгеров
    override_logger_levels(OVERRIDE_LEVEL_LOGGERS)
    disable_loggers(DISABLED_LOGGERS)

    return logger.bind(request_id=None, method=None)
