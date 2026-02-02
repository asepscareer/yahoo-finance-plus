import logging
from fastapi import APIRouter, Depends, Request

from domain.request import GlobalRequest
from domain.response import success
from services.funds_service import FundsService
from util.helper import convert_keys_to_camel_case

router = APIRouter()
logger = logging.getLogger(__name__)

def get_funds_service(request: Request):
    return FundsService(redis=request.app.state.redis)

@router.post("/funds-data", summary="Get funds data for a given symbol", tags=["Holdings"], operation_id="get_funds_data")
async def get_funds_data(req: GlobalRequest, svc: FundsService = Depends(get_funds_service)):
    logger.info(f"Getting funds data for symbol: {req.symbol}")
    response = await svc.get_funds_data(req.symbol)
    logger.info(f"Successfully retrieved funds data for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))
