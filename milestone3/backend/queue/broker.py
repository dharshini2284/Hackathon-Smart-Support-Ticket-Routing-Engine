import asyncio
from typing import Callable, Any


# --------------------------------------------
# In-Memory Async Broker
# --------------------------------------------

class InMemoryBroker:

    def __init__(self):
        self.queue = asyncio.Queue()

    # --------------------------------------------
    # Publish Message
    # --------------------------------------------

    async def publish(self, message: Any):
        await self.queue.put(message)

    # --------------------------------------------
    # Consume Message
    # --------------------------------------------

    async def consume(self):
        message = await self.queue.get()
        self.queue.task_done()
        return message

    # --------------------------------------------
    # Start Worker Loop
    # --------------------------------------------

    async def start_worker(
        self,
        handler: Callable[[Any], Any]
    ):
        while True:
            message = await self.consume()
            try:
                await handler(message)
            except Exception as e:
                print(f"Worker error: {e}")