import logging

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import database
from schemas import MessageBase
from services.messages_generator import MessagesGenerator
from services.messages_manager import MessagesManager

logger = logging.getLogger(__name__)

router = APIRouter()

messages_generator = MessagesGenerator()


async def start_generator(session: AsyncSession) -> None:
    session_id = await messages_generator.init(session)
    logger.info(f"Session started | {session_id}")
    await messages_generator.start(session)


@router.get("/start")
async def start(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(database.get_async_session),
) -> None:
    background_tasks.add_task(start_generator, session)


@router.get("/stop")
async def stop(request: Request, session: AsyncSession = Depends(database.get_async_session)) -> None:
    await messages_generator.stop()


@router.post("/end")
async def end(request: Request, message: MessageBase,
              session: AsyncSession = Depends(database.get_async_session)) -> MessageBase:
    return await MessagesManager.process_message_end(session, message)
