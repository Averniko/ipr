import logging
from typing import AsyncGenerator, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import DATABASE_URL, SHOW_DB_LOG
from db.models import Base, Message

logger = logging.getLogger(__name__)

engine = create_async_engine(DATABASE_URL, echo=SHOW_DB_LOG)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_next_message_id(session: AsyncSession) -> int:
    results = await session.execute(Message.message_id_seq.next_value())
    return results.scalar()


async def get_next_session_id(session: AsyncSession) -> int:
    results = await session.execute(Message.session_id_seq.next_value())
    return results.scalar()


async def get_message_by_id(session: AsyncSession, message_id: int) -> Optional[Message]:
    statement = select(Message).where(Message.id == message_id)
    results = await session.execute(statement)
    return results.unique().scalar_one_or_none()


async def update_message(session: AsyncSession, message: Message) -> None:
    session.add(message)
    await session.commit()
