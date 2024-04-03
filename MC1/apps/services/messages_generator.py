import logging
from asyncio import sleep

from services.messages_manager import MessagesManager
from services.ws_manager import WSManager
from sqlalchemy.ext.asyncio import AsyncSession

from core import config
from core.config import MC2_WS
from db import database

logger = logging.getLogger(__name__)
ws_producer = WSManager(MC2_WS)


class MessagesGenerator:
    INTERVAL = config.INTERVAL
    started = False
    session_id = None

    async def init(self, session: AsyncSession):
        self.started = False
        self.session_id = await database.get_next_session_id(session)

    async def start(self, session: AsyncSession):
        self.started = True
        while self.started:
            message = await MessagesManager.create_message(session, self.session_id)
            await ws_producer.send(message)
            await sleep(self.INTERVAL)

    async def stop(self):
        self.started = False
        logger.info(f"Session stopped | {self.session_id}")
        return self.session_id
