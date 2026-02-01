import logging
import asyncio
import functools
from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

class HoldersService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=3600)
    async def get_major_holders(self, symbol: str) -> dict:
        logger.debug(f"Getting major holders for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        major_holders_data = await loop.run_in_executor(None, ticker.major_holders.reset_index)
        major_holders_data = await loop.run_in_executor(None, functools.partial(major_holders_data.rename, columns={0: 'percentage', 1: 'description'}))
        return self._format_df_to_json(major_holders_data)

    @cache_result(ttl_seconds=3600)
    async def get_institutional_holders(self, symbol: str) -> dict:
        logger.debug(f"Getting institutional holders for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        institutional_holders_data = await loop.run_in_executor(None, lambda: ticker.institutional_holders)
        return self._format_df_to_json(institutional_holders_data)

    @cache_result(ttl_seconds=3600)
    async def get_mutual_fund_holders(self, symbol: str) -> dict:
        logger.debug(f"Getting mutual fund holders for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.mutualfund_holders)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=3600)
    async def get_insider_roster_holders(self, symbol: str) -> dict:
        logger.debug(f"Getting insider roster holders for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.insider_roster_holders)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=3600)
    async def get_insider_transactions(self, symbol: str) -> dict:
        logger.debug(f"Getting insider transactions for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.insider_transactions)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=3600)
    async def get_insider_purchases(self, symbol: str) -> dict:
        logger.debug(f"Getting insider purchases for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.insider_purchases)
        return self._format_df_to_json(df)