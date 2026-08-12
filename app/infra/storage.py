from typing import Protocol


class ObjectStorage(Protocol):
    async def upload(self, key: str, content: bytes, content_type: str) -> str: ...

    async def create_download_url(self, key: str, expires_seconds: int = 600) -> str: ...
