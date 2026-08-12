from redis.asyncio import Redis

from app.core.config import Settings

redis_cache: Redis | None = None


def initialize_redis_cache(settings: Settings) -> None:
    global redis_cache
    redis_cache = Redis.from_url(
        settings.redis_cache_url.get_secret_value(),
        encoding="utf-8",
        decode_responses=True,
        socket_connect_timeout=settings.redis_socket_timeout_seconds,
        socket_timeout=settings.redis_socket_timeout_seconds,
    )


async def close_redis_cache() -> None:
    global redis_cache
    if redis_cache is not None:
        await redis_cache.aclose()
    redis_cache = None


def get_redis_cache() -> Redis:
    if redis_cache is None:
        raise RuntimeError("Redis cache has not been initialized")
    return redis_cache


async def check_redis_cache() -> None:
    await get_redis_cache().ping()
