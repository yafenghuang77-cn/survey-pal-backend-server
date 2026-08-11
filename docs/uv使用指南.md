# uv 使用指南

## 什么是 uv

uv 是一个极速的 Python 包管理工具，比 pip 快 10-100 倍，功能类似于 npm、pnpm 或 cargo。

## 虚拟环境管理

### 自动创建虚拟环境

uv 会在首次运行时自动创建 `.venv` 目录：

```bash
# 任意一条命令都会触发创建
uv sync           # 推荐：同步 pyproject.toml 中的依赖
uv run python     # 运行 Python
uv add requests   # 添加依赖
```

### 手动管理虚拟环境

```bash
# 创建虚拟环境
uv venv

# 创建时指定 Python 版本
uv venv --python 3.13

# 删除虚拟环境
rm -rf .venv

# 重新创建
uv venv && uv sync
```

### 虚拟环境位置

uv 默认在项目根目录创建 `.venv`，结构如下：

```text
.venv/
├── bin/              # 可执行文件
│   ├── python       # Python 解释器
│   ├── pip          # pip (如果安装)
│   └── uvicorn      # 项目依赖的命令
├── lib/             # Python 库
│   └── python3.13/
│       └── site-packages/
└── pyvenv.cfg       # 虚拟环境配置
```

---

## Python 版本管理

### 指定 Python 版本

uv 通过 `.python-version` 文件锁定 Python 版本：

```bash
# 查看当前版本
cat .python-version
# 输出: 3.13

# 更改版本
echo "3.12" > .python-version

# 重新创建虚拟环境
rm -rf .venv
uv sync
```

### uv 自动管理 Python

uv 会自动下载和管理 Python 版本：

```bash
# 查看 uv 管理的 Python 版本
ls ~/.local/share/uv/python/

# uv 会在需要时自动下载指定版本
# 不需要手动安装 Python
```

---

## 依赖管理

### 安装依赖

```bash
# 同步 pyproject.toml 中的所有依赖
uv sync

# 只安装生产依赖（不包括开发依赖）
uv sync --no-dev

# 强制重新安装
uv sync --reinstall
```

### 添加依赖

```bash
# 添加生产依赖
uv add fastapi

# 添加开发依赖
uv add --dev pytest ruff mypy

# 添加可选依赖
uv add --optional redis

# 添加并指定版本
uv add "fastapi>=0.141.1"
```

### 移除依赖

```bash
# 移除依赖
uv remove requests

# 移除开发依赖
uv remove --dev pytest
```

### 更新依赖

```bash
# 更新所有依赖
uv sync --upgrade

# 更新特定依赖
uv add fastapi --upgrade

# 查看过期的依赖
uv pip list --outdated
```

---

## 运行命令

### 基本用法

```bash
# 在虚拟环境中运行命令
uv run python main.py
uv run uvicorn main:app --reload
uv run pytest

# uv run 会自动：
# 1. 创建虚拟环境（如果不存在）
# 2. 安装依赖（如果需要）
# 3. 在虚拟环境中执行命令
```

### 激活虚拟环境（可选）

uv 推荐使用 `uv run`，但你也可以手动激活：

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 激活后可以直接运行命令
python main.py
uvicorn main:app --reload

# 退出虚拟环境
deactivate
```

---

## 锁文件管理

### uv.lock 文件

`uv.lock` 是依赖锁定文件，记录了所有依赖的精确版本：

```bash
# 更新锁文件
uv lock

# 更新并升级依赖
uv lock --upgrade

# 查看锁文件内容
cat uv.lock
```

### 生产部署

```bash
# 仅安装锁文件中的版本（不解析新版本）
uv sync --frozen

# 验证锁文件是否最新
uv lock --check
```

---

## 查看信息

### 查看已安装的包

```bash
# 列出所有包
uv pip list

# 显示包详情
uv pip show fastapi

# 查看依赖树
uv pip tree
```

### 查看项目信息

```bash
# 查看项目配置
cat pyproject.toml

# 查看虚拟环境配置
cat .venv/pyvenv.cfg

# 查看 uv 版本
uv --version
```

---

## 常见任务

### 清理和重置

```bash
# 删除虚拟环境
rm -rf .venv

# 重新安装所有依赖
uv sync

# 清理缓存
uv cache clean
```

### 导出依赖

```bash
# 导出为 requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# 包含开发依赖
uv pip compile pyproject.toml --extra dev -o requirements-dev.txt
```

### 从其他工具迁移

```bash
# 从 requirements.txt 导入
uv add -r requirements.txt

# 从 poetry 迁移（pyproject.toml 已存在）
uv sync

# 从 pipenv 迁移（先生成 requirements.txt）
pipenv requirements > requirements.txt
uv add -r requirements.txt
```

---

## uv 配置

### 项目配置（pyproject.toml）

```toml
[project]
name = "survey-pal-backend-server"
version = "0.1.0"
requires-python = ">=3.13,<3.14"
dependencies = [
    "fastapi[standard-no-fastapi-cloud-cli]>=0.141.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.8.0",
    "mypy>=1.11.0",
]

[tool.uv]
# uv 特定配置（可选）
```

### 全局配置

```bash
# 查看配置位置
uv config --show

# 设置配置
uv config set index-url https://pypi.org/simple
```

---

## 与其他工具对比

| 操作 | uv | pip | poetry |
| --- | --- | --- | --- |
| 安装依赖 | `uv sync` | `pip install -r requirements.txt` | `poetry install` |
| 添加依赖 | `uv add <pkg>` | `pip install <pkg>` | `poetry add <pkg>` |
| 运行命令 | `uv run <cmd>` | `python <cmd>` | `poetry run <cmd>` |
| 创建虚拟环境 | 自动 | `python -m venv .venv` | 自动 |
| 锁定依赖 | `uv.lock` | `requirements.txt` | `poetry.lock` |

---

## 最佳实践

### 1. 提交版本控制

```bash
# 应该提交
git add pyproject.toml
git add uv.lock
git add .python-version

# 不要提交
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
```

### 2. 团队协作

```bash
# 新成员克隆项目后
git clone <repo>
cd <project>

# 一条命令完成环境搭建
uv sync

# 就可以开始开发了
uv run fastapi dev main.py
```

### 3. CI/CD 环境

```yaml
# GitHub Actions 示例
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync --frozen

- name: Run tests
  run: uv run pytest
```

---

## 故障排查

### 虚拟环境损坏

```bash
rm -rf .venv
uv sync
```

### Python 版本问题

```bash
# 查看期望版本
cat .python-version

# 查看实际版本
uv run python --version

# 重新创建环境
rm -rf .venv
uv venv --python 3.13
uv sync
```

### 依赖冲突

```bash
# 查看冲突详情
uv lock --verbose

# 尝试升级解决
uv sync --upgrade

# 手动解决（修改 pyproject.toml 中的版本约束）
# 然后重新锁定
uv lock
```

---

## 参考资料

- [uv 官方文档](https://docs.astral.sh/uv/)
- [pyproject.toml 规范](https://peps.python.org/pep-0621/)
- [Python 打包指南](https://packaging.python.org/)

---

## 快速参考

```bash
# 项目初始化
uv init                    # 创建新项目
uv sync                    # 安装依赖

# 依赖管理
uv add <pkg>              # 添加依赖
uv add --dev <pkg>        # 添加开发依赖
uv remove <pkg>           # 移除依赖
uv sync --upgrade         # 更新所有依赖

# 运行命令
uv run <command>          # 在虚拟环境中运行
uv run python main.py     # 运行 Python 脚本
uv run pytest             # 运行测试

# 信息查看
uv pip list               # 列出所有包
uv pip show <pkg>         # 查看包详情
uv --version              # 查看 uv 版本

# 虚拟环境
uv venv                   # 创建虚拟环境
rm -rf .venv && uv sync   # 重建虚拟环境

# 锁文件
uv lock                   # 更新锁文件
uv lock --upgrade         # 升级依赖并更新锁文件
uv sync --frozen          # 使用锁定的版本（CI/CD）
```
