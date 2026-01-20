---
description: AuraMax 前端 UX/UI 现代化升级与 B2G 监管端设计规划
---

# AuraMax UX/UI Modernization & B2G Design Workflow

本工作流旨在解决当前系统“视觉割裂”的问题，统一设计语言，提升 Landing Page 的科技感，并为 B2G 监管端制定详细的界面交互规范。

## 🎨 Phase 1: 统一设计系统 (Design System Unification)

目标：在 `globals.css` 中建立一套支持 B2B、B2C、B2G 三种业务形态的 Design Tokens。

### 1.1 核心色板定义 (Color Palette)
在 `:root` 中定义语义化变量，而非硬编码颜色值。

*   **Primary Brand (AuraBlue)**: 用于 Landing Page 和通用 CTA。
    *   `--color-brand-500`: `#3B82F6` (Royal Blue)
*   **B2B Context (Pharma Dark)**: 强调沉浸感与高密度数据。
    *   `--color-b2b-bg`: `#09090B` (Zinc 950)
    *   `--color-b2b-surface`: `#18181B` (Zinc 900)
    *   `--color-b2b-accent`: `#F97316` (Orange 500 - for data highlights)
*   **B2C Context (Patient Light)**: 强调清晰与信任。
    *   `--color-b2c-bg`: `#FFFFFF`
    *   `--color-b2c-surface`: `#F8FAFC` (Slate 50)
    *   `--color-b2c-primary`: `#0EA5E9` (Sky 500 - calming)
*   **B2G Context (Regulator Audit)**: 强调对比度与状态指示。
    *   `--color-b2g-bg`: `#F8FAFC` (Slate 50)
    *   `--color-b2g-header`: `#1E293B` (Slate 800 - 严谨感)
    *   `--color-status-pass`: `#10B981` (Emerald 500)
    *   `--color-status-fail`: `#EF4444` (Red 500)
    *   `--color-status-warn`: `#F59E0B` (Amber 500)

### 1.2 排版系统 (Typography)
*   字体统一为 `Inter` (默认) 或 `Plus Jakarta Sans` (标题)。
*   定义 `.text-audit-mono` 用于 B2G 的哈希值和 ID 显示 (使用 `JetBrains Mono` 或系统等宽字体)。

---

## 🚀 Phase 2: Landing Page 动效升级 (Motion Injection)

目标：使用 `framer-motion` 让首页“活”起来，体现 AI 运算能力。

### 2.1 Hero Section 编排
*   **文字渐显**: 标题 "Decode your biological age" 采用 `staggerChildren` 逐行上浮淡入。
*   **背景氛围**: 添加一个低透明度的 Canvas 或 SVG 动画背景（如缓慢旋转的抽象 DNA 螺旋或流动的数据粒子），置于文字下方 `z-index: -1`。
*   **CTA 呼吸感**: "Start for free" 按钮添加微弱的 `scale` 呼吸动画，吸引点击。

### 2.2 数据可视化动态化
*   **Stats Counter**: "40+ Biomarkers" 等数字不应静态显示，而应从 0 开始 `countUp` 滚动到最终值。
*   **Feature Cards**: 当用户滚动到 "How it works" 区域时，卡片依次滑入 (`WhileInView`)。

---

## 🏛️ Phase 3: B2G 监管端界面线框图 (B2G Wireframe Specs)

目标：为政府监管部门（FDA/NMPA 模拟）设计一套高可信、可审计的监控界面。

### 3.1 布局架构 (Layout Structure)
采用 **"L-Shape"** 布局，强调导航效率。

*   **Left Sidebar (Dark Navy `#1E293B`)**:
    *   **Logo Area**: "AuraMax Oversight" (白色无衬线字体)。
    *   **Navigation**:
        *   📊 **Dashboard** (态势感知)
        *   🏥 **Active Trials** (进行中的试验)
        *   ⚠️ **Adverse Events** (不良反应 - 红色角标显示未读数)
        *   🔍 **Data Audit** (数据审计日志)
        *   📜 **Reports** (合规报告)
*   **Top Header (White `#FFFFFF`)**:
    *   **Global Filter**: "Region: National", "Therapeutic Area: Oncology".
    *   **Notification Bell**: 仅提示高风险违规。
    *   **User Profile**: "Log out" (带有 Session Timer 倒计时，强调安全性)。

### 3.2 核心视图：态势感知仪表盘 (Dashboard View)
**设计风格**: High Contrast, Audit Clean.

#### A. 顶部关键指标卡 (KPI Cards)
一排 4 个卡片，用于快速扫描状态：
1.  **Trials Monitored**: 数字 (e.g., "12") | 趋势 (Flat)。
2.  **Safety Signals**: 数字 (e.g., "3" - **红色高亮**) | 描述: "Requires immediate review"。
3.  **Data Integrity Score**: 数字 (e.g., "99.8%") | 进度条 (绿色)。
4.  **Pending Approvals**: 数字 (e.g., "5").

#### B. 主视图：区域合规热力图 (Regional Compliance Map)
*   **组件**: 一个交互式地图。
*   **视觉**: ALert 区域显示为只有红色/橙色脉冲点的地图（深色或灰色底图）。
*   **交互**: 悬停在某个红点（某医院/研究中心）上，显示 Tooltip:
    *   "Center ID: 8832"
    *   "Protocol Deviations: 15% (> Threshold 5%)"
    *   "Action: **Initiate Audit** (Button)"

#### C. 底部面板：实时审计流 (Live Audit Stream)
*   **标题**: "Recent Data Commit Log"
*   **列表样式**: 等宽字体，紧凑行高。
*   **内容**:
    *   `[10:42:01] UPDATE Cohort_882 safety_data (Hash: 8a7f...2d) by User_Pharma_01`
    *   `[10:41:55] CREATE Adverse_Event #9921 (Grade 3) by Investigator_Smith`
*   **功能**: 点击任意一行，右侧滑出 Drawer，显示该操作的完整 JSON Diff 和区块链存证哈希。

### 3.3 交互细节：红色警报处理 (Red Flag Workflow)
1.  用户点击顶部 "Safety Signals" 卡片。
2.  界面跳转至 "Adverse Events" 列表，自动过滤出 "Grade 3-4" 且 "Unresolved" 的条目。
3.  选中某条目，进入详情页。
4.  **详情页特征**:
    *   左侧：患者临床数据时间轴。
    *   右侧：AI 分析建议 ("Potential correlation with study drug: High").
    *   底部：操作栏 "Request More Info", "Freeze Trial Enrollment" (危险操作，需二次确认).

---

## 📝 Execution Plan

// turbo
1. 更新 `globals.css` 定义 Phase 1 的变量。
// turbo
2. 安装 `framer-motion` (如尚未安装)。
3. 重构 `src/app/page.tsx` 实现 Phase 2 的动效。
4. 创建 `src/app/gov/layout.tsx` 和 `src/app/gov/dashboard/page.tsx` 实现 Phase 3 的 B2G 原型。
