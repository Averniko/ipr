import json
import logging
from datetime import datetime
from typing import AsyncIterable

from aiokafka import AIOKafkaConsumer

from schemas import MessageBase
from services.messages_producer import MessagesProducer

logger = logging.getLogger(__name__)

messages_producer = MessagesProducer()


class MessagesConsumer:
    def __init__(self, topic: str = "default"):
        self._consumer = AIOKafkaConsumer(topic, bootstrap_servers="kafka:29092")

    async def _receive_messages(self) -> AsyncIterable[MessageBase]:
        async for message in self._consumer:
            yield MessageBase(**json.loads(message.value.decode("utf-8")))

    async def consume(self):
        await self._consumer.start()
        logger.info(f"Consumer started")
        while True:
            async for message in self._receive_messages():
                message.mc3_timestamp = datetime.now()
                logger.info(f"Message MC3 | {message}")
                await messages_producer.send_message(message)
