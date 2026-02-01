import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: Exception):
    logger.warning(
        f"HTTP Exception caught: status_code={exc.status_code}, detail={exc.detail}",
        extra={"trace_id": request.headers.get('X-Request-ID')}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "An unexpected error occurred. Please contact the API provider for assistance."},
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception caught",
        exc_info=True,
        extra={"trace_id": request.headers.get('X-Request-ID')}
    )
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please contact the API provider for assistance."},
    )
