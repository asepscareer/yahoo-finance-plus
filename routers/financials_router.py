import logging
from fastapi import APIRouter, Depends, Request

from domain.request import GlobalRequest
from domain.response import success
from services.financials_service import FinancialsService

router = APIRouter()
logger = logging.getLogger(__name__)

def get_financials_service(request: Request):
    return FinancialsService(redis=request.app.state.redis)

@router.post("/financials", summary="Get annual financial statements", tags=["Financials"])
async def get_financials(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting financials for symbol: {req.symbol}")
    response = await svc.get_financials(req.symbol)
    logger.info(f"Successfully retrieved financials for symbol: {req.symbol}")
    return success(response)

@router.post("/quarterly-financials", summary="Get quarterly financial statements", tags=["Financials"])
async def get_quarterly_financials(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting quarterly financials for symbol: {req.symbol}")
    response = await svc.get_quarterly_financials(req.symbol)
    logger.info(f"Successfully retrieved quarterly financials for symbol: {req.symbol}")
    return success(response)
    
@router.post("/income-statement", summary="Get annual income statement", tags=["Financials"])
async def get_income_stmt(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting income statement for symbol: {req.symbol}")
    response = await svc.get_income_stmt(req.symbol)
    logger.info(f"Successfully retrieved income statement for symbol: {req.symbol}")
    return success(response)

@router.post("/quarterly-income-statement", summary="Get quarterly income statement", tags=["Financials"])
async def get_quarterly_income_stmt(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting quarterly income statement for symbol: {req.symbol}")
    response = await svc.get_quarterly_income_stmt(req.symbol)
    logger.info(f"Successfully retrieved quarterly income statement for symbol: {req.symbol}")
    return success(response)

@router.post("/balance-sheet", summary="Get annual balance sheet", tags=["Financials"])
async def get_balance_sheet(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting balance sheet for symbol: {req.symbol}")
    response = await svc.get_balance_sheet(req.symbol)
    logger.info(f"Successfully retrieved balance sheet for symbol: {req.symbol}")
    return success(response)

@router.post("/quarterly-balance-sheet", summary="Get quarterly balance sheet", tags=["Financials"])
async def get_quarterly_balance_sheet(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting quarterly balance sheet for symbol: {req.symbol}")
    response = await svc.get_quarterly_balance_sheet(req.symbol)
    logger.info(f"Successfully retrieved quarterly balance sheet for symbol: {req.symbol}")
    return success(response)

@router.post("/cash-flow", summary="Get annual cash flow statement", tags=["Financials"])
async def get_cash_flow(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting cash flow for symbol: {req.symbol}")
    response = await svc.get_cashflow(req.symbol)
    logger.info(f"Successfully retrieved cash flow for symbol: {req.symbol}")
    return success(response)

@router.post("/quarterly-cash-flow", summary="Get quarterly cash flow statement", tags=["Financials"])
async def get_quarterly_cash_flow(req: GlobalRequest, svc: FinancialsService = Depends(get_financials_service)):
    logger.info(f"Getting quarterly cash flow for symbol: {req.symbol}")
    response = await svc.get_quarterly_cashflow(req.symbol)
    logger.info(f"Successfully retrieved quarterly cash flow for symbol: {req.symbol}")
    return success(response)
