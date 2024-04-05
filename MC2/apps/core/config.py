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
SECRET_KEY: str = os.environ.get("SECRET_KEY")
OTLP_HTTP_ENDPOINT = os.environ.get(
    "OTLP_HTTP_ENDPOINT", "http://otel-collector:4318/v1/traces"
)

resource = Resource.create(attributes={
    "service.name": "MS2",
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
        "root": {"handlers": ["default"], "level": "DEBUG" if DEBUG else "INFO", "propagate": False},
    },
}
