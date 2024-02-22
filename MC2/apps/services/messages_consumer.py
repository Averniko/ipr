import json

from aiokafka import AIOKafkaProducer

from schemas import MessageBase


class MessagesConsumer:
    def __init__(self):
        self._producer = AIOKafkaProducer(bootstrap_servers="kafka:29092")
        self._is_started = False

    async def _connect(self):
        if not self._is_started:
            await self._producer.start()
            self._is_started = True

    async def close(self):
        await self._producer.stop()
        self._is_started = False

    async def send(self, message: MessageBase):
        await self._connect()
        await self._producer.send_and_wait("default", json.dumps(message.model_dump(mode="json")).encode("utf-8"))
