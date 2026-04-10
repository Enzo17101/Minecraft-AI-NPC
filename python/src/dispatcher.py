import logging
from vllm.engine.async_llm_engine import AsyncLLMEngine
from schemas import IncomingPayload, OutgoingPayload
from intent_engine import detect_intent
from rp_engine import generate_npc_dialogue

logger = logging.getLogger(__name__)

async def process_interaction(engine: AsyncLLMEngine, payload: IncomingPayload) -> OutgoingPayload:
    try:
        intent_result = await detect_intent(engine, payload.world.event_type, payload.player.message)
        dialogue = await generate_npc_dialogue(payload, intent_result)
        
        return OutgoingPayload(
            status="SUCCESS",
            message=dialogue,
            action_intent=intent_result.intent,
        )
        
    except Exception as e:
        logger.error(f"Interaction processing failed: {e}")
        return OutgoingPayload(
            status="ERROR",
            message="*Eldon semble perdu dans ses pensées et ne répond pas.*",
            action_intent="CHAT_ONLY",
        )