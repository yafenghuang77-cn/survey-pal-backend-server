from collections.abc import AsyncIterator

import httpx


async def get_http_client() -> AsyncIterator[httpx.AsyncClient]:
    timeout = httpx.Timeout(10.0, connect=3.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        yield client
