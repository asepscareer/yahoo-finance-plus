import logging
from fastapi import APIRouter, Depends, Request

from domain.request import GlobalRequest
from domain.response import success
from services.holders_service import HoldersService

router = APIRouter()
logger = logging.getLogger(__name__)

def get_holders_service(request: Request):
    return HoldersService(redis=request.app.state.redis)

@router.post("/major-holders", summary="Get major holders data for a given symbol", tags=["Holdings"])
async def get_major_holders(req: GlobalRequest, svc: HoldersService = Depends(get_holders_service)):
    logger.info(f"Getting major holders for symbol: {req.symbol}")
    response = await svc.get_major_holders(req.symbol)
    logger.info(f"Successfully retrieved major holders for symbol: {req.symbol}")
    return success(response)

@router.post("/institutional-holders", summary="Get institutional holders data for a given symbol", tags=["Holdings"])
async def get_institutional_holders(req: GlobalRequest, svc: HoldersService = Depends(get_holders_service)):
    logger.info(f"Getting institutional holders for symbol: {req.symbol}")
    response = await svc.get_institutional_holders(req.symbol)
    logger.info(f"Successfully retrieved institutional holders for symbol: {req.symbol}")
    return success(response)

@router.post("/mutual-fund-holders", summary="Get mutual fund holders data for a given symbol", tags=["Holdings"])
async def get_mutual_fund_holders(req: GlobalRequest, svc: HoldersService = Depends(get_holders_service)):
    logger.info(f"Getting mutual fund holders for symbol: {req.symbol}")
    response = await svc.get_mutual_fund_holders(req.symbol)
    logger.info(f"Successfully retrieved mutual fund holders for symbol: {req.symbol}")
    return success(response)

@router.post("/insider-roster-holders", summary="Get insider roster holders data for a given symbol", tags=["Holdings"])
async def get_insider_roster_holders(req: GlobalRequest, svc: HoldersService = Depends(get_holders_service)):
    logger.info(f"Getting insider roster holders for symbol: {req.symbol}")
    response = await svc.get_insider_roster_holders(req.symbol)
    logger.info(f"Successfully retrieved insider roster holders for symbol: {req.symbol}")
    return success(response)

@router.post("/insider-transactions", summary="Get insider transactions data for a given symbol", tags=["Holdings"])
async def get_insider_transactions(req: GlobalRequest, svc: HoldersService = Depends(get_holders_service)):
    logger.info(f"Getting insider transactions for symbol: {req.symbol}")
    response = await svc.get_insider_transactions(req.symbol)
    logger.info(f"Successfully retrieved insider transactions for symbol: {req.symbol}")
    return success(response)

@router.post("/insider-purchases", summary="Get insider purchases data for a given symbol", tags=["Holdings"])
async def get_insider_purchases(req: GlobalRequest, svc: HoldersService = Depends(get_holders_service)):
    logger.info(f"Getting insider purchases for symbol: {req.symbol}")
    response = await svc.get_insider_purchases(req.symbol)
    logger.info(f"Successfully retrieved insider purchases for symbol: {req.symbol}")
    return success(response)