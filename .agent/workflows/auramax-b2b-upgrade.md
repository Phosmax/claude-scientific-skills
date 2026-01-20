---
description: AuraMax B2B 战略升级执行计划 - 从 C 端玩具到 B 端利器
---

# AuraMax B2B 战略升级计划 (Operation: B2B Pivot)

**目标**: 填补当前系统与 `AURAMAX_COMMERCIAL_REPORT.md` 中承诺的 B2B 功能（队列分析、证据合成）之间的巨大鸿沟，确保 Week 11 的 Pilot 预热具备实质性的演示能力。

## 阶段一：队列分析引擎 (Cohort Analysis Engine)
*目标: 实现医药行业核心的生存分析能力，摆脱单纯的“体检报告”定位。*

1.  **数据模型构建** (Priority: P0)
    *   新增 `Cohort` 模型：定义患者群组（筛选条件）。
    *   新增 `SurvivalAnalysis` 模型：存储 KM 曲线分析结果。
    *   *Audit*: 确保模型关系正确，索引优化。

2.  **队列筛选服务** (Priority: P0)
    *   实现 `CohortService.filter_patients()`：支持基于年龄、基因型、病史的复杂 SQL 构建。
    *   *Audit*: 检查 SQL 注入风险和查询性能。

3.  **生存分析计算** (Priority: P1)
    *   集成 Python `lifelines` 库。
    *   实现 `calculate_km_curve(cohort_a, cohort_b)`。
    *   *Audit*: 验证数学计算准确性（与标准数据对比）。

4.  **API 暴露** (Priority: P1)
    *   `/api/v1/cohorts` 端点：创建、管理队列。
    *   `/api/v1/analysis/survival` 端点：运行分析。
    *   *Audit*: 检查权限控制（RBAC），确保只有 Pro/Enterprise 用户可用。

## 阶段二：证据合成模块 (Evidence Synthesis)
*目标: 实现“去黑盒化”承诺，提供 Scientific Grounding。*

1.  **文献索引** (Priority: P2)
    *   创建 `Evidence` 模型。
    *   实现简单的 PubMed 模拟接口（Phase 3 再接真实 API）。

2.  **RAG 管道** (Priority: P2)
    *   在 `ReportingService` 中集成证据查找。
    *   为每条建议附加 `[Citation]`。

## 执行工作流 (Loop)

对于上述每个步骤，执行以下循环：
1.  **Implement**: 编写/修改代码。
2.  **Roast (Audit)**: 使用 `code-roaster` 技能进行毒舌审计。
3.  **Refine**: 根据审计修复问题。
4.  **Verify**: 确认无误后进入下一步。
