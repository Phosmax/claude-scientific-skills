# AuraMax B2B 分析：端到端演示指南

## 1. 场景 (Scenario)
**用户画像**: 医药公司的高级医学研究员。
**目标**: 利用真实世界证据 (RWE) 验证 *吉非替尼 (Gefitinib)* 在 EGFR+ 非小细胞肺癌 (NSCLC) 患者队列中的疗效。

## 2. 演示旅程 (Dashboard Flow)

### 第一阶段：队列选择 (Phase 1: Cohort Selection)
*   **动作**: 用户登录 `/professional/analytics` 页面。
*   **UI 交互**: 从队列下拉菜单中选择 "NSCLC (EGFR+)"。
*   **系统行为**:
    *   前端调用 `POST /api/v1/analytics/cohorts`，基于条件 `{"condition": "NSCLC", "mutation": "EGFR"}` 定义虚拟队列。
    *   后端（演示模式下模拟）生成约 1200 名患者的合成队列。

### 第二阶段：生存分析 (Phase 2: Survival Analysis - Real-Time Calculation)
*   **动作**: 仪表盘自动加载生存曲线。
*   **UI 交互**: 用户观察到两条曲线："Experimental (Gefitinib)"（实验组）与 "Standard Care"（标准护理组）。
*   **系统行为**:
    *   前端调用 `POST /api/v1/analytics/survival`。
    *   **后端引擎**:
        *   检索患者数据。
        *   使用 `lifelines` 逻辑（在 `SurvivalEngine` 中模拟）计算 Kaplan-Meier 概率。
        *   计算 Log-Rank 检验 (P-Value < 0.001)。
    *   **结果**: "Experimental" 曲线显示出更高的生存概率，并在第 2 个月开始肉眼可见地分离。

### 第三阶段：证据综合 (Phase 3: Evidence Synthesis - Hybrid RAG)
*   **动作**: 用户注意到曲线分离，并在证据搜索栏中输入 "Gefitinib efficacy EGFR"。
*   **系统行为**:
    *   前端调用 `GET /api/v1/analytics/evidence?q=Gefitinib...`。
    *   **RAG 引擎**:
        *   **召回 (Recall)**: SQL 查询查找包含 "Gefitinib" 和 "EGFR" 的文章。
        *   **重排序 (Re-rank)**: 语义评分器提升 "High Confidence"（高置信度）指南（如《新英格兰医学杂志》）的排名。
    *   **展示**: 仪表盘显示带有 "HIGH Confidence" 徽章的 *Live RAG* 结果。

## 3. 技术验证 (Technical Verification)
为了证明系统运行的是"真实科学"，执行以下检查：

1.  **分子有效性**: 系统现在强制依赖 RDKit。任何验证分子 `COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1` (Gefitinib) 的尝试都将通过严格的 `MolecularDescriptorCalculator` 计算。
2.  **优雅降级**: 断开后端连接。仪表盘会显示 "Demo Mode"（演示模式）徽章，但仍使用高保真模拟数据保持交互性。
