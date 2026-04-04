"""
Drizzle — Request Logging Middleware
=====================================
Logs every inbound request with timing info.
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

log = logging.getLogger("drizzle.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.perf_counter()
        method = request.method
        path = request.url.path

        response = await call_next(request)

        elapsed = (time.perf_counter() - start) * 1000  # ms
        user_info = ""
        if hasattr(request.state, "user"):
            u = request.state.user
            user_info = f" user={u.get('uid', '?')} role={u.get('role', '?')}"

        log.info(
            f"{method} {path} → {response.status_code} "
            f"({elapsed:.1f}ms){user_info}"
        )
        return response
