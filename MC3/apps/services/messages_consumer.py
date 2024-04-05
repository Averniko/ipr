import json
import logging
from datetime import datetime
from typing import AsyncIterable

from aiokafka import AIOKafkaConsumer
from opentelemetry.context import Context
from opentelemetry.propagate import extract

from core.config import trace
from schemas import MessageBase
from services.messages_producer import MessagesProducer

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

messages_producer = MessagesProducer()


class MessagesConsumer:
    def __init__(self, topic: str = "default"):
        self._consumer = AIOKafkaConsumer(topic, bootstrap_servers="kafka:29092")

    @staticmethod
    def _deserialize_message(data) -> tuple[dict, Context]:
        data = json.loads(data.value.decode("utf-8"))
        context: Context = extract(data)
        return data, context

    async def _receive_messages(self) -> AsyncIterable[MessageBase]:
        async for data in self._consumer:
            message, context = self._deserialize_message(data)
            yield MessageBase(**message), context

    async def consume(self):
        await self._consumer.start()
        logger.info(f"Consumer started")
        while True:
            async for message, context in self._receive_messages():
                with tracer.start_as_current_span("message_received", context=context):
                    message.mc3_timestamp = datetime.now()
                    logger.info(f"Message MC3 | {message}")
                with tracer.start_as_current_span("send_message", context=context):
                    await messages_producer.send_message(message, context)
