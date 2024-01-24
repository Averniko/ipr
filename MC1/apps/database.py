from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import DATABASE_URL, SHOW_DB_LOG
from models import Base, Message

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
