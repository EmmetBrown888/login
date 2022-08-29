"""Services module."""

from aioredis import Redis


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def process(self, key: str, value: str) -> str:
        await self._redis.set(key, value, expire=600)
        return await self._redis.get(key, encoding="utf-8")
