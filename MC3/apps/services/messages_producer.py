from opentelemetry.context import Context

from schemas import MessageBase
from services.api_client import APIClient


class MessagesProducer:
    def __init__(self, client: APIClient = APIClient()):
        self._client = client

    async def send_message(self, message: MessageBase, context: Context):
        await self._client.send_message(message.model_dump(mode="json"), context=context)
