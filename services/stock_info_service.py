import logging
import asyncio
import functools
from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

class StockInfoService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=600)
    async def get_info(self, symbol: str) -> dict:
        logger.debug(f"Getting stock info for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        info = await loop.run_in_executor(None, lambda: ticker.info)
        return info

    @cache_result(ttl_seconds=600)
    async def get_price_history(self, symbol: str, period: str, interval: str) -> dict:
        logger.debug(f"Getting price history for symbol: {symbol} with period: {period} and interval: {interval}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        history = await loop.run_in_executor(None, functools.partial(ticker.history, period=period, interval=interval))
        logger.info(f"Response history data: {history}")
        return self._format_df_to_json(history.reset_index())

    @cache_result(ttl_seconds=600)
    async def get_max_price_history(self, symbol: str, interval: str) -> dict:
        logger.debug(f"Getting max price history for symbol: {symbol} with interval: {interval}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        history = await loop.run_in_executor(None, functools.partial(ticker.history, period="max", interval=interval))
        return self._format_df_to_json(history.reset_index())

    @cache_result(ttl_seconds=600)
    async def get_actions(self, symbol: str) -> dict:
        logger.debug(f"Getting actions for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        actions = await loop.run_in_executor(None, ticker.actions.reset_index)
        return self._format_df_to_json(actions)