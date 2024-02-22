import json
import logging
from datetime import datetime

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from services.messages_consumer import MessagesConsumer
from services.ws_manager import WSManager
from schemas import MessageBase

logger = logging.getLogger(__name__)

router = APIRouter()

ws_manager = WSManager()

messages_consumer = MessagesConsumer()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    logger.info(f"WS connected | {websocket}")
    try:
        while True:
            data = await websocket.receive_text()
            message = MessageBase(**json.loads(data))
            message.mc2_timestamp = datetime.now()
            logger.info(f"Message MC2 | {message}")
            await messages_consumer.send(message)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
