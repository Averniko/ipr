import json

import websockets
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

    async def send(self, message: MessageBase):
        await self._connect()
        message = json.dumps(message.model_dump(mode="json"))
        await self._ws.send(message)
