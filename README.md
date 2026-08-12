# 调研宝后端服务

基于 FastAPI 的模块化单体后端，按照《调研宝后端架构设计方案 v2.2》搭建。

## 🚧 当前状态：框架骨架

当前完成架构实施计划的**阶段一骨架搭建**，仅包含基础设施和测试接口，**不含业务逻辑**：

### 已完成
- ✅ FastAPI 应用工厂、版本路由和统一响应格式
- ✅ 请求 ID、结构化 JSON 日志、全局异常处理和 CORS
- ✅ SQLAlchemy 2.0 Async、PostgreSQL 基础配置和 Alembic 环境
- ✅ 独立 Redis Cache / Celery Broker 配置
- ✅ `/health/live`、`/health/ready` 和 `/metrics` 健康检查
- ✅ 测试响应接口：`/api/v1/test`、`/api/v1/echo`、`/api/v1/list`、`/api/v1/error-demo`
- ✅ Docker Compose 本地基础设施、API 与 Worker 镜像
- ✅ Ruff、mypy、pytest 和 GitHub Actions CI 流水线

### 待实现业务模块(按架构文档后续阶段)
- ⏳ 用户认证与 Token 验证(阶段二)
- ⏳ 问卷 CRUD、答卷提交、版本管理(阶段三)
- ⏳ 异步任务、统计计算、报表生成(阶段四)
- ⏳ 实时聊天 WebSocket、房间与消息(阶段五)
- ⏳ 管理后台与审计日志(阶段六)

## 环境要求

- uv 0.8+
- Docker + Docker Compose（启动 PostgreSQL 和 Redis 时需要）
- Python 3.13（由 uv 根据 `.python-version` 自动管理）

## 本地启动

首次初始化：

```bash
uv sync
cp .env.example .env
docker compose -f deploy/docker-compose.yml up -d postgres redis-cache redis-broker
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

服务启动后：

- OpenAPI 文档：http://localhost:8000/docs
- 测试接口：http://localhost:8000/api/v1/test
- 回显测试：http://localhost:8000/api/v1/echo（POST）
- 分页测试：http://localhost:8000/api/v1/list?page=1&page_size=10
- 错误格式：http://localhost:8000/api/v1/error-demo?code=10001
- 存活检查：http://localhost:8000/health/live
- 就绪检查：http://localhost:8000/health/ready
- Prometheus 指标：http://localhost:8000/metrics

完整容器环境：

```bash
docker compose -f deploy/docker-compose.yml up --build
```

## 开发命令

```bash
# 代码质量
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest

# 数据库迁移
uv run alembic check
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

## 测试接口说明

当前提供的测试接口用于验证统一响应格式和基础设施：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/test` | GET | 基础服务测试 |
| `/api/v1/echo` | POST | 请求体解析与响应 |
| `/api/v1/list` | GET | 分页响应格式 |
| `/api/v1/error-demo` | GET | 错误响应格式(可传 code 参数) |
| `/api/v1/exception-demo` | GET | 全局异常处理器 |
| `/api/v1/version` | GET | 版本信息 |
| `/health/live` | GET | K8s liveness 探针 |
| `/health/ready` | GET | K8s readiness 探针 |
| `/metrics` | GET | Prometheus 指标 |

## 目录说明

```text
app/api/           HTTP 接口入口(当前仅测试接口)
app/core/          配置、日志、异常、响应和中间件
app/models/        SQLAlchemy 数据模型(骨架)
app/schemas/       Pydantic 输入输出契约
app/services/      业务逻辑(待实现)
app/repositories/  数据访问(骨架)
app/infra/         PostgreSQL、Redis、HTTP、存储适配
app/tasks/         Celery Worker(骨架)
app/events/        Outbox 领域事件(骨架)
app/websocket/     实时连接与广播(骨架)
alembic/           数据库迁移
deploy/            Docker 与部署配置
tests/             自动化测试
```

架构依据见 [调研宝后端架构设计方案 v2.2](./docs/调研宝后端架构设计方案_v2.1.md)。
