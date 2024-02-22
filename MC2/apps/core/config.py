import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()

DEBUG: bool = bool(strtobool(os.environ.get("DEBUG", "False")))
SECRET_KEY: str = os.environ.get("SECRET_KEY")

LOGGER_CONFIG: dict[str, any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "fmt": "%(levelname)s %(asctime)s %(pathname)s:%(lineno)s %(process)d %(thread)d %(message)s",
            "use_colors": None,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {"handlers": ["default"], "level": "DEBUG" if DEBUG else "INFO", "propagate": False},
    },
}
