import asyncio
import logging
import time
from src.core.ai_engine import init_vllm_engine
from src.services.intent_engine import detect_intent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_intent_tests():
    logger.info("--- Starting Local Intent Engine Tests ---")
    
    # Initialize the engine (pays the cold start cost)
    engine = init_vllm_engine()
    
    # Wait a tiny bit for the engine to be fully ready
    await asyncio.sleep(2)

    test_cases = [
        {"event": "CHAT", "msg": "Bonjour Eldon !"},
        {"event": "CHAT", "msg": "Je suis gravement blessé, aide-moi..."},
        {"event": "CHAT", "msg": "Donne moi ton épée ou je te tue !"},
        {"event": "CHAT", "msg": "Je veux acheter 3 potions de soin."},
        {"event": "CHAT", "msg": "Où se trouve le château du roi ?"},
        {"event": "RIGHT_CLICK", "msg": None} # Silent click
    ]

    for i, test in enumerate(test_cases):
        logger.info(f"\nTest {i+1}: Event='{test['event']}', Msg='{test['msg']}'")
        
        start_time = time.time()
        result = await detect_intent(engine, test["event"], test["msg"])
        latency = time.time() - start_time
        
        logger.info(f"Result: {result.model_dump_json(indent=2)}")
        logger.info(f"Latency: {latency:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(run_intent_tests())