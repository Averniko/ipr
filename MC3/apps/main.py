import asyncio
import logging
from asyncio import get_event_loop
from logging.config import dictConfig

from aiokafka.errors import KafkaConnectionError
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


async def consume_messages():
    while True:
        try:
            await messages_consumer.consume()
        except KafkaConnectionError as exception:
            logger.exception(exception)
            await asyncio.sleep(1)


asyncio.create_task(consume_messages())
