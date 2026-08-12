from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from app.api.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.infra.db import close_database, initialize_database
from app.infra.redis_cache import close_redis_cache, initialize_redis_cache


def validate_settings(settings: Settings) -> None:
    if (
        settings.environment == "production"
        and settings.jwt_secret_key.get_secret_value() == "change-me-before-production"
    ):
        raise RuntimeError("JWT_SECRET_KEY must be changed in production")


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    validate_settings(app_settings)
    configure_logging(app_settings.log_level)

    if app_settings.sentry_dsn:
        sentry_sdk.init(
            dsn=app_settings.sentry_dsn,
            environment=app_settings.environment,
            traces_sample_rate=0.1,
        )

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        initialize_database(app_settings)
        initialize_redis_cache(app_settings)
        try:
            yield
        finally:
            await close_redis_cache()
            await close_database()

    application = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        debug=app_settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if app_settings.environment != "production" else None,
        redoc_url="/redoc" if app_settings.environment != "production" else None,
    )
    application.add_middleware(RequestContextMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "X-Request-ID"],
    )
    register_exception_handlers(application)
    application.include_router(health_router)
    application.include_router(api_router, prefix=app_settings.api_v1_prefix)

    @application.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return application


app = create_app()
