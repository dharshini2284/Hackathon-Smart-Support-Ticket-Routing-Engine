import asyncio
from typing import Dict


class LockManager:
    """
    Named async lock manager.
    Ensures safe concurrent access to shared resources.
    """

    def __init__(self):
        self._locks: Dict[str, asyncio.Lock] = {}
        self._registry_lock = asyncio.Lock()

    async def _get_lock(self, name: str) -> asyncio.Lock:
        """
        Returns existing lock or creates one safely.
        """
        async with self._registry_lock:
            if name not in self._locks:
                self._locks[name] = asyncio.Lock()
            return self._locks[name]

    async def acquire(self, name: str):
        lock = await self._get_lock(name)
        await lock.acquire()

    async def release(self, name: str):
        async with self._registry_lock:
            lock = self._locks.get(name)

        if lock and lock.locked():
            lock.release()

    def get_lock(self, name: str):
        """
        Context manager usage:
        async with lock_manager.get_lock("agent"):
            ...
        """

        manager = self

        class _LockContext:
            async def __aenter__(self_inner):
                await manager.acquire(name)

            async def __aexit__(self_inner, exc_type, exc, tb):
                await manager.release(name)

        return _LockContext()


# Optional: Global singleton
lock_manager = LockManager()