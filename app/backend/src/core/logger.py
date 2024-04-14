from logging import config as logging_config
from pathlib import Path

from .config import settings

LOG_FORMAT = settings.LOG_FORMAT
LOG_LEVEL_DEFAULT = settings.LOG_LEVEL_DEFAULT
LOG_LEVEL_ACCESS = settings.LOG_LEVEL_ACCESS
LOG_LEVEL_SQLALCHEMY = settings.LOG_LEVEL_SQLALCHEMY

LOG_PATH = settings.LOG_PATH

if LOG_PATH:
    log_path = Path("/".join(LOG_PATH.split("/")[:-1]))
    if not log_path.exists():
        log_path.mkdir(parents=True, exist_ok=True)
    DEFAULT_HANDLER = {
        "formatter": "default",
        "class": "logging.FileHandler",
        "filename": LOG_PATH,
    }
    ACCESS_HANDLER = {
        "formatter": "access",
        "class": "logging.FileHandler",
        "filename": LOG_PATH,
    }
else:
    DEFAULT_HANDLER = {
        "formatter": "default",
        "class": "logging.StreamHandler",
        "stream": "ext://sys.stdout",
    }
    ACCESS_HANDLER = {
        "formatter": "access",
        "class": "logging.StreamHandler",
        "stream": "ext://sys.stdout",
    }

LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": LOG_DATE_FORMAT,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": LOG_DATE_FORMAT,
        },
    },
    "handlers": {"default": DEFAULT_HANDLER, "access": ACCESS_HANDLER},
    "loggers": {
        "uvicorn.error": {
            "handlers": ["default"],
            "level": LOG_LEVEL_DEFAULT,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": LOG_LEVEL_ACCESS,
            "propagate": False,
        },
        "sqlalchemy": {
            "handlers": ["default"],
            "level": LOG_LEVEL_SQLALCHEMY,
            "propagate": False,
        },
    },
    "root": {
        "level": LOG_LEVEL_DEFAULT,
        "formatter": "default",
        "handlers": ["default"],
        "propagate": False,
    },
}

logging_config.dictConfig(LOGGING)
