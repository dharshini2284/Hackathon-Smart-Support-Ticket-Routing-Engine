import asyncio
import json
from typing import Any, Callable, Optional

import redis.asyncio as redis  # <- this is crucial

REDIS_HOST = "localhost"
REDIS_PORT = 6379
QUEUE_NAME = "ticket_queue"
class RedisBroker:

    def __init__(
        self,
        host: str = REDIS_HOST,
        port: int = REDIS_PORT,
        queue_name: str = QUEUE_NAME
    ):
        self.queue_name = queue_name
        self.redis: Optional[redis.Redis] = redis.Redis(
            host=host,
            port=port,
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