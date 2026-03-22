import redis.asyncio as asyncredis
from typing import TypeVar
from  core.config import settings

KeyT = TypeVar('KeyT')

class RedisClient:
    def __init__(self, host: str, port: int, db: int):
        self._connection = asyncredis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )

    async def get_value(self, name: KeyT) -> str:
        return await self._connection.get(name)
    
    async def set_value(self, name: KeyT, value: str, ex: int = None):
        await self._connection.set(name, value, ex=ex)
    
    async def ping(self) -> str:
        return await self._connection.ping()
    
    async def get_values(self, pattern: str) -> list[str]:
        return await self._connection.keys(pattern)
    
redis_client = RedisClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)