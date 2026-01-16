# AuraMax 项目上下文

## 项目概述

AuraMax是一个医疗健康科技平台，提供生物年龄分析、电子病历管理、分子分析等功能的SaaS平台。

## 用户等级体系

| 等级 | 标识 | 功能权限 | 目标用户 |
|------|------|---------|---------|
| **Visitor** | 访客 | 首页浏览、功能了解 | 潜在用户 |
| **Free** | 免费版 | 3份报告/月、基础分析 | 个人用户 |
| **Pro** | 专业版 | 无限分析、AI洞察、趋势追踪 | 健康爱好者 |
| **Clinic** | 诊所版 | 团队协作、患者管理(10人) | 小型诊所 |
| **Enterprise** | 企业版 | 无限用户、API访问、审计日志 | 大型机构 |

## 角色设计

### 核心用户角色

1. **诊所管理员 (Clinic Admin)**
   - 管理团队成员
   - 配置诊所信息
   - 查看使用统计
   - 导出合规报告

2. **主治医生 (Physician)**
   - 患者病历管理
   - 报告上传与分析
   - 生物年龄评估
   - 健康目标追踪

3. **免费用户 (Free User)**
   - 基础功能体验
   - 付费转化漏斗
   - 引导升级

4. **Pro专业用户 (Pro User)**
   - 深度数据分析
   - AI洞察
   - 自定义健康目标

5. **Clinic诊所用户 (Clinic User)**
   - 团队协作
   - 患者共享
   - 批量操作

6. **企业用户 (Enterprise User)**
   - API访问
   - 审计日志
   - SSO集成

## 技术栈

- **前端**: Next.js 15, React 18, TypeScript
- **UI**: Tailwind CSS, shadcn/ui
- **状态管理**: Zustand
- **国际化**: next-intl
- **测试**: Vitest
- **图表**: Recharts

## 功能权限矩阵

| 功能 | Free | Pro | Clinic | Enterprise |
|------|------|-----|--------|------------|
| 报告分析 | 3份/月 | 无限 | 无限 | 无限 |
| AI洞察 | ❌ | ✅ | ✅ | ✅ |
| 趋势分析 | ❌ | ✅ | ✅ | ✅ |
| 患者管理 | 1人 | 5人 | 无限 | 无限 |
| 团队成员 | 1人 | 1人 | 10人 | 无限 |
| API访问 | ❌ | ❌ | ❌ | ✅ |
| 审计日志 | ❌ | ❌ | ❌ | ✅ |

## 核心文件结构

```
auramax-web/
├── src/
│   ├── app/
│   │   ├── dashboard/       # 用户仪表盘
│   │   ├── admin/           # 管理后台
│   │   │   └── dashboard/   # 管理员仪表盘
│   │   └── professional/    # 专业版功能
│   ├── components/
│   │   ├── auth/            # 认证相关
│   │   │   └── PermissionGuard.tsx  # 权限守卫
│   │   ├── ui/              # 基础UI组件
│   │   ├── paywall/         # 付费墙组件
│   │   └── charts/          # 图表组件
│   ├── lib/
│   │   ├── api.ts           # API客户端
│   │   ├── permissions.ts   # 权限管理
│   │   └── auth.ts          # 认证状态
│   ├── stores/
│   │   └── auth.ts          # 认证Store
│   └── test/                # 测试文件
├── docs/
│   └── USER_ROLES_AUDIT_PLAN.md  # 用户角色审计计划
└── package.json
```

## 最近的优化

### 1. 前端优化 (2025-01-13)
- Toast通知系统替换所有alert
- ErrorBoundary错误边界组件
- 移动端响应式导航
- ARIA无障碍标签
- Vitest单元测试框架 (39个测试100%通过)

### 2. 权限系统
- 权限管理模块 (`permissions.ts`)
- 权限守卫组件 (`PermissionGuard.tsx`)
- 付费墙组件
- 路由守卫

### 3. 管理员界面
- 管理员仪表盘页面 (`/admin/dashboard`)
- 团队管理面板 (团队成员CRUD操作)
- 患者管理（患者CRUD、CSV导入导出）
- 数据分析面板
- 系统设置 (NVIDIA NIM API配置)

## 管理员仪表盘完整功能

### 5标签页结构 (已更新 2025-01-14)
```
/admin/dashboard
├── 概览 (Overview)       - 系统统计卡片、团队状态、最近活动
├── 团队管理 (Team)       - 成员CRUD、状态管理、角色分配
├── 患者管理 (Patients)   - 患者CRUD、CSV导入导出
├── 数据分析 (Analytics)  - 报告统计、活跃患者分析
└── 系统设置 (Settings)   - 已移除，移至独立页面
```

**重要变更**:
- ✅ 移除了"系统设置"tab（之前容易造成困惑）
- ✅ 仪表盘专注于日常运营（团队、患者、数据）
- ✅ 系统配置功能移至统一管理控制台主页

---

### 管理控制台统一入口 (新增 2025-01-14)

**路径**: `/admin` (新建统一主页)

**Oracle 战略分析结果**:
- **根本问题**: 不是功能缺失，是导航结构和信息架构混乱
- **用户反馈**: "系统配置完全不满足管理员要求"
- **真实原因**: 两个"设置"入口，功能重叠，管理员无法找到功能

**统一主页功能**:
```
/admin (统一管理控制台主页)
├── 欢迎标题和用户信息
├── 快速操作面板 (4个常用功能)
│   ├── 查看系统概览
│   ├── 管理团队成员
│   ├── 查看审计日志
│   └── 系统设置
├── 4大功能分类卡片
│   ├── 核心管理 (仪表盘、系统设置)
│   ├── 用户与团队 (团队管理、用户管理、患者管理)
│   ├── 数据与分析 (数据分析、文件管理)
│   └── 安全与审计 (审计日志)
└── 系统状态摘要 (系统运行状态、活跃用户、存储使用)
```

**导航路径优化**:
```
之前 (混乱):
  /admin
  ├── /dashboard (5 tabs: 概览/团队/患者/分析/设置) ← "设置"tab 误导!
  └── /settings/system (6 tabs: 概览/诊所/定价/安全/API/系统)
  问题: 两个"设置"入口，功能重复

现在 (清晰):
  /admin (统一主页: 所有功能分类入口)
  ├── 快速操作面板: 一键访问常用功能
  ├── 功能分类卡片: 清晰的功能说明和图标
  └── /dashboard (4 tabs: 概览/团队/患者/分析) ← 专注于日常运营
  └── /settings/system (6 tabs: 概览/诊所/定价/安全/API/系统) ← 完整系统配置
```

**用户体验改进**:
- 🎯 统一入口点（/admin）：新管理员快速上手
- 🎯 清晰的功能分类：功能发现更容易
- 🎯 快速操作面板：常用功能一键访问
- 🎯 详细的功能说明：每个功能卡片都有描述
- 🎯 简化的仪表盘：专注于团队和患者管理

### API端点
- 团队成员: `/admin/team-members`
- 患者管理: `/clinic/patients`
- 审计日志: `/admin/audit-logs`
- 系统配置: `/api/v1/admin/config`

### 权限要求
- 需要 `is_admin = true` 才能访问管理控制台
- 使用 `usePermission` hook 进行权限验证
- 非管理员用户会看到"访问被拒绝"页面

## 开发指南

### 运行测试
```bash
cd auramax-web
npm run test
```

### 添加新功能
1. 在`permissions.ts`中定义功能限制
2. 使用`PaywallGuard`组件包裹功能
3. 在`PermissionGuard`中添加路由守卫

### 添加新角色
1. 在`permissions.ts`中更新`UserRole`类型
2. 更新权限矩阵
3. 创建对应的界面

## 重要配置

### 环境变量
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### API端点
- 基础URL: `http://localhost:8000`
- 认证: `/api/v1/auth/`
- 患者: `/api/v1/clinic/patients`
- 分析: `/api/v1/upload/`
- 目标: `/api/v1/goals/`
- 趋势: `/api/v1/trends/`

## 系统配置完整功能

### 系统配置页面 (`/admin/settings/system`)

**6标签页结构：**
```
/admin/settings/system
├── 概览 (Overview)       - 今日统计、收入概览、快速操作
├── 诊所信息 (Clinic)     - 诊所名称、联系方式、地址、时区
├── 定价配置 (Pricing)    - Free/Pro/Clinic/Enterprise定价
├── 安全设置 (Security)   - 2FA、会话超时、密码策略
├── API配置 (API)         - NVIDIA NIM、外部API密钥
└── 系统参数 (System)     - 上传限制、并发数、数据管理
```

**API集成：**
- `/api/v1/admin/dashboard` - 仪表盘统计数据
- `/api/v1/admin/config` - 系统配置读写

### 管理员权限要求
- 需要 `is_admin = true` 才能访问管理控制台
- 使用 `usePermission` hook 进行权限验证
- 非管理员用户会看到"访问被拒绝"页面

## 下一步计划

1. **完善管理员界面**
   - 患者管理完整实现
   - 批量操作功能
   - 数据导出

2. **用户角色扩展**
   - 企业用户仪表盘
   - SSO集成
   - 审计日志查看

3. **测试覆盖**
   - 权限测试
   - 组件测试
   - E2E测试

---

## 测试覆盖率提升进展 (2025-01-15)

### 目标
将整体测试覆盖率从44%提升到80%+ (参考TESTING_COVERAGE_PLAN.md)

### 已完成
- **Phase 4**: 中等覆盖模块提升
  - `main.py`: 69% → 97% ✅ (164/169行)
  - `auramax_reasoning/llm/client.py`: 56% → 98% ✅ (115/117行)
    - 18个测试用例 (Anthropic/OpenAI/Ollama客户端, 工厂函数, 生命周期)
  - `database/config.py`: 58% → 70% ✅ (部分提升)

- **Phase 5**: 服务层测试 (0% → 70%+)
  - `wearable_service.py`: 0% → **99%** ✅ (76/77行)
    - 12个测试用例覆盖3个核心方法
    - 修复了源代码Decimal/float类型混合bug

- **Phase 3**: API路由测试 (0% → 70-100%) ✅ **已完成**
  - `routers/health.py`: 0% → **85%** ✅ (28/33行)
    - 7个测试用例覆盖健康检查和深度系统检查
    - 包括数据库/缓存/磁盘空间检测
  - `routers/password_reset.py`: 0% → **100%** ✅ (51/51行)
    - 8个测试用例覆盖forgot_password和reset_password
    - 包括有效/无效/过期token测试
  - `routers/email_verification.py`: 0% → **100%** ✅ (59/59行)
    - 9个测试用例覆盖邮箱验证全流程
    - 包括发送验证邮件、token验证、状态查询
  - `routers/data_warehouse.py`: **95%** ✅ (23个测试, 12个端点, Code Review: 4.8/5)
  - `routers/treatment_recommendations.py`: **100%** ✅ (10个测试, 4个端点, Code Review: 4.8/5)
  - `routers/grade.py`: 64% → **94%** ✅ (17个测试, 5个端点, Code Review: 4.7/5)
    - 覆盖assess、assess_batch、get_summary、health_check、quick_assess
    - GRADE证据分级系统完整测试
  - `routers/analytics.py`: 47% → **100%** ✅ (12个测试, 3个端点, Code Review: 4.67/5)
    - 覆盖create_cohort、run_survival_analysis、search_evidence
    - B2B Analytics队列管理和生存分析
    - 使用FastAPI dependency_overrides标准模式
  - ⏭️ 跳过: `molecular.py`, `consent.py`, `billing.py`, `cohort_analysis.py`, `ehr.py` (依赖未实现或未注册)
  - **总结**: 21个已注册router全部达到70%+覆盖率

### 统计数据
- **测试数量**: 574 → **627** (+53个新测试)
- **整体覆盖率**: 44% → **47%** (+3%)
- **新增测试文件**: 7个
  - `tests/test_llm/test_client.py` (18个测试)
  - `tests/test_services/test_wearable_service.py` (12个测试)
  - `tests/test_routers/test_health.py` (7个测试)
  - `tests/test_routers/test_password_reset.py` (8个测试)
  - `tests/test_routers/test_email_verification.py` (9个测试)
  - `tests/test_api/test_grade.py` (17个测试)
  - `tests/test_api/test_analytics.py` (12个测试)
- **源代码修改**:
  - `main.py`: 添加password_reset和email_verification路由注册

### 已完成
- **Phase 3**: API路由测试 ✅ 全部完成
  - 21个已注册router全部达到70%+覆盖率
  - 代码审核平均分: 4.7/5 (优秀)

---

*文档更新时间: 2025-01-16*
*版本: 1.3*
