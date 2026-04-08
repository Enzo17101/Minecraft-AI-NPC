import json
import logging
import uuid
from typing import Optional
from pydantic import BaseModel, Field
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams

logger = logging.getLogger(__name__)

class IntentResult(BaseModel):
    """
    Data transfer object mapping the local LLM JSON output to Python types.
    Represents the mathematical classification of a player's interaction.
    """
    intent: str = Field(description="The detected intent from the taxonomy")
    extracted_target: Optional[str] = Field(
        default=None, 
        description="Specific item, quest, or subject the player mentioned, if applicable"
    )

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

async def detect_intent(engine: AsyncLLMEngine, event_type: str, message: Optional[str]) -> IntentResult:
    """
    Evaluates the context of a player interaction using the local LLM to extract a strict actionable intent.
    Bypasses the LLM entirely for pure physical interactions to guarantee zero latency.
    """
    if event_type == "RIGHT_CLICK" and not message:
        return IntentResult(intent="CHAT_ONLY")
        
    safe_message = message or ""

    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{INTENT_SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>

Event: {event_type}
Message: {safe_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

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