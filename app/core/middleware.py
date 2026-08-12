import logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.context import reset_request_id, set_request_id

logger = logging.getLogger(__name__)

HTTP_REQUESTS = Counter(
    "survey_pal_http_requests_total",
    "Total HTTP requests",
    ("method", "route", "status_code"),
)
HTTP_DURATION = Histogram(
    "survey_pal_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ("method", "route"),
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID") or f"req_{uuid4().hex}"
        token = set_request_id(request_id)
        started_at = perf_counter()
        response: Response | None = None
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            route = request.scope.get("route")
            route_path = getattr(route, "path", request.url.path)
            duration_seconds = perf_counter() - started_at
            HTTP_REQUESTS.labels(request.method, route_path, str(status_code)).inc()
            HTTP_DURATION.labels(request.method, route_path).observe(duration_seconds)
            logger.info(
                "HTTP request completed",
                extra={
                    "method": request.method,
                    "route": route_path,
                    "status_code": status_code,
                    "duration_ms": round(duration_seconds * 1000, 2),
                },
            )
            reset_request_id(token)
