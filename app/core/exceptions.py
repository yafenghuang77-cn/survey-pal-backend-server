import logging
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.response import error

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AppException(Exception):
    code: int
    message: str
    status_code: int = 400
    details: dict[str, Any] | list[Any] | None = field(default=None)


def _json_error(
    status_code: int,
    code: int,
    message: str,
    details: dict[str, Any] | list[Any] | None = None,
) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=error(code, message, details).model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(_request: Request, exc: AppException) -> JSONResponse:
        return _json_error(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            {"field": ".".join(str(part) for part in item["loc"]), "message": item["msg"]}
            for item in exc.errors()
        ]
        return _json_error(422, 10001, "参数校验失败", details)

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        code = 10004 if exc.status_code == 404 else 10000
        message = "请求的资源不存在" if exc.status_code == 404 else str(exc.detail)
        return _json_error(exc.status_code, code, message)

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled application exception",
            extra={"method": request.method, "route": request.url.path},
        )
        return _json_error(500, 50000, "内部服务器错误")
