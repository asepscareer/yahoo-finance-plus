import uuid
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request

TRACE_ID_HEADER = "X-Request-ID"
trace_id_var = ContextVar(TRACE_ID_HEADER, default=None)

async def trace_id_middleware(request: Request, call_next: RequestResponseEndpoint):
    # Get trace ID from headers or generate a new one
    trace_id = request.headers.get(TRACE_ID_HEADER) or str(uuid.uuid4())
    
    # Set the trace ID in the context variable
    token = trace_id_var.set(trace_id)
    
    response = await call_next(request)
    
    # Add trace ID to response headers
    response.headers[TRACE_ID_HEADER] = trace_id
    
    # Reset the context variable
    trace_id_var.reset(token)
    
    return response
