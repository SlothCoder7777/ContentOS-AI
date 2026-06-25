import logging
import os
import sys
from time import perf_counter

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger("contentos.api")
        start_time = perf_counter()
        response: Response | None = None

        try:
            response = await call_next(request)
            return response

        finally:
            duration_ms = round((perf_counter() - start_time) * 1000, 2)
            status_code = response.status_code if response else 500

            logger.info(
                "%s %s %s %.2fms",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
            )
