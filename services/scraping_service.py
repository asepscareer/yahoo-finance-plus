import logging
import json
import pandas as pd
import asyncio
import functools

from services.base_service import BaseYFinanceService
from cache.redis_adapter import cache_result
from redis import asyncio as aioredis
from util import to_timestamp, to_epoch
from util import TableScraper as use_selenium

logger = logging.getLogger(__name__)

class ScrapingService(BaseYFinanceService):
    def __init__(self, redis: aioredis.Redis):
        super().__init__(redis)

    @cache_result(ttl_seconds=600)
    async def pricecustomdate(self, symbol, start, end):
        url = ("https://finance.yahoo.com/quote/{symbol}/history/?period1={start}&period2={end}"
               .format(symbol=symbol, start=to_timestamp(start), end=to_timestamp(end)))

        logger.info(f"Scraping custom date price from URL: {url}")

        df = await self.scrape_table(url)
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            "Close Close price adjusted for splits.": "Close",
            "Adj Close Adjusted close price adjusted for splits and dividend and/or capital gain distributions.": "Adj Close"
        })

        df['Open'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(pd.to_numeric, df['Open'].astype(str).str.replace(',', '', regex=False), errors='coerce'))
        df['Close'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(pd.to_numeric, df['Close'].astype(str).str.replace(',', '', regex=False), errors='coerce'))
        df['High'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(pd.to_numeric, df['High'].astype(str).str.replace(',', '', regex=False), errors='coerce'))
        df['Low'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(pd.to_numeric, df['Low'].astype(str).str.replace(',', '', regex=False), errors='coerce'))
        df['Adj Close'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(pd.to_numeric, df['Adj Close'].astype(str).str.replace(',', '', regex=False), errors='coerce'))
        df['Date'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(df['Date'].astype(str).apply, to_epoch))
        df['Volume'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(df['Volume'].replace, '-', pd.NA))
        df['Volume'] = await asyncio.get_event_loop().run_in_executor(None, functools.partial(pd.to_numeric, df['Volume'].astype(str).str.replace(',', '', regex=False), errors='coerce'))

        buildJson = await asyncio.get_event_loop().run_in_executor(None, functools.partial(df.to_json, orient="records"))
        response = await asyncio.get_event_loop().run_in_executor(None, functools.partial(json.loads, buildJson))
        logger.info(f"Successfully scraped custom date price for symbol: {symbol}")
        return response

    async def scrape_table(self, url):
        logger.debug(f"Using Selenium to scrape table from: {url}")
        loop = asyncio.get_event_loop()
        df_scraper = await loop.run_in_executor(None, functools.partial(use_selenium, url))
        data = await loop.run_in_executor(None, df_scraper.get_data)
        if data:
            logger.debug("Successfully got data from Selenium scraper")
            return data[0]
        logger.warning("Selenium scraper returned no data")
        return pd.DataFrame()