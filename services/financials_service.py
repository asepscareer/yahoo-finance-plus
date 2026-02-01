import logging
import asyncio
import functools
from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

class FinancialsService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=3600)
    async def get_financials(self, symbol: str) -> dict:
        logger.debug(f"Getting financials for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        financial_data = await loop.run_in_executor(None, ticker.financials.reset_index)
        return self._format_df_to_json(financial_data)

    @cache_result(ttl_seconds=3600)
    async def get_quarterly_financials(self, symbol: str) -> dict:
        logger.debug(f"Getting quarterly financials for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        quarterly_financials = await loop.run_in_executor(None, ticker.quarterly_financials.reset_index)
        return self._format_df_to_json(quarterly_financials)

    @cache_result(ttl_seconds=3600)
    async def get_balance_sheet(self, symbol: str) -> dict:
        logger.debug(f"Getting balance sheet for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        balance_sheet = await loop.run_in_executor(None, ticker.balance_sheet.reset_index)
        return self._format_df_to_json(balance_sheet)

    @cache_result(ttl_seconds=3600)
    async def get_quarterly_balance_sheet(self, symbol: str) -> dict:
        logger.debug(f"Getting quarterly balance sheet for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        quarterly_balance_sheet = await loop.run_in_executor(None, ticker.quarterly_balance_sheet.reset_index)
        return self._format_df_to_json(quarterly_balance_sheet)

    @cache_result(ttl_seconds=3600)
    async def get_cashflow(self, symbol: str) -> dict:
        logger.debug(f"Getting cash flow for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        cash_flow_data = await loop.run_in_executor(None, ticker.cashflow.reset_index)
        return self._format_df_to_json(cash_flow_data)

    @cache_result(ttl_seconds=3600)
    async def get_quarterly_cashflow(self, symbol: str) -> dict:
        logger.debug(f"Getting quarterly cash flow for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        quarterly_cashflow = await loop.run_in_executor(None, ticker.quarterly_cashflow.reset_index)
        return self._format_df_to_json(quarterly_cashflow)

    @cache_result(ttl_seconds=3600)
    async def get_income_stmt(self, symbol):
        logger.debug(f"Getting income statement for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: data.income_stmt)
        return self._format_df_to_json_index(df)

    @cache_result(ttl_seconds=3600)
    async def get_quarterly_income_stmt(self, symbol):
        logger.debug(f"Getting quarterly income statement for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: data.quarterly_income_stmt)
        return self._format_df_to_json_index(df)