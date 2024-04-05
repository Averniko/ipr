import json

from aiokafka import AIOKafkaProducer
from opentelemetry.context import Context
from opentelemetry.propagate import inject

from schemas import MessageBase


class MessagesProducer:
    def __init__(self):
        self._producer = AIOKafkaProducer(bootstrap_servers="kafka:29092")
        self._is_started = False

    async def _connect(self) -> None:
        if not self._is_started:
            await self._producer.start()
            self._is_started = True

    async def close(self) -> None:
        await self._producer.stop()
        self._is_started = False

    async def send(self, message: MessageBase, context: Context) -> None:
        await self._connect()
        await self._producer.send_and_wait("default", self._serialize_message(message, context))

    @staticmethod
    def _serialize_message(message: MessageBase, context: Context) -> bytes:
        data = message.model_dump(mode="json")
        inject(data, context)
        return json.dumps(data).encode("utf-8")
