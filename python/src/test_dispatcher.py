import asyncio
import logging
import os
from ai_engine import init_vllm_engine
from dispatcher import process_interaction
from schemas import (
    IncomingPayload, WorldData, PlayerData, LocationData, NPCData,
    Capabilities, TradeCapability, TradeItem
)
from dotenv import load_dotenv

# Load .env variables (MODEL_API_KEY, HF_TOKEN)
load_dotenv()

os.environ["VLLM_LOGGING_LEVEL"] = "WARNING"
os.environ["VLLM_CONFIGURE_LOGGING"] = "0"
logging.getLogger("httpx").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_mock_payload(msg: str) -> IncomingPayload:
    return IncomingPayload(
        world=WorldData(event_type="CHAT", timestamp=0, world_time=6000, weather="CLEAR"),
        player=PlayerData(
            player_uuid="123", player_name="Arthas", message=msg,
            held_item="minecraft:air", economy_balance=100.0, 
            player_health=20.0, player_max_health=20.0
        ),
        npc=NPCData(
            npc_uuid="456", npc_name="Eldon", npc_health=20.0,
            npc_location=LocationData(x=0, y=0, z=0),
            capabilities=Capabilities(
                trade=TradeCapability(
                    is_merchant=True,
                    inventory=[TradeItem(item="apple", stock=18, price=6.0)]
                )
            )
        )
    )

async def run_pipeline_tests():
    engine = init_vllm_engine()
    await asyncio.sleep(2)
    
    payload = create_mock_payload("Je voudrais t'acheter des pommes.")
    
    result = await process_interaction(engine, payload)
    
    logger.info(f"Final JSON Output:\n{result.model_dump_json(indent=2)}")

if __name__ == "__main__":
    asyncio.run(run_pipeline_tests())