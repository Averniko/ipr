from logging.config import dictConfig

from fastapi import FastAPI

from core.config import LOGGER_CONFIG
from routers import router as ws_router

dictConfig(LOGGER_CONFIG)

app = FastAPI(
    title="MC2"
)

app.include_router(ws_router)
