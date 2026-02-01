from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from redis import asyncio as aioredis

from exceptions import http_exception_handler, unhandled_exception_handler
from routers.stock_info_router import router as stock_info_router
from routers.financials_router import router as financials_router
from routers.holders_router import router as holders_router
from routers.dividends_splits_router import router as dividends_splits_router
from routers.other_info_router import router as other_info_router
from routers.scraping_router import router as scraping_router
from routers.funds_router import router as funds_router
from util.request_context import trace_id_middleware


@asynccontextmanager
async def _lifespan(app: FastAPI):
    redis_url = f"redis://default:wXewwNFntlQAhZJbAeszQUbPcEfoFywL@metro.proxy.rlwy.net:50331/0"
    redis = aioredis.from_url(redis_url)
    app.state.redis = redis

    yield
    await app.state.redis.close()

def _create_application() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=trace_id_middleware)

    app.include_router(stock_info_router, prefix="/api/v1")
    app.include_router(financials_router, prefix="/api/v1")
    app.include_router(holders_router, prefix="/api/v1")
    app.include_router(dividends_splits_router, prefix="/api/v1")
    app.include_router(other_info_router, prefix="/api/v1")
    app.include_router(scraping_router, prefix="/api/v1")
    app.include_router(funds_router, prefix="/api/v1")

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    return app


app = _create_application()
