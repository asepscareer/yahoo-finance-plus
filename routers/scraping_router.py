import logging
from fastapi import APIRouter, Depends, Request

from domain.request import PriceCustomRequest
from domain.response import success
from services.scraping_service import ScrapingService

router = APIRouter()
logger = logging.getLogger(__name__)

def get_scraping_service(request: Request):
    return ScrapingService(redis=request.app.state.redis)

@router.post("/price-custom-date", summary="Get historical price data for a custom date range by scraping", tags=["Stock"])
async def price_custom_date(req: PriceCustomRequest, svc: ScrapingService = Depends(get_scraping_service)):
    logger.info(f"Getting custom date price for symbol: {req.symbol} from {req.start} to {req.end}")
    response = await svc.pricecustomdate(req.symbol, req.start, req.end)
    logger.info(f"Successfully retrieved custom date price for symbol: {req.symbol}")
    return success(response)