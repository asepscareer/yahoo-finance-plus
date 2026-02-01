from redis import asyncio as aioredis

class RedisAdapterBase:
    def __init__(self, redis: aioredis.Redis):
        if redis is None:
            raise ValueError("Redis client is not initialized.")
        self.redis = redis