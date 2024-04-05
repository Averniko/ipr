import asyncio
import logging
from asyncio import sleep
from datetime import datetime, timedelta

import opentelemetry.context
from services.messages_manager import MessagesManager
from services.ws_manager import WSManager
from sqlalchemy.ext.asyncio import AsyncSession

from core import config
from core.config import MC2_WS
from core.config import trace
from db import database
from db.database import async_session_maker

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
ws_producer = WSManager(MC2_WS)


class MessagesGenerator:
    INTERVAL = config.INTERVAL
    started = False
    session_id = None
    started_at = None
    stopped_at = None
    messages_count = 0

    def _reset_metrics(self):
        self.started_at = None
        self.stopped_at = None
        self.messages_count = 0

    async def init(self, session: AsyncSession) -> int:
        self._reset_metrics()
        self.started = False
        self.session_id = await database.get_next_session_id(session)
        return self.session_id

    @staticmethod
    async def _create_and_send_message(session, session_id) -> None:
        message = await MessagesManager.create_message(session, session_id)
        await ws_producer.send(message, context=opentelemetry.context.get_current())

    async def start(self, session: AsyncSession) -> None:
        self._reset_metrics()
        self.started = True
        self.started_at = datetime.now()

        while self.started:
            with tracer.start_as_current_span("send_ws_message"):
                asyncio.create_task(self._create_and_send_message(session, self.session_id))
            self.messages_count += 1
            await sleep(self.INTERVAL)

    async def stop(self) -> int:
        self.started = False
        self.stopped_at = datetime.now()
        return self.session_id

    @property
    def duration(self) -> timedelta:
        if self.started_at and self.stopped_at:
            return self.stopped_at - self.started_at
        return timedelta()

    @property
    def rps(self) -> float:
        duration = self.duration
        if duration and self.messages_count:
            return self.messages_count / duration.total_seconds()
        return 0.0
