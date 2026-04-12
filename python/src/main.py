from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
import logging
import os

from src.models.schemas import IncomingPayload, OutgoingPayload
from src.api.connection_manager import ConnectionManager
from src.core.ai_engine import init_vllm_engine
from src.services.dispatcher import process_interaction
from src.services.memory_manager import MemoryManager

from dotenv import load_dotenv

# Load .env variables (MODEL_API_KEY, HF_TOKEN)
load_dotenv()

# Suppress verbose dependencies output before server startup
os.environ["VLLM_LOGGING_LEVEL"] = "WARNING"
os.environ["VLLM_CONFIGURE_LOGGING"] = "0"
logging.getLogger("httpx").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = None
memory_manager = None
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, memory_manager
    logger.info("Initializing Local LLM Engine (vLLM)...")
    engine = init_vllm_engine()
    logger.info("Local LLM Engine ready.")

    logger.info("Connecting to Redis Memory Manager...")
    memory_manager = MemoryManager()

    yield
    logger.info("Shutting down services...")
    await memory_manager.close()

app = FastAPI(
    title="Minecraft NPC AI Orchestrator",
    description="Backend API for asynchronous AI NPC management via WebSockets",
    version="1.0.5",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "operational", "engine_loaded": engine is not None}

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("New client connected to /ws/chat")
    
    try:
        while True:
            raw_data = await websocket.receive_text()
            
            try:
                incoming = IncomingPayload.model_validate_json(raw_data)
                logger.info(f"[INCOMING PAYLOAD] {incoming}")
                logger.info(f"Received message from {incoming.player.player_name} to {incoming.npc.npc_name}")

                
                if not memory_manager:
                    raise RuntimeError("Critical: Memory Manager is not initialized.")
                    
                # Offload processing to the local intent engine and cloud roleplay model
                outgoing = await process_interaction(engine, memory_manager, incoming)
                
                # Preserve the original player UUID for accurate Java server routing
                outgoing.target_player_uuid = incoming.player.player_uuid

                # Pass the memory manager to the dispatcher
                outgoing = await process_interaction(engine, memory_manager, incoming)
                
                await manager.send_payload(outgoing.model_dump_json(), websocket)
                
            except ValidationError as e:
                logger.error(f"Payload validation failed: {e.errors()}")
                
                error_payload = OutgoingPayload(
                    status="ERROR",
                    target_player_uuid=None,
                    message="[System] Invalid JSON payload.",
                    action_intent=None
                )
                await manager.send_payload(error_payload.model_dump_json(), websocket)
                
            except Exception as e:
                logger.error(f"Unexpected error during processing: {e}")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected from /ws/chat")