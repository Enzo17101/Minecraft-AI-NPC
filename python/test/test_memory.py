import pytest
import logging
from src.services.memory_manager import MemoryManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The pytest.mark.asyncio decorator tells the test runner to handle the async event loop automatically
@pytest.mark.asyncio
async def test_sliding_window_memory():
    logger.info("Starting Redis Memory Manager Tests with Pytest")
    
    memory = MemoryManager()
    session_id = "test_player_eldon"
    
    # Ensure a clean slate before executing the core logic
    await memory.clear_session(session_id)
    
    logger.info("Simulating a long conversation to trigger the trimming mechanism...")
    for i in range(1, 16):
        await memory.add_message(session_id, "user", f"Test message {i}")
        
    history = await memory.get_history(session_id)
    
    # Assertions replace manual log reading by strictly validating expected behavior
    assert len(history) == 10, f"Expected exactly 10 messages, but got {len(history)}"
    assert history[0]["content"] == "Test message 6", "The oldest message should be the 6th one sent"

    for i in range(0, len(history)):
        logger.info(f"history {i}: {history[i]}")

    # Clean up the database and close connections to prevent resource leaks
    await memory.clear_session(session_id)
    await memory.close()
    
    logger.info("Test passed successfully.")