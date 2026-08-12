import pytest

from app.core.config import Settings
from app.main import create_app


def test_comma_separated_cors_origins() -> None:
    settings = Settings(cors_origins="http://localhost:3000,http://localhost:5173")
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost:5173"]


def test_default_secret_is_rejected_in_production() -> None:
    settings = Settings(environment="production")
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        create_app(settings)
