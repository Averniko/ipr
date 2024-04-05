import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db import database
from db.models import Message
from schemas import MessageBase

logger = logging.getLogger(__name__)


class MessagesManager:
    @staticmethod
    async def create_message(session: AsyncSession, session_id: int) -> MessageBase:
        message_id = await database.get_next_message_id(session)
        await session.commit()
        message = MessageBase(
            id=message_id,
            session_id=session_id,
            mc1_timestamp=datetime.now(),
        )
        await database.update_message(session, Message(**message.__dict__))
        logger.info(f"Message created | {message}")
        return message

    @staticmethod
    async def process_message_end(session: AsyncSession, message: MessageBase) -> MessageBase:
        db_message = await database.get_message_by_id(session, message.id)
        db_message.mc2_timestamp = message.mc2_timestamp
        db_message.mc3_timestamp = message.mc3_timestamp
        db_message.end_timestamp = datetime.now()
        await database.update_message(session, db_message)
        message = MessageBase(**db_message.__dict__)
        logger.info(f"Message end updated | {message}")
        return message
