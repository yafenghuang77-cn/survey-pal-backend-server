from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        environment="test",
        database_url="postgresql+asyncpg://test:test@localhost:5432/test",
        redis_cache_url="redis://localhost:6379/15",
        redis_broker_url="redis://localhost:6380/15",
        jwt_secret_key="test-secret-not-for-production",
    )


@pytest.fixture
async def client(test_settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(test_settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
