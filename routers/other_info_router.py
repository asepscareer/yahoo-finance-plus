import logging
from fastapi import APIRouter, Depends, Request

from domain.request import GlobalRequest, OptionChainRequest
from domain.response import success
from services.other_info_service import OtherInfoService
from util.helper import convert_keys_to_camel_case

router = APIRouter()
logger = logging.getLogger(__name__)

def get_other_info_service(request: Request):
    return OtherInfoService(redis=request.app.state.redis)

@router.post("/alt-info", summary="Get alternative general information for a given symbol", tags=["Stock"], operation_id="get_simple_info")
async def get_simple_info(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting alt info for symbol: {req.symbol}")
    response = await svc.altinfo(req.symbol)
    logger.info(f"Successfully retrieved alt info for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/earnings-dates", summary="Get upcoming earnings dates for a given symbol", tags=["Stock"], operation_id="get_earnings_dates")
async def get_earnings_dates(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting earnings dates for symbol: {req.symbol}")
    response = await svc.get_earnings_dates(req.symbol)
    logger.info(f"Successfully retrieved earnings dates for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/calendar", summary="Get economic calendar events for a given symbol", tags=["Calendar"], operation_id="get_calendar")
async def get_calendar(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting calendar for symbol: {req.symbol}")
    response = await svc.get_calendar(req.symbol)
    logger.info(f"Successfully retrieved calendar for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))
    
@router.post("/sustainability", summary="Get sustainability data for a given symbol", tags=["Analysis"], operation_id="get_sustainability")
async def get_sustainability(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting sustainability for symbol: {req.symbol}")
    response = await svc.get_sustainability(req.symbol)
    logger.info(f"Successfully retrieved sustainability for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/recommendations", summary="Get analyst recommendations for a given symbol", tags=["Analysis"], operation_id="get_recommendations")
async def get_recommendations(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting recommendations for symbol: {req.symbol}")
    response = await svc.get_recommendations(req.symbol)
    logger.info(f"Successfully retrieved recommendations for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/recommendations-summary", summary="Get a summary of analyst recommendations for a given symbol", tags=["Analysis"], operation_id="get_recommendations_summary")
async def get_recommendations_summary(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting recommendations summary for symbol: {req.symbol}")
    response = await svc.get_recommendations_summary(req.symbol)
    logger.info(f"Successfully retrieved recommendations summary for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/analyst-price-targets", summary="Get analyst price targets for a given symbol", tags=["Analysis"], operation_id="get_analyst_price_targets")
async def get_analyst_price_targets(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting analyst price targets for symbol: {req.symbol}")
    response = await svc.get_analyst_price_targets(req.symbol)
    logger.info(f"Successfully retrieved analyst price targets for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/revenue-estimate", summary="Get revenue estimates for a given symbol", tags=["Analysis"], operation_id="get_revenue_estimate")
async def get_revenue_estimate(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting revenue estimate for symbol: {req.symbol}")
    response = await svc.get_revenue_estimate(req.symbol)
    logger.info(f"Successfully retrieved revenue estimate for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/earnings-estimate", summary="Get earnings estimates for a given symbol", tags=["Analysis"], operation_id="get_earnings_estimate")
async def get_earnings_estimate(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting earnings estimate for symbol: {req.symbol}")
    response = await svc.get_earnings_estimate(req.symbol)
    logger.info(f"Successfully retrieved earnings estimate for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/growth-estimates", summary="Get growth estimates for a given symbol", tags=["Analysis"], operation_id="get_growth_estimates")
async def get_growth_estimates(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting growth estimates for symbol: {req.symbol}")
    response = await svc.get_growth_estimates(req.symbol)
    logger.info(f"Successfully retrieved growth estimates for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/upgrades-downgrades", summary="Get analyst upgrades and downgrades for a given symbol", tags=["Analysis"], operation_id="get_upgrades_downgrades")
async def get_upgrades_downgrades(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting upgrades/downgrades for symbol: {req.symbol}")
    response = await svc.get_upgrades_downgrades(req.symbol)
    logger.info(f"Successfully retrieved upgrades/downgrades for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/isin", summary="Get ISIN (International Securities Identification Number) for a given symbol", tags=["Stock"], operation_id="get_isin")
async def get_isin(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting ISIN for symbol: {req.symbol}")
    response = await svc.get_isin(req.symbol)
    logger.info(f"Successfully retrieved ISIN for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/capital-gains", summary="Get capital gains data for a given symbol", tags=["Stock"], operation_id="get_capital_gains")
async def get_capital_gains(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting capital gains for symbol: {req.symbol}")
    response = await svc.get_capital_gains(req.symbol)
    logger.info(f"Successfully retrieved capital gains for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/news", summary="Get news articles for a given symbol", tags=["Stock"], operation_id="get_news")
async def get_news(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting news for symbol: {req.symbol}")
    response = await svc.get_news(req.symbol)
    logger.info(f"Successfully retrieved news for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/options", summary="Get available option expiration dates for a given symbol", tags=["Stock"], operation_id="get_options")
async def get_options(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting options for symbol: {req.symbol}")
    response = await svc.get_options(req.symbol)
    logger.info(f"Successfully retrieved options for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))
    
@router.post("/option-chain", summary="Get option chain data for a specific symbol and expiration date. The 'date' parameter should be one of the dates returned by the '/options' endpoint.", tags=["Stock"], operation_id="get_option_chain")
async def get_option_chain(req: OptionChainRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting option chain for symbol: {req.symbol} on date: {req.date}")
    response = await svc.get_option_chain(req.symbol, req.date)
    logger.info(f"Successfully retrieved option chain for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))

@router.post("/shares-full", summary="Get full shares data for a given symbol", tags=["Stock"], operation_id="get_shares_full")
async def get_shares_full(req: GlobalRequest, svc: OtherInfoService = Depends(get_other_info_service)):
    logger.info(f"Getting full shares for symbol: {req.symbol}")
    response = await svc.get_shares_full(req.symbol)
    logger.info(f"Successfully retrieved full shares for symbol: {req.symbol}")
    return success(convert_keys_to_camel_case(response))
