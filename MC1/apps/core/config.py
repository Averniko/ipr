import os
from distutils.util import strtobool

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

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
INTERVAL: float = float(os.environ.get("INTERVAL", 1))
WORKERS_LIMIT: int = int(os.environ.get("WORKERS_LIMIT", 20))
OTLP_HTTP_ENDPOINT = os.environ.get(
    "OTLP_HTTP_ENDPOINT", "http://otel-collector:4318/v1/traces"
)

resource = Resource.create(attributes={
    "service.name": "MS1",
})

provider = TracerProvider(resource=resource)

trace.set_tracer_provider(provider)

provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporterHTTP(endpoint=OTLP_HTTP_ENDPOINT))
)

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
        "root": {"handlers": ["default"], "level": "DEBUG" if DEBUG else "WARNING", "propagate": False},
        "uvicorn.access": {"handlers": ["default"], "level": "DEBUG" if DEBUG else "WARNING", "propagate": False},
    },
}
