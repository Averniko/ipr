import os
import sys
from datetime import datetime

from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_next_message_id, get_async_session, get_next_session_id
from schemas import MessageBase

app = FastAPI(
    title="Test App"
)


@app.get("/start")
async def start(request: Request, session: AsyncSession = Depends(get_async_session)):
    # async with websockets.connect(f"ws://localhost:8001/ws/") as websocket:
    message_id = await get_next_message_id(session)
    session_id = await get_next_session_id(session)
    print(message_id, session_id)
    message = MessageBase(
        id=message_id,
        session_id=session_id,
        mc1_timestamp=datetime.now(),
    )
    print(message)
    # await websocket.send("Hello, Server!")
