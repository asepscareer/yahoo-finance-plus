import logging
import json
import yfinance as yf
import pandas as pd
from redis import asyncio as aioredis

logger = logging.getLogger(__name__)

class BaseYFinanceService:
    def __init__(self, redis: aioredis.Redis):
        if redis is None:
            raise ValueError("Redis client is not initialized.")
        self.redis = redis
        
    def _get_ticker(self, symbol: str) -> yf.Ticker:
        logger.debug(f"Creating yfinance.Ticker object for symbol: {symbol}")
        return yf.Ticker(symbol)

    def _format_df_to_json(self, df: pd.DataFrame) -> dict:
        logger.debug("Formatting DataFrame to JSON (orient=records)")
        return json.loads(df.to_json(orient="records", date_format="iso"))

    def _format_df_to_json_index(self, df: pd.DataFrame) -> dict:
        logger.debug("Formatting DataFrame to JSON (orient=index)")
        return json.loads(df.to_json(orient="index"))

    def _format_series_to_json(self, series: pd.Series) -> dict:
        logger.debug("Formatting Series to JSON")
        return json.loads(series.to_json(orient="index"))
