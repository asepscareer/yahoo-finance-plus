from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from datetime import datetime

def validate_date_format(v: str) -> str:
    """Validator to check date format is DD-MM-YYYY"""
    if v is None:
        return v
    try:
        datetime.strptime(v, "%d-%m-%Y")
        return v
    except ValueError:
        raise ValueError("Incorrect date format, should be DD-MM-YYYY")
    

def option_chain_date_format(v: str) -> str:
    """Validator to check date format is YYYY-MM-DD"""
    if v is None:
        return v
    try:
        datetime.strptime(v, "%Y-%m-%d")
        return v
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

class PriceCustomRequest(BaseModel):
    symbol: str = "AAPL"
    start: str = "01-01-2026"
    end: str = "31-01-2026"

    @field_validator('start', 'end')
    def check_dates(cls, v: str) -> str:
        return validate_date_format(v)


class PriceRequest(BaseModel):
    symbol: str = "AAPL"
    period: Optional[Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]] = "1mo"
    interval: Optional[Literal["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]] = "1d"
    start: int = 1
    limit: int = 10


class MaxPriceRequest(BaseModel):
    symbol: str = "AAPL"
    interval: Optional[Literal["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]] = "1d"
    start: int = 1
    limit: int = 10

class GlobalRequest(BaseModel):
    symbol: str = "AAPL"

class OptionChainRequest(BaseModel):
    symbol: str = "AAPL"
    date: Optional[str] = "2026-02-06"

    @field_validator('date')
    def check_date(cls, v: str) -> str:
        return option_chain_date_format(v)