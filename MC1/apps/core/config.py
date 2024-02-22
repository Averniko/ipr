import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()

DEBUG: bool = bool(strtobool(os.environ.get("DEBUG", "False")))
DB_HOST: str = os.environ.get("DB_HOST")
DB_PORT: str = os.environ.get("DB_PORT")
DB_NAME: str = os.environ.get("DB_NAME")
DB_USER: str = os.environ.get("DB_USER")
DB_PASS: str = os.environ.get("DB_PASS")
SECRET_KEY: str = os.environ.get("SECRET_KEY")
DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SHOW_DB_LOG: bool = bool(strtobool(os.environ.get("SHOW_DB_LOG", "False")))
MC2_WS: str = os.environ.get("MC2_WS")

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
