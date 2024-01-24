import logging
from datetime import datetime

from fastapi import APIRouter
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_next_message_id, get_async_session, get_next_session_id
from schemas import MessageBase

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/start")
async def start(request: Request, session: AsyncSession = Depends(get_async_session)) -> None:
    # async with websockets.connect(f"ws://localhost:8001/ws/") as websocket:
    message_id = await get_next_message_id(session)
    session_id = await get_next_session_id(session)
    message = MessageBase(
        id=message_id,
        session_id=session_id,
        mc1_timestamp=datetime.now(),
    )
    logger.info(f"Message created | {message}")
    # await websocket.send("Hello, Server!")
