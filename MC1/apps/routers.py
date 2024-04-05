import logging

from asgiref.sync import async_to_sync
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Request, Depends
from opentelemetry.propagate import extract
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import trace
from db import database
from schemas import MessageBase, MetricsBase
from services.messages_generator import MessagesGenerator
from services.messages_manager import MessagesManager

logger = logging.getLogger(__name__)

router = APIRouter()

messages_generator = MessagesGenerator()

tracer = trace.get_tracer(__name__)


async def start_generator(session: AsyncSession) -> None:
    session_id = await messages_generator.init(session)
    await messages_generator.start(session)
    logger.info(f"Session started | {session_id}")


@router.get("/start")
async def start(
        request: Request,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(database.get_async_session),
) -> None:
    with tracer.start_as_current_span("/start"):
        background_tasks.add_task(start_generator, session)


@router.get("/stop")
async def stop(request: Request, session: AsyncSession = Depends(database.get_async_session)) -> MetricsBase:
    with tracer.start_as_current_span("/stop"):
        session_id = await messages_generator.stop()
    logger.info(f"Session stopped | {session_id}")
    return MetricsBase(
        session_id=messages_generator.session_id,
        started_at=messages_generator.started_at,
        stopped_at=messages_generator.stopped_at,
        duration=messages_generator.duration,
        messages_count=messages_generator.messages_count,
        rps=messages_generator.rps,
    )


@router.post("/end")
async def end(request: Request, message: MessageBase,
              session: AsyncSession = Depends(database.get_async_session)) -> MessageBase:
    with tracer.start_as_current_span("/end", context=extract(request.headers)):
        response = await MessagesManager.process_message_end(session, message)
    return response
