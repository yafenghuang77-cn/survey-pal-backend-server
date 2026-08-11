from fastapi import FastAPI
from pydantic import BaseModel


class TestResponse(BaseModel):
    message: str


app = FastAPI(
    title="Survey Pal API",
    version="0.1.0",
)


@app.get("/api/v1/test", response_model=TestResponse, tags=["test"])
async def get_test_message() -> TestResponse:
    return TestResponse(message="调研宝后端服务运行正常")
