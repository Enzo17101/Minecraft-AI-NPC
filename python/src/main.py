from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
import logging

from schemas import IncomingPayload, OutgoingPayload
from connection_manager import ConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Minecraft NPC AI Orchestrator",
    description="Backend API for asynchronous AI NPC management via WebSockets",
    version="1.0.0"
)

manager = ConnectionManager()

@app.get("/health")
async def health_check():
    return {"status": "operational"}

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("New client connected to /ws/chat")
    
    try:
        while True:
            raw_data = await websocket.receive_text()
            
            try:
                incoming = IncomingPayload.model_validate_json(raw_data)
                
                logger.info(f"Received message from player {incoming.player.player_name} to NPC {incoming.npc.npc_name}")
                
                # Echo logic for Sprint 1
                response_text = f"[ECHO] {incoming.npc.npc_name} heard: {incoming.player.message}"
                
                outgoing = OutgoingPayload(
                    status="SUCCESS",
                    message=response_text,
                    action_intent="ECHO",
                    commands=[]
                )
                
                await manager.send_payload(outgoing.model_dump_json(), websocket)
                
            except ValidationError as e:
                logger.error(f"Payload validation failed: {e.errors()}")
                
                error_payload = OutgoingPayload(
                    status="ERROR",
                    message="Invalid JSON schema sent by the client.",
                    action_intent=None,
                    commands=[]
                )
                await manager.send_payload(error_payload.model_dump_json(), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected from /ws/chat")