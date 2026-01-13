---
description: 核心科学能力回归工作流 - 将 Legacy Skills 移植到 AuraMax 平台
---

# 核心科学能力回归工作流 (Core Skill Regression Workflow)

本工作流指导如何将 `claude-scientific-skills` 中的 legacy skill 标准化为 AuraMax 平台的微服务模块。

## 1. Skill 移植标准流程

### 1.1 依赖分析
首先检查 `legacy-skill/SKILL.md` 和 `requirements.txt`：
1. 确定 Python 依赖 (如 `pandas`, `scipy`)。
2. 将依赖添加到 `auramax-core/pyproject.toml`。
3. 运行 `uv sync` 更新环境。

### 1.2 模块创建
在 `src/` 下创建新的 Python 模块 (如果不存在)：

```bash
mkdir -p src/auramax_[module_name]
touch src/auramax_[module_name]/__init__.py
```

### 1.3 代码重构 (The "Lift & Shift")
将 legacy script 转化为 Python 类/函数：
1. **去除 CLI 参数解析**：将 `argparse` 修改为函数参数。
2. **去除硬编码路径**：使用输入参数传递文件路径。
3. **添加类型提示**：为所有函数添加 Python Type Hints。
4. **添加错误处理**：使用 `try/except` 捕获异常并抛出标准错误。

### 1.4 MCP 工具封装
在 `src/auramax_[module_name]/server.py` 中创建 MCP Tools：

```python
@mcp.tool()
async def analyze_data(file_path: str) -> str:
    """Analyze a data file."""
    # Call the refactored logic
    ...
```

---

## 2. 验证与集成

### 2.1 单元测试
为新模块编写 `pytest` 测试：
```python
# tests/test_[module_name].py
def test_analysis():
    result = analyze_data("test.csv")
    assert "summary" in result
```

// turbo
### 2.2 运行测试
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-core && source .venv/bin/activate && python -m pytest tests/test_analysis.py -v
```

### 2.3 注册到 Orchestrator
修改 `src/auramax_api/mcp_server.py`，将新工具注册到主 Agent。

---

## 3. 部署检查
1. **Docker 构建**：确保新依赖不破坏 Docker 构建。
2. **环境变量**：检查是否需要新的 API Key (如 PubMed API Key)。
