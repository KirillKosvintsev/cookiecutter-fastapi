import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, \
    RequestResponseEndpoint
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings


class EndpointExecutionTimeLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.debug(f"Endpoint executed in {process_time} seconds")

        return response


def setup_middleware(app: FastAPI):
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if settings.profile_endpoints:
        app.add_middleware(EndpointExecutionTimeLoggingMiddleware)
