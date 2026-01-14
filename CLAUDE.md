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

### 5标签页结构
```
/admin/dashboard
├── 概览 (Overview)       - 系统统计卡片、团队状态、最近活动
├── 团队管理 (Team)       - 成员CRUD、状态管理、角色分配
├── 患者管理 (Patients)   - 患者CRUD、CSV导入导出
├── 数据分析 (Analytics)  - 报告统计、活跃患者分析
└── 系统设置 (Settings)   - 诊所信息、NVIDIA NIM API配置
```

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

*文档更新时间: 2025-01-14*
*版本: 1.1*
