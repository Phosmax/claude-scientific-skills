---
description: AuraMax 核心功能开发工作流 - 从 Bio-Age 到 GRADE 证据分级的完整开发流程
---

# AuraMax 核心功能开发工作流

本工作流涵盖 AuraMax 平台的核心功能开发，基于 `scientific-skills` 项目的最佳实践。

## 前置条件

// turbo
1. 启动后端服务：
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-core && source .venv/bin/activate && nohup python -m uvicorn auramax_api.main:app --host 0.0.0.0 --port 8000 > /tmp/auramax_backend.log 2>&1 &
```

// turbo
2. 启动前端服务：
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-web && nohup npm run dev > /tmp/auramax_frontend.log 2>&1 &
```

// turbo
3. 验证服务状态：
```bash
sleep 3 && lsof -i :3000 -i :8000 | grep LISTEN
```

---

## Phase 1: GRADE 证据分级系统

### 1.1 后端 - 添加证据分级到 AI 解读

修改文件: `auramax_api/routers/workflow.py`

添加 GRADE 分级逻辑到 lab_interpret workflow:
- 1A: 强推荐，高质量证据 (随机对照试验)
- 1B: 强推荐，中等质量证据
- 2A: 弱推荐，高质量证据
- 2B: 弱推荐，中等质量证据
- 2C: 弱推荐，低质量证据

### 1.2 前端 - 显示证据等级徽章

创建组件: `src/components/ui/EvidenceBadge.tsx`

在 AI 建议卡片中显示证据等级标签，不同等级使用不同颜色：
- 1A/1B: 绿色 (高可信度)
- 2A/2B: 黄色 (中等可信度)
- 2C: 灰色 (低可信度)

---

## Phase 2: SMART 健康目标模块

### 2.1 后端 - 健康目标 API

创建文件: `auramax_api/routers/goals.py`

API 端点:
- `POST /api/v1/goals/` - 创建健康目标
- `GET /api/v1/goals/` - 获取用户目标列表
- `PATCH /api/v1/goals/{id}` - 更新目标进度
- `DELETE /api/v1/goals/{id}` - 删除目标

### 2.2 前端 - 目标卡片组件

创建组件: `src/components/goals/GoalCard.tsx`

SMART 目标字段:
- Specific: 具体目标描述
- Measurable: 可测量指标 (如 HbA1c < 7%)
- Achievable: 可达成性评估
- Relevant: 与健康优先级的关联
- Time-bound: 截止日期

---

## Phase 3: 生物标志物趋势分析

### 3.1 后端 - 多报告比较 API

修改文件: `auramax_api/routers/clinic.py`

添加端点: `GET /api/v1/clinic/patients/{id}/biomarker-trends`

返回:
- 时间序列数据
- 变化趋势 (上升/下降/稳定)
- 风险分层 (低/中/高)

### 3.2 前端 - 趋势图表

创建组件: `src/components/charts/BiomarkerTrend.tsx`

使用 Recharts 或原生 SVG 绘制趋势线图。

---

## Phase 4: HIPAA Safe Harbor 脱敏

### 4.1 后端 - PII 检测服务

修改文件: `auramax_ingest/redactor.py`

确保检测并替换 18 项 HIPAA 标识符：
- 姓名、地址、日期、电话、Email
- 社会安全号、病历号、保险号
- 等...

### 4.2 集成到 PDF 解析流程

在 PDF 解析后、存储前自动调用脱敏服务。

---

## 验证步骤

// turbo
4. 运行后端测试：
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-core && source .venv/bin/activate && python -m pytest tests/ -v --tb=short -x
```

5. 手动测试 Dashboard:
- 访问 http://localhost:3000/dashboard
- 验证 Bio-Age 显示正常
- 验证 AI 建议带有证据等级
- 验证多语言切换正常

---

## 回滚计划

如果出现问题，可以使用 Git 回滚：
```bash
git checkout -- <file>
```

或者恢复到最近的稳定提交：
```bash
git log --oneline -5
git checkout <commit-hash>
```
