import logging
from fastapi import APIRouter, Depends, Request

from domain.request import PriceRequest, MaxPriceRequest, GlobalRequest
from domain.response import success
from services.stock_info_service import StockInfoService
from util.helper import get_paginated_list, convert_keys_to_camel_case

router = APIRouter()
logger = logging.getLogger(__name__)

def get_stock_info_service(request: Request):
    return StockInfoService(redis=request.app.state.redis)

@router.post("/info", summary="Get general stock information", tags=["Stock"], operation_id="get_stock_info")
async def get_stock_info(req: GlobalRequest, yf_service: StockInfoService = Depends(get_stock_info_service)):
    logger.info(f"Getting stock info for symbol: {req.symbol}")
    stock_info = await yf_service.get_info(req.symbol)
    logger.info(f"Successfully retrieved stock info for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(stock_info))

@router.post("/price", summary="Get historical price data for a specified period and interval", tags=["Stock"], operation_id="get_price")
async def get_price(req: PriceRequest, yf_service: StockInfoService = Depends(get_stock_info_service)):
    logger.info(f"Getting price history for symbol: {req.symbol} with period: {req.period} and interval: {req.interval}")
    price_data = await yf_service.get_price_history(req.symbol, req.period, req.interval)
    logger.info(f"Successfully retrieved price history for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(price_data))

@router.post("/price-max-history", summary="Get maximum historical price data with pagination", tags=["Stock"], operation_id="price_max_history")
async def price_max_history(req: MaxPriceRequest, yf_service: StockInfoService = Depends(get_stock_info_service)):
    logger.info(f"Getting max price history for symbol: {req.symbol} with interval: {req.interval}")
    response = await yf_service.get_max_price_history(req.symbol, req.interval)
    response = convert_keys_to_camel_case(response)
    paginated_data = get_paginated_list(response, f'/{req.symbol}/price-max-history', page=req.start, limit=req.limit)
    logger.info(f"Successfully retrieved max price history for symbol: {req.symbol}")
    return success(paginated_data)