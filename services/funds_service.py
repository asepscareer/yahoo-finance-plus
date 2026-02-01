import logging
import asyncio
import functools
from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

class FundsService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=3600)
    async def get_funds_data(self, symbol):
        logger.debug(f"Getting funds data for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        funds = await loop.run_in_executor(None, lambda: data.funds_data)
        logger.debug(f"Extracting top holdings for symbol: {symbol}")
        return self._format_df_to_json(funds.top_holdings)