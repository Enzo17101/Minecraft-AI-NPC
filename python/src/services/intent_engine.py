import json
import logging
import uuid
from typing import List, Dict
from vllm import SamplingParams
from src.models.schemas import IntentResult
logger = logging.getLogger(__name__)


INTENT_SYSTEM_PROMPT = """You are a strictly logical JSON parsing engine for a Minecraft NPC.
Your ONLY job is to categorize the player's interaction based on these strict definitions:

- "CHAT_ONLY": Standard greetings, small talk, or generic comments.
- "TRIGGER_QUEST": The player asks about specific lore, locations, requests a mission, or asks for directions.
- "TRIGGER_TRADE": The player explicitly wants to buy, sell, or trade items.
- "TRIGGER_HOSTILITY": The player threatens, insults, or demands things aggressively.
- "TRIGGER_ASSISTANCE": The player explicitly asks for physical healing, buffs, or help because they are injured.

You must output ONLY valid JSON.
Example of expected format:
{
    "intent": "TRIGGER_QUEST",
    "extracted_target": "the king's castle"
}

DO NOT output any conversational text. DO NOT output markdown code blocks. Just the raw JSON object."""

async def detect_intent(engine, event_type: str, user_message: str | None, history: List[Dict[str, str]]) -> IntentResult:
    """
    Evaluates the context of a player interaction using the local LLM to extract a strict actionable intent.
    Bypasses the LLM entirely for pure physical interactions to guarantee zero latency.
    """
    if event_type == "RIGHT_CLICK" and not user_message:
        return IntentResult(intent="CHAT_ONLY")
        
    last_npc_message = ""
    for msg in reversed(history):
        if msg["role"] == "assistant":
            last_npc_message = msg["content"]
            break

    context_prompt = ""
    if last_npc_message:
        context_prompt = f"Previous NPC statement: '{last_npc_message}'\n"

    user_prompt = f"{context_prompt}Player says: '{user_message}'"

    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{INTENT_SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>

Event: {event_type}
Message: {user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{{"""

    sampling_params = SamplingParams(
        temperature=0.0, 
        max_tokens=50,
        stop=["<|eot_id|>"]
    )
    
    request_id = f"intent_{uuid.uuid4().hex[:8]}"
    
    try:
        final_output = ""
        async for request_output in engine.generate(prompt, sampling_params, request_id):
            final_output = request_output.outputs[0].text

        raw_json_string = "{" + final_output.strip()
        
        if raw_json_string.endswith("```"):
            raw_json_string = raw_json_string.replace("```", "").strip()
            
        parsed_data = json.loads(raw_json_string)
        return IntentResult(**parsed_data)
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Intent JSON. Raw output: {final_output} | Error: {e}")
        return IntentResult(intent="CHAT_ONLY")
    except Exception as e:
        logger.error(f"Local Engine Intent Failure: {e}")
        return IntentResult(intent="CHAT_ONLY")