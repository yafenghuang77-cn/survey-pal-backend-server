from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.infra.db import get_db_session
from app.infra.redis_cache import get_redis_cache

SettingsDep = Annotated[Settings, Depends(get_settings)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
RedisCacheDep = Annotated[Redis, Depends(get_redis_cache)]
