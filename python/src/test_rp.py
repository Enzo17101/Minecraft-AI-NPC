import asyncio
import logging
from schemas import IncomingPayload, WorldData, PlayerData, NPCData, LocationData
from intent_engine import IntentResult
from rp_engine import generate_npc_dialogue
from dotenv import load_dotenv

# Load .env variables (MODEL_API_KEY, HF_TOKEN)
load_dotenv()

# Mute noisy loggers
import os
os.environ["VLLM_LOGGING_LEVEL"] = "WARNING"
os.environ["VLLM_CONFIGURE_LOGGING"] = "0"
logging.getLogger("httpx").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_mock_payload(message: str, health: float, item: str, weather: str, max_health: float) -> IncomingPayload:
    """Helper to quickly generate a fake Minecraft state."""
    return IncomingPayload(
        world=WorldData(event_type="CHAT", timestamp=0, world_time=6000, weather=weather),
        player=PlayerData(
            player_uuid="123", player_name="Arthas", message=message,
            held_item=item, economy_balance=100.0, player_health=health, player_max_health=max_health
        ),
        npc=NPCData(
            npc_uuid="456", npc_name="Eldon", npc_health=20.0,
            npc_location=LocationData(x=0, y=0, z=0)
        )
    )

async def run_roleplay_tests():
    logger.info("--- Starting Roleplay Engine Tests ---")

    # Scenario 1: Healthy player, sunny, threatening the NPC with a sword
    payload1 = create_mock_payload("Donne moi ton armure le vieux !", 20.0, "minecraft:iron_sword", "CLEAR", 20.0)
    intent1 = IntentResult(intent="TRIGGER_HOSTILITY", extracted_target="armure")
    
    logger.info("\nTest 1: Hostility (Iron Sword / Healthy)")
    response1 = await generate_npc_dialogue(payload1, intent1)
    logger.info(f"\nEldon dit : {response1}")

    # Scenario 2: Dying player, in the rain, asking for help
    payload2 = create_mock_payload("Aide-moi...", 4.0, "minecraft:air", "STORM", 20.0)
    intent2 = IntentResult(intent="TRIGGER_ASSISTANCE", extracted_target=None)
    
    logger.info("\nTest 2: Assistance (Dying / Storm)")
    response2 = await generate_npc_dialogue(payload2, intent2)
    logger.info(f"\nEldon dit : {response2}")

if __name__ == "__main__":
    asyncio.run(run_roleplay_tests())