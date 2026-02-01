import logging
import json
import pandas as pd
import asyncio
import functools

from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis
from util import default_converter

logger = logging.getLogger(__name__)

class OtherInfoService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=600)
    async def altinfo(self, symbol):
        logger.debug(f"Getting alternative info for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        fast_info = await loop.run_in_executor(None, lambda: ticker.fast_info)

        data = {
            'currency': fast_info['currency'],
            'day_high': fast_info['dayHigh'],
            'day_low': fast_info['dayLow'],
            'exchange': fast_info['exchange'],
            'fifty_day_average': fast_info['fiftyDayAverage'],
            'last_price': fast_info['lastPrice'],
            'last_volume': fast_info['lastVolume'],
            'market_cap': fast_info['marketCap'],
            'open': fast_info['open'],
            'previous_close': fast_info['previousClose'],
            'quote_type': fast_info['quoteType'],
            'regular_market_previous_close': fast_info['regularMarketPreviousClose'],
            'shares': fast_info['shares'],
            'ten_day_average_volume': fast_info['tenDayAverageVolume'],
            'three_month_average_volume': fast_info['threeMonthAverageVolume'],
            'timezone': fast_info['timezone'],
            'two_hundred_day_average': fast_info['twoHundredDayAverage'],
            'year_change': fast_info['yearChange'],
            'year_high': fast_info['yearHigh'],
            'year_low': fast_info['yearLow']
        }
        return data

    @cache_result(ttl_seconds=600)
    async def get_earnings_dates(self, symbol: str) -> dict:
        logger.debug(f"Getting earnings dates for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        earnings_dates_df = await loop.run_in_executor(None, ticker.earnings_dates.reset_index)
        return self._format_df_to_json(earnings_dates_df)

    @cache_result(ttl_seconds=600)
    async def get_calendar(self, symbol: str) -> dict:
        logger.debug(f"Getting calendar for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        calendar_data = await loop.run_in_executor(None, lambda: ticker.calendar)
        calendar_json = await loop.run_in_executor(None, functools.partial(json.dumps, calendar_data, default=default_converter))
        response = await loop.run_in_executor(None, functools.partial(json.loads, calendar_json))
        return response

    @cache_result(ttl_seconds=600)
    async def get_sustainability(self, symbol: str) -> dict:
        logger.debug(f"Getting sustainability for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.sustainability)
        df = await loop.run_in_executor(None, df.reset_index)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_recommendations(self, symbol: str) -> dict:
        logger.debug(f"Getting recommendations for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.recommendations)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_recommendations_summary(self, symbol: str) -> dict:
        logger.debug(f"Getting recommendations summary for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.recommendations_summary)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_analyst_price_targets(self, symbol: str) -> dict:
        logger.debug(f"Getting analyst price targets for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        data = await loop.run_in_executor(None, lambda: ticker.analyst_price_targets)
        return data

    @cache_result(ttl_seconds=600)
    async def get_revenue_estimate(self, symbol: str) -> dict:
        logger.debug(f"Getting revenue estimate for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.revenue_estimate)
        df = await loop.run_in_executor(None, df.reset_index)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_earnings_estimate(self, symbol: str) -> dict:
        logger.debug(f"Getting earnings estimate for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.earnings_estimate)
        df = await loop.run_in_executor(None, df.reset_index)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_growth_estimates(self, symbol: str) -> dict:
        logger.debug(f"Getting growth estimates for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.growth_estimates)
        df = await loop.run_in_executor(None, df.reset_index)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_upgrades_downgrades(self, symbol: str) -> dict:
        logger.debug(f"Getting upgrades/downgrades for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, lambda: ticker.upgrades_downgrades)
        df = await loop.run_in_executor(None, df.reset_index)
        return self._format_df_to_json(df)

    @cache_result(ttl_seconds=600)
    async def get_capital_gains(self, symbol):
        logger.debug(f"Getting capital gains for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        response = await loop.run_in_executor(None, data.capital_gains.tolist)
        return response

    @cache_result(ttl_seconds=600)
    async def get_isin(self, symbol):
        logger.debug(f"Getting ISIN for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        response = await loop.run_in_executor(None, lambda: data.isin)
        return response

    @cache_result(ttl_seconds=600)
    async def get_news(self, symbol):
        logger.debug(f"Getting news for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        response = await loop.run_in_executor(None, lambda: data.news)
        return response

    @cache_result(ttl_seconds=600)
    async def get_options(self, symbol):
        logger.debug(f"Getting options for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        response = await loop.run_in_executor(None, lambda: data.options)
        return response

    @cache_result(ttl_seconds=600)
    async def get_option_chain(self, symbol, date):
        logger.debug(f"Getting option chain for symbol: {symbol}, date: {date}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        opt = await loop.run_in_executor(None, functools.partial(data.option_chain, date))
        option_calls = await loop.run_in_executor(None, lambda: opt.calls)
        option_puts = await loop.run_in_executor(None, lambda: opt.puts)
        option_callsJson = await loop.run_in_executor(None, functools.partial(option_calls.to_json, orient="records"))
        option_putsJson = await loop.run_in_executor(None, functools.partial(option_puts.to_json, orient="records"))
        response_calls = await loop.run_in_executor(None, functools.partial(json.loads, option_callsJson))
        response_puts = await loop.run_in_executor(None, functools.partial(json.loads, option_putsJson))
        response = [response_calls, response_puts]
        return response

    @cache_result(ttl_seconds=600)
    async def get_shares_full(self, symbol):
        logger.debug(f"Getting full shares for symbol: {symbol}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, functools.partial(self._get_ticker, symbol))
        df = await loop.run_in_executor(None, data.get_shares_full)
        df = await loop.run_in_executor(None, df.reset_index)
        df = await loop.run_in_executor(None, functools.partial(df.rename, columns={'index': 'time', 0: 'shares'}))
        return self._format_df_to_json(df)