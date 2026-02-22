import httpx
import asyncio
from typing import Dict, Optional

from config import settings


class WebhookClient:
    """
    Async webhook sender with retry + timeout protection.
    """

    def __init__(
        self,
        timeout: float = 5.0,
        retries: int = 2
    ):
        self.timeout = timeout
        self.retries = retries

    async def send(
        self,
        url: str,
        payload: Dict
    ) -> bool:

        for attempt in range(self.retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=payload)

                    if response.status_code < 300:
                        return True

            except Exception as e:
                print(f"Webhook attempt {attempt+1} failed: {e}")

            await asyncio.sleep(1)

        return False


# Optional singleton
webhook_client = WebhookClient()