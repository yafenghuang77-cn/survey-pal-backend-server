# 调研宝后端服务

Survey Pal Backend Server - 基于 FastAPI 的问卷调研系统后端 API

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-green.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-0.7.6+-orange.svg)](https://docs.astral.sh/uv/)

## 快速开始

```bash
# 安装依赖
uv sync

# 启动开发服务器
uv run fastapi dev main.py
```

访问 http://localhost:8000/docs 查看 API 文档

## 文档

- [快速开始指南](./docs/快速开始.md) - 详细的安装、配置和使用说明
- [架构设计方案](./docs/调研宝后端架构设计方案.md) - 技术架构和实施计划

## 核心功能 (规划)

- 用户认证和会话管理
- 问卷创建、编辑、发布和版本管理
- 问卷填写和答题提交
- 数据统计和报表生成
- 调研房间和实时聊天
- 管理后台和审计日志

## 技术栈

- **Web 框架**: FastAPI 0.141.1
- **数据库**: PostgreSQL 16+ (计划)
- **缓存**: Redis 7+ (计划)
- **异步任务**: Celery (计划)
- **包管理**: uv
- **Python**: 3.13

## 项目状态

🚧 当前处于**开发阶段**，正在搭建基础骨架

## 开发

```bash
# 运行测试 (计划)
uv run pytest

# 代码检查 (计划)
uv run ruff check .

# 格式化代码 (计划)
uv run ruff format .
```

## License

MIT