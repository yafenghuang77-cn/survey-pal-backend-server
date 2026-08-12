from time import time
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from app.core.context import get_request_id

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None
    request_id: str
    timestamp: int


class ErrorResponse(ApiResponse[None]):
    details: dict[str, Any] | list[Any] | None = None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool
    next_cursor: str | None = None


class PageResult(BaseModel, Generic[T]):
    items: list[T]
    pagination: Pagination


def now_milliseconds() -> int:
    return int(time() * 1000)


def success[T](data: T | None = None, message: str = "success") -> ApiResponse[T]:
    return ApiResponse(
        code=0,
        message=message,
        data=data,
        request_id=get_request_id(),
        timestamp=now_milliseconds(),
    )


def error(
    code: int,
    message: str,
    details: dict[str, Any] | list[Any] | None = None,
) -> ErrorResponse:
    return ErrorResponse(
        code=code,
        message=message,
        data=None,
        request_id=get_request_id(),
        timestamp=now_milliseconds(),
        details=details,
    )


def paginated[T](items: list[T], page: int, page_size: int, total: int) -> ApiResponse[PageResult[T]]:
    total_pages = (total + page_size - 1) // page_size if total else 0
    result = PageResult(
        items=items,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        ),
    )
    return success(result)
