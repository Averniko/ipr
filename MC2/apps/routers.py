import asyncio
import json
import logging
from datetime import datetime

from fastapi import APIRouter
from opentelemetry.propagate import extract
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.config import trace
from schemas import MessageBase
from services.messages_producer import MessagesProducer
from services.ws_manager import WSManager

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()

ws_manager = WSManager()

messages_producer = MessagesProducer()


async def _process_message(data: str):
    data = json.loads(data)
    context = extract(data)
    message = MessageBase(**data)
    with tracer.start_span("message_received", context=context):
        message.mc2_timestamp = datetime.now()
        logger.info(f"Message MC2 | {message}")
    with tracer.start_span("send_message", context=context):
        await messages_producer.send(message, context)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    logger.info(f"WS connected | {websocket}")
    try:
        while True:
            data = await websocket.receive_text()
            asyncio.create_task(_process_message(data))

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
