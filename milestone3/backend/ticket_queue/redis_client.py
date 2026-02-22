import asyncio
import json
from typing import Any, Callable, Optional

import redis.asyncio as redis
from config import settings

class RedisBroker:

    def __init__(
        self,
        redis_url: str = settings.REDIS_URL,
        queue_name: str = settings.REDIS_QUEUE
    ):
        self.queue_name = queue_name
        self.redis: Optional[redis.Redis] = redis.from_url(
            redis_url, 
            decode_responses=True
        )
        # <-- Add processed counter
        self.processed_count = 0

    # --------------------------------------------
    # Publish Message
    # --------------------------------------------
    async def publish(self, message: Any):
        try:
            await self.redis.rpush(
                self.queue_name,
                json.dumps(message)
            )
        except Exception as e:
            print(f"Redis publish error: {e}")

    # --------------------------------------------
    # Consume Message (Blocking)
    # --------------------------------------------
    async def consume(self) -> Any:
        try:
            result = await self.redis.blpop(
                self.queue_name
            )

            if result:
                _, message = result
                return json.loads(message)

        except Exception as e:
            print(f"Redis consume error: {e}")

        return None

    # --------------------------------------------
    # Worker Loop
    # --------------------------------------------
    async def start_worker(
        self,
        handler: Callable[[Any], Any]
    ):
        while True:
            message = await self.consume()

            if message is None:
                await asyncio.sleep(1)
                continue

            try:
                await handler(message)
                # <-- Increment processed counter after successful handling
                self.processed_count += 1
            except Exception as e:
                print(f"Worker processing error: {e}")