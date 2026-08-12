from httpx import AsyncClient


async def test_live_health(client: AsyncClient) -> None:
    response = await client.get("/health/live", headers={"X-Request-ID": "req_test"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req_test"
    assert response.json()["code"] == 0
    assert response.json()["data"] == {"status": "ok"}


async def test_api_response_contract(client: AsyncClient) -> None:
    response = await client.get("/api/v1/test")
    body = response.json()

    assert response.status_code == 200
    assert body["code"] == 0
    assert body["message"] == "success"
    assert body["data"]["message"] == "调研宝后端服务运行正常"
    assert body["request_id"].startswith("req_")
    assert isinstance(body["timestamp"], int)


async def test_not_found_uses_error_contract(client: AsyncClient) -> None:
    response = await client.get("/missing")
    body = response.json()

    assert response.status_code == 404
    assert body["code"] == 10004
    assert body["data"] is None
