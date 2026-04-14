import logging
from src.models.schemas import IncomingPayload, OutgoingPayload
from src.services.intent_engine import detect_intent
from src.services.rp_engine import generate_npc_dialogue
from src.services.memory_manager import MemoryManager
from src.services.profile_manager import ProfileManager

logger = logging.getLogger(__name__)

async def process_interaction(engine, 
                              memory: MemoryManager, 
                              profiles: ProfileManager, 
                              payload: IncomingPayload
                              ) -> OutgoingPayload:
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

        if intent_result != "TALK_ONLY":
            # Uses the NPC's name (lowercase) to match the YAML file name (e.g., 'eldon.yaml')
            npc_id = payload.npc.npc_name.lower()
            mapped_commands = profiles.get_action_commands(npc_id, intent_result.intent, payload.player.player_name)
        else:
            mapped_commands = []
        
        # Save the interaction to Redis to maintain the sliding window
        if payload.player.message:
            await memory.add_message(session_id, "user", payload.player.message)
            
        await memory.add_message(session_id, "assistant", dialogue)
        
        return OutgoingPayload(
            target_player_uuid=payload.player.player_uuid,
            npc_name=payload.npc.npc_name,
            status="SUCCESS",
            message=dialogue,
            action_intent=intent_result.intent,
            commands = mapped_commands
        )
        
    except Exception as e:
        logger.error(f"Interaction processing failed: {e}")
        return OutgoingPayload(
            target_player_uuid=payload.player.player_uuid,
            npc_name=payload.npc.npc_name,
            status="ERROR",
            message=f"*{payload.npc.npc_name if payload.npc.npc_name is None else 'Le villageois'} semble perdu dans ses pensées et ne répond pas.*",
            action_intent="CHAT_ONLY",
            commands = []
        )