import atexit
import logging

import httpx
from opentelemetry.context import Context
from opentelemetry.propagate import inject

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        self.base_url = "http://mc1:8000"
        self._client = httpx.AsyncClient()
        atexit.register(self._client.aclose)

    async def send_message(self, message: dict, context: Context = None) -> None:
        headers = {}
        inject(headers, context=context)
        try:
            resp = await self._client.post(
                url=f"{self.base_url}/end",
                json=message,
                headers=headers
            )

            resp.raise_for_status()
        except (httpx.ConnectError, httpx.HTTPError) as Error:
            logger.error(f"Ошибка при обращении к API: {str(Error)}")
            return None
