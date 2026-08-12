from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings

engine: AsyncEngine | None = None
session_factory: async_sessionmaker[AsyncSession] | None = None


def initialize_database(settings: Settings) -> None:
    global engine, session_factory
    engine = create_async_engine(
        settings.database_url.get_secret_value(),
        pool_pre_ping=True,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_timeout=settings.database_pool_timeout_seconds,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def close_database() -> None:
    global engine, session_factory
    if engine is not None:
        await engine.dispose()
    engine = None
    session_factory = None


async def get_db_session() -> AsyncIterator[AsyncSession]:
    if session_factory is None:
        raise RuntimeError("Database has not been initialized")
    async with session_factory() as session:
        yield session


async def check_database() -> None:
    if engine is None:
        raise RuntimeError("Database has not been initialized")
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
