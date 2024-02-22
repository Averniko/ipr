import asyncio
import logging
from asyncio import get_event_loop
from logging.config import dictConfig

from fastapi import FastAPI

from core.config import LOGGER_CONFIG
from services.messages_consumer import MessagesConsumer

logger = logging.getLogger(__name__)

dictConfig(LOGGER_CONFIG)

app = FastAPI(
    title="MC3"
)

messages_consumer = MessagesConsumer()

event_loop = get_event_loop()
asyncio.create_task(messages_consumer.consume())
