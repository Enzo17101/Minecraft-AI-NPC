import json
import logging
import os
from typing import List, Dict, Optional
from redis.asyncio import Redis, from_url
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, redis_url: Optional[str] = None):
        # Force retrieval from the environment to fail fast if the configuration is missing
        url = redis_url or os.getenv("REDIS_URL")
        if not url:
            raise ValueError("Critical Error: REDIS_URL environment variable is missing.")
        
        # Explicit typing resolves unawaitable errors raised by Pylance
        self.redis_client: Redis = from_url(url, decode_responses=True)
        self.max_history_length = 10
        self.session_ttl_seconds = 300 
        
    async def add_message(self, session_id: str, role: str, content: str):
        """
        Pushes a new message into the list, trims the history, and resets the TTL.
        """
        message_data = json.dumps({"role": role, "content": content})
        
        try:
            # Grouping commands in a pipeline ensures atomicity and reduces network round trips
            async with self.redis_client.pipeline(transaction=True) as pipe:
                pipe.rpush(session_id, message_data)
                pipe.ltrim(session_id, -self.max_history_length, -1)
                pipe.expire(session_id, self.session_ttl_seconds)
                await pipe.execute()
                
        except RedisError as e:
            logger.error(f"Failed to add message to Redis for session {session_id}: {e}")

    async def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieves the active conversation history for the given session.
        """
        try:
            raw_history = await self.redis_client.lrange(session_id, 0, -1) # type: ignore
            return [json.loads(msg) for msg in raw_history]
        except RedisError as e:
            logger.error(f"Failed to retrieve history for session {session_id}: {e}")
            return []

    async def clear_session(self, session_id: str):
        """
        Forces the immediate deletion of a session from memory.
        """
        try:
            await self.redis_client.delete(session_id)
        except RedisError as e:
            logger.error(f"Failed to clear session {session_id}: {e}")

    async def close(self):
        """
        Cleanly closes the Redis connection pool. 
        Intended to be called during the FastAPI server shutdown sequence.
        """
        await self.redis_client.aclose()