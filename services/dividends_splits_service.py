import logging
import asyncio
import functools
from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

class DividendsSplitsService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=3600)
    async def get_dividend_data(self, symbol: str) -> dict:
        logger.debug(f"Getting dividend data for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        dividend_data = await loop.run_in_executor(None, ticker.dividends.reset_index)
        return self._format_df_to_json(dividend_data)

    @cache_result(ttl_seconds=3600)
    async def get_splits(self, symbol: str) -> dict:
        logger.debug(f"Getting splits data for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        splits_data = await loop.run_in_executor(None, ticker.splits.reset_index)
        return self._format_df_to_json(splits_data)