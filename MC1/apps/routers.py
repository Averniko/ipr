import logging
from datetime import datetime

from fastapi import APIRouter
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import MC2_WS
from db import database
from db.models import Message
from schemas import MessageBase
from services.ws_manager import WSManager

logger = logging.getLogger(__name__)

router = APIRouter()

ws_producer = WSManager(MC2_WS)


@router.get("/start")
async def start(request: Request, session: AsyncSession = Depends(database.get_async_session)) -> MessageBase:
    message_id = await database.get_next_message_id(session)
    session_id = await database.get_next_session_id(session)
    message = MessageBase(
        id=message_id,
        session_id=session_id,
        mc1_timestamp=datetime.now(),
    )
    logger.info(f"Message created | {message}")
    await database.update_message(session, Message(**message.__dict__))
    await ws_producer.send(message)
    return message


@router.post("/end")
async def end(request: Request, message: MessageBase,
              session: AsyncSession = Depends(database.get_async_session)) -> MessageBase:
    db_message = await database.get_message_by_id(session, message.id)
    db_message.mc2_timestamp = message.mc2_timestamp
    db_message.mc3_timestamp = message.mc3_timestamp
    db_message.end_timestamp = datetime.now()

    await database.update_message(session, db_message)

    message = MessageBase(**db_message.__dict__)
    logger.info(f"Message end | {message}")
    return message
