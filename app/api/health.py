import asyncio
from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from app.core.response import ApiResponse, success
from app.infra.db import check_database
from app.infra.redis_cache import check_redis_cache

router = APIRouter(prefix="/health", tags=["health"])


class LiveStatus(BaseModel):
    status: Literal["ok"] = "ok"


class DependencyStatus(BaseModel):
    status: Literal["ok", "unavailable"]
    database: Literal["ok", "unavailable"]
    redis_cache: Literal["ok", "unavailable"]


@router.get("/live", response_model=ApiResponse[LiveStatus])
async def live() -> ApiResponse[LiveStatus]:
    return success(LiveStatus())


async def _dependency_status() -> DependencyStatus:
    database_result, redis_result = await asyncio.gather(
        check_database(),
        check_redis_cache(),
        return_exceptions=True,
    )
    database = "unavailable" if isinstance(database_result, BaseException) else "ok"
    redis_cache = "unavailable" if isinstance(redis_result, BaseException) else "ok"
    overall = "ok" if database == redis_cache == "ok" else "unavailable"
    return DependencyStatus(status=overall, database=database, redis_cache=redis_cache)


@router.get("/ready", response_model=ApiResponse[DependencyStatus])
async def ready(response: Response) -> ApiResponse[DependencyStatus]:
    dependency_status = await _dependency_status()
    if dependency_status.status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return success(dependency_status)
