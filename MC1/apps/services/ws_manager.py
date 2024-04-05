import json

import websockets
from opentelemetry.context import Context
from opentelemetry.propagate import inject
from websockets import ConnectionClosedError

from schemas import MessageBase


class WSManager:
    _ws = None

    def __init__(self, url):
        self.url = url

    async def _connect(self):
        try:
            await self._ws.ensure_open()
        except (AttributeError, ConnectionClosedError):
            self._ws = await websockets.connect(self.url)

    async def send(self, message: MessageBase, context: Context = None):
        await self._connect()

        data = message.model_dump(mode="json")
        inject(data, context)
        message = json.dumps(data)
        await self._ws.send(message)
