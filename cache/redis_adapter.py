import asyncio
import functools
import hashlib
import json
import logging
from typing import Any, Callable, Optional
import pandas as pd
from io import StringIO

from .base import RedisAdapterBase

logger = logging.getLogger(__name__)

class RedisCacheAdapter(RedisAdapterBase):
    """
    An adapter to simplify using Redis as a cache.
    It handles JSON serialization and deserialization automatically.
    """

    async def get_cache(self, key: str) -> Optional[Any]:
        """
        Gets a value from the cache and deserializes it from JSON.

        Args:
            key: The cache key.

        Returns:
            The deserialized Python object, or None if the key doesn't exist.
        """
        cached_value = await self.redis.get(key)
        if cached_value:
            logger.info(f"Cache HIT for key: {key}")
            data = json.loads(cached_value)
            if isinstance(data, dict) and '__dataframe__' in data:
                # Deserialize DataFrame
                return pd.read_json(StringIO(data['__dataframe__']), orient='split')
            return data
        logger.info(f"Cache MISS for key: {key}")
        return None

    async def set_cache(self, key: str, value: Any, ttl_seconds: int):
        """
        Sets a value in the cache, serializing it to JSON.

        Args:
            key: The cache key.
            value: The Python object to cache.
            ttl_seconds: The time-to-live for the cache entry in seconds.
        """
        if isinstance(value, pd.DataFrame):
            # Special handling for DataFrames
            serialized_value = json.dumps({'__dataframe__': value.to_json(orient='split')})
        else:
            # Default JSON serialization
            serialized_value = json.dumps(value, default=str)
        await self.redis.set(key, serialized_value, ex=ttl_seconds)
        logger.info(f"Cache SET for key: {key} with TTL: {ttl_seconds} seconds")


def cache_result(ttl_seconds: int):
    """
    A decorator to cache the result of an async function in Redis.

    Args:
        ttl_seconds: The time-to-live for the cache entry in seconds.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(self: RedisAdapterBase, *args, **kwargs):
            # Create a stable cache key from function name, args, and kwargs
            arg_str = ",".join(map(str, args))
            kwarg_str = ",".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            raw_key = f"{func.__name__}:{arg_str}:{kwarg_str}"
            
            # Use a hash for a clean, fixed-length key
            cache_key = f"cache:{func.__module__}.{func.__name__}:{hashlib.md5(raw_key.encode()).hexdigest()}"

            # 'self' is expected to be an object with a 'redis' attribute,
            # like any class inheriting from RedisAdapterBase.
            cache_adapter = RedisCacheAdapter(self.redis)
            
            cached_value = await cache_adapter.get_cache(cache_key)
            if cached_value is not None:
                return cached_value

            # If not in cache, call the original function
            result = await func(self, *args, **kwargs)

            # Store the result in cache
            await cache_adapter.set_cache(cache_key, result, ttl_seconds)

            return result

        return wrapper

    return decorator