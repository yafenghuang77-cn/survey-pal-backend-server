from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.response import ApiResponse, error, paginated, success

router = APIRouter(tags=["system"])


class EchoRequest(BaseModel):
    message: str = Field(..., description="要回显的消息")


class EchoResponse(BaseModel):
    echo: str
    length: int


class ListItem(BaseModel):
    id: int
    name: str


@router.get("/test", response_model=ApiResponse[dict[str, str]])
async def test_service() -> dict[str, Any]:
    """基础测试接口 - 验证服务运行"""
    return success({"message": "调研宝后端服务运行正常", "status": "healthy"})


@router.post("/echo", response_model=ApiResponse[EchoResponse])
async def echo(body: EchoRequest) -> dict[str, Any]:
    """回显接口 - 测试请求体解析和响应格式"""
    return success(EchoResponse(echo=body.message, length=len(body.message)))


@router.get("/error-demo", response_model=ApiResponse[None])
async def error_demo(code: int = 10001) -> dict[str, Any]:
    """错误响应演示 - 测试统一错误格式"""
    error_messages = {
        10001: "参数校验失败",
        11001: "未登录",
        11002: "Token 过期",
        50000: "内部服务器错误",
    }
    message = error_messages.get(code, "未知错误")
    return error(code, message, details={"demo": True})


@router.get("/exception-demo")
async def exception_demo() -> None:
    """异常演示 - 测试全局异常处理器"""
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="这是一个测试异常")


@router.get("/list", response_model=ApiResponse[dict[str, Any]])
async def list_demo(page: int = 1, page_size: int = 10) -> dict[str, Any]:
    """分页列表演示 - 测试分页响应格式"""
    # 模拟数据
    total = 45
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    items = [ListItem(id=i, name=f"Item {i}") for i in range(start + 1, end + 1)]

    return paginated([item.model_dump() for item in items], page, page_size, total)


@router.get("/version", response_model=ApiResponse[dict[str, str]])
async def version_info() -> dict[str, Any]:
    """版本信息"""
    return success(
        {
            "app": "survey-pal-backend",
            "version": "0.1.0",
            "python": "3.13",
            "framework": "FastAPI 0.141+",
        }
    )
