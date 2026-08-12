from app.core.config import Settings


def get_broker_url(settings: Settings) -> str:
    """Keep broker configuration separate from the cache client by design."""
    return settings.redis_broker_url.get_secret_value()
