import logging
from src.models.schemas import IncomingPayload, OutgoingPayload
from src.services.intent_engine import detect_intent
from src.services.rp_engine import generate_npc_dialogue
from src.services.memory_manager import MemoryManager

logger = logging.getLogger(__name__)

async def process_interaction(engine, memory: MemoryManager, payload: IncomingPayload) -> OutgoingPayload:
    """
    Orchestrates the lifecycle of an interaction.
    Retrieves memory, determines player intent via the local LLM, generates immersive dialogue 
    via the cloud LLM, and persists the new conversational state.
    """
    try:
        # Create a unique session key combining the player and the specific NPC
        session_id = f"session_{payload.player.player_uuid}_{payload.npc.npc_uuid}"
        
        history = await memory.get_history(session_id)
        
        intent_result = await detect_intent(engine, payload.world.event_type, payload.player.message, history)
        dialogue = await generate_npc_dialogue(payload, intent_result, history)
        
        # Save the interaction to Redis to maintain the sliding window
        if payload.player.message:
            await memory.add_message(session_id, "user", payload.player.message)
            
        await memory.add_message(session_id, "assistant", dialogue)
        
        return OutgoingPayload(
            target_player_uuid=payload.player.player_uuid,
            status="SUCCESS",
            message=dialogue,
            action_intent=intent_result.intent,
        )
        
    except Exception as e:
        logger.error(f"Interaction processing failed: {e}")
        return OutgoingPayload(
            target_player_uuid=payload.player.player_uuid,
            status="ERROR",
            message="*Eldon semble perdu dans ses pensées et ne répond pas.*",
            action_intent="CHAT_ONLY",
        )