import logging
from fastapi import APIRouter, Depends, Request

from domain.request import GlobalRequest
from domain.response import success
from services.dividends_splits_service import DividendsSplitsService
from util.helper import convert_keys_to_camel_case

router = APIRouter()
logger = logging.getLogger(__name__)

def get_dividends_splits_service(request: Request):
    return DividendsSplitsService(redis=request.app.state.redis)

@router.post("/dividends", summary="Get dividend data for a given symbol", tags=["Stock"], operation_id="get_dividends")
async def get_dividends(req: GlobalRequest, svc: DividendsSplitsService = Depends(get_dividends_splits_service)):
    logger.info(f"Getting dividends for symbol: {req.symbol}")
    response = await svc.get_dividend_data(req.symbol)
    logger.info(f"Successfully retrieved dividends for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/splits", summary="Get stock split data for a given symbol", tags=["Stock"], operation_id="get_splits")
async def get_splits(req: GlobalRequest, svc: DividendsSplitsService = Depends(get_dividends_splits_service)):
    logger.info(f"Getting splits for symbol: {req.symbol}")
    response = await svc.get_splits(req.symbol)
    logger.info(f"Successfully retrieved splits for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))
