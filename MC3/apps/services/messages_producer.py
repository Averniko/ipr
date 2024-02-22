from services.api_client import APIClient
from schemas import MessageBase


class MessagesProducer:
    def __init__(self, client: APIClient = APIClient()):
        self._client = client

    async def send_message(self, message: MessageBase):
        await self._client.send_message(message.model_dump(mode="json"))
