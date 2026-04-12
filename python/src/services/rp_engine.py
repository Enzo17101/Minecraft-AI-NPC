import logging
from typing import List, Dict
from src.models.schemas import IncomingPayload
from src.core.ai_engine import generate_cloud_response
from src.services.intent_engine import IntentResult

logger = logging.getLogger(__name__)

# Base NPC Persona Configuration
# In Sprint 3 (Database), this will be dynamically fetched from PostgreSQL
NPC_PERSONA = """You are Eldon, a grumpy but wise veteran guard of the Northern Kingdom. 
You are stationed in a small village. You speak in a medieval, slightly tired tone. 
You respect strength but despise arrogance. You have a scar over your left eye."""

def get_time_description(world_time: int) -> str:
    """
    Translates Minecraft server ticks (0-24000) into narrative time cycles.
    """
    t = world_time % 24000
    
    schedule = [
        (1000, "dawn"),
        (5000, "morning"),
        (7000, "noon"),
        (11500, "afternoon"),
        (13000, "twilight"),
        (17000, "the beginning of the night"),
        (22500, "nighttime"),
        (24000, "dawn")
    ]

    desc = next(description for limit, description in schedule if t < limit)
    return f"It is {desc}."

def get_weather_description(weather: str) -> str:
    return "It is raining heavily." if weather == "STORM" else "The weather is clear."

def get_player_health_description(player_health: float, player_max_health: float) -> str:
    """
    Calculates the player's health percentage to provide a realistic visual state.
    """
    health_thresholds = [
        (0.2, "severely wounded and bleeding"),
        (0.4, "severely wounded"),
        (0.6, "bruised and injured"),
        (0.8, "moderately injured"),
        (0.9, "slightly injured"),
    ]

    desc = next(
        (description for pct, description in health_thresholds if player_health < (player_max_health * pct)),
        "healthy"
    ) 
    return f"{desc}."

def get_player_held_item_description(player_held_item: str) -> str:
    """
    Cleans up the raw Bukkit material string into natural language.
    """
    held_item = player_held_item.replace("minecraft:", "").replace("_", " ").lower()
    return "holding nothing" if held_item == "air" else f"holding a {held_item}"

def build_context_paragraph(payload: IncomingPayload, intent: IntentResult) -> str:
    """
    Translates raw JSON metrics into a narrative context for the LLM.
    """
    player = payload.player
    world = payload.world
    caps = payload.npc.capabilities
    
    weather_desc = get_weather_description(world.weather)
    time_desc = get_time_description(world.world_time)
    health_desc = get_player_health_description(player.player_health, player.player_max_health)
    
    # Passing the held_item argument fixes the memory address injection bug
    item_desc = get_player_held_item_description(player.held_item)
    
    context = (
        f"[DIRECTOR'S NOTES]\n"
        f"Time & Weather: {time_desc} {weather_desc}\n"
        f"Player Status: The player '{player.player_name}' is {health_desc} and {item_desc}.\n"
        f"Detected Intent: {intent.intent}\n"
    )
    
    if intent.extracted_target:
        context += f"The player is specifically focusing on: {intent.extracted_target}\n"
        
    # Injects trade capabilities only if the Java server explicitly authorized them
    if caps.trade and caps.trade.is_merchant:
        inventory_details = ", ".join(
            [f"{item.item} (Price: {item.price} gold, Stock: {item.stock})" for item in caps.trade.inventory]
        )
        context += f"Merchant Info: You are currently a merchant. You have these items for sale: {inventory_details}. If asked to trade, mention your prices naturally.\n"
        
    return context

def format_conversation_history(history: List[Dict[str, str]], npc_name: str) -> str:
    """
    Transforms the raw Redis dictionary list into a readable transcript for the LLM.
    """
    if not history:
        return ""
        
    transcript = "[Recent Conversation History]\n"
    for msg in history:
        speaker = "Player" if msg["role"] == "user" else npc_name
        transcript += f"{speaker}: {msg['content']}\n"
        
    return transcript + "\n"

async def generate_npc_dialogue(payload: IncomingPayload, intent: 'IntentResult', history: List[Dict[str, str]]) -> str:
    """
    Constructs the final prompt and calls the Cloud LLM to generate spoken dialogue.
    """
    context_notes = build_context_paragraph(payload, intent)
    history_transcript = format_conversation_history(history, payload.npc.npc_name)
    
    system_prompt = f"""{NPC_PERSONA}

Strict Rules:
1. Stay in character AT ALL TIMES. Never break the 4th wall.
2. Do not mention Minecraft mechanics. Talk about the world naturally.
3. Keep your response concise (1 to 3 short sentences max). You are in a video game, players hate reading long texts.
4. React naturally to the DIRECTOR'S NOTES (weather, player health, held item, and your merchant inventory if applicable).
"""

    user_message = payload.player.message if payload.player.message else "*Approaches silently*"
    # Inject the history right before the new player message
    user_prompt = f"{context_notes}\n\n{history_transcript}Player says: \"{user_message}\""


    logger.info(f"Generating Roleplay response for {payload.player.player_name} via Cloud LLM...")
    response_text = await generate_cloud_response(system_prompt, user_prompt)
    
    return response_text.strip()