# config/logging_config.py
import logging.config
import sys
from django.conf import settings

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[{levelname}] {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if not settings.DEBUG else "DEBUG",
    },
}

logging.config.dictConfig(LOGGING)
