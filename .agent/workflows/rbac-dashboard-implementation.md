---
description: 12角色RBAC仪表盘完整实现工作流
---

# 12角色RBAC仪表盘完整实现工作流

## 目标
为所有12个角色创建功能完整的控制面板，每个链接都连接到真实的后端API。

## 后端API能力总结

### 1. Data Asset Reports (`/api/v1/data-asset`)
- **POST /generate** - 生成报告
- **GET /** - 报告列表
- **GET /:id** - 报告详情
- **GET /download** - 下载PDF
- **GET /summary** - 统计摘要

### 2. Partnership CRM (`/api/v1/partnership`)
- **POST /partners** - 创建合作伙伴
- **GET /partners** - 合作伙伴列表
- **GET /partners/:id** - 合作伙伴详情
- **PUT /partners/:id** - 更新合作伙伴
- **DELETE /partners/:id** - 删除合作伙伴
- **POST /match** - 执行匹配
- **GET /matches/:hospital_id** - 匹配结果
- **PUT /matches/:match_id/status** - 更新匹配状态

## 12角色功能映射

### 医院 (Hospital)

#### 1. Hospital Admin (医院管理员)
**主要功能**:
- ✅ 生成数据资产报告 (Data Asset)
- ✅ 查看报告列表和详情
- ✅ 下载报告
- ✅ 查看合作匹配 (Partnership Matches)
- ✅ 更新匹配状态

**页面结构**:
- `/dashboard/hospital/admin` - 主仪表盘
- `/dashboard/hospital/admin/reports` - 报告列表
- `/dashboard/hospital/admin/reports/new` - 生成新报告
- `/dashboard/hospital/admin/reports/[id]` - 报告详情
- `/dashboard/hospital/admin/matches` - 合作匹配
- `/dashboard/hospital/admin/settings` - 组织设置

#### 2. Hospital Compliance (医院合规官)
**主要功能**:
- ✅ 查看数据资产报告 (只读)
- ✅ 下载报告

**页面结构**:
- `/dashboard/hospital/compliance` - 主仪表盘
- `/dashboard/hospital/compliance/reports` - 报告列表

#### 3. Hospital Research (医院科研负责人)
**主要功能**:
- ✅ 查看数据资产报告
- ✅ 查看合作匹配

**页面结构**:
- `/dashboard/hospital/research` - 主仪表盘
- `/dashboard/hospital/research/reports` - 报告列表
- `/dashboard/hospital/research/matches` - 合作匹配

### 药企 (Pharmaceutical)

#### 4. Pharma BD (药企BD经理)
**主要功能**:
- ✅ 查看授权的数据资产报告
- ✅ 查看合作伙伴列表
- ✅ 更新合作伙伴信息
- ✅ 查看匹配结果
- ✅ 更新匹配状态

**页面结构**:
- `/dashboard/pharma/business` - 主仪表盘
- `/dashboard/pharma/business/partners` - 合作伙伴列表
- `/dashboard/pharma/business/partners/[id]` - 合作伙伴详情
- `/dashboard/pharma/business/data-access` - 数据访问权限
- `/dashboard/pharma/business/matches` - 匹配结果

#### 5. Pharma R&D (药企研发)
**主要功能**:
- ✅ 查看授权的详细数据资产报告
- ✅ 查看合作伙伴列表
- ✅ 数据分析

**页面结构**:
- `/dashboard/pharma/research` - 主仪表盘
- `/dashboard/pharma/research/data-assets` - 数据资产
- `/dashboard/pharma/research/projects` - 研发项目

#### 6. Pharma Compliance (药企合规)
**主要功能**:
- ✅ 查看授权的摘要数据资产报告
- ✅ 查看合作伙伴列表

**页面结构**:
- `/dashboard/pharma/compliance` - 主仪表盘
- `/dashboard/pharma/compliance/reports` - 合规报告

### 研究机构 (Research Institution)

#### 7. Research Admin (研究机构管理员)
**主要功能**:
- ✅ 查看授权的数据资产报告
- ✅ 管理合作伙伴
- ✅ 查看匹配结果
- ✅ 更新匹配状态

**页面结构**:
- `/dashboard/research/admin` - 主仪表盘
- `/dashboard/research/admin/partners` - 合作伙伴
- `/dashboard/research/admin/projects` - 研究项目

#### 8. Research Lead (研究项目负责人)
**主要功能**:
- ✅ 查看授权的数据资产报告
- ✅ 查看合作伙伴列表

**页面结构**:
- `/dashboard/research/lead` - 主仪表盘
- `/dashboard/research/lead/projects` - 项目管理

### 监管 (Regulatory)

#### 9. Regulatory Auditor (监管审核员)
**主要功能**:
- ✅ 查看所有数据资产报告
- ✅ 下载所有报告
- ✅ 查看所有合作伙伴
- ✅ 查看所有匹配结果
- ✅ 审计追踪

**页面结构**:
- `/dashboard/regulatory/auditor` - 主仪表盘
- `/dashboard/regulatory/auditor/reports` - 报告审核
- `/dashboard/regulatory/auditor/organizations` - 组织列表
- `/dashboard/regulatory/auditor/audit-logs` - 审计日志

#### 10. Compliance Inspector (合规检查员)
**主要功能**:
- ✅ 查看所有数据资产报告
- ✅ 查看所有合作伙伴
- ✅ 合规检查

**页面结构**:
- `/dashboard/regulatory/compliance` - 主仪表盘
- `/dashboard/regulatory/compliance/inspections` - 检查记录

### 平台 (Platform)

#### 11. Super Admin (超级管理员)
**主要功能**:
- ✅ 所有权限
- ✅ 创建/管理合作伙伴
- ✅ 执行匹配
- ✅ 系统配置

**页面结构**:
- `/dashboard/platform/admin` - 主仪表盘
- `/dashboard/platform/admin/partners` - 合作伙伴管理
- `/dashboard/platform/admin/matching` - 智能匹配
- `/dashboard/platform/admin/system` - 系统配置

#### 12. Ops Manager (运营经理)
**主要功能**:
- ✅ 管理合作伙伴
- ✅ 执行匹配
- ✅ 运营数据

**页面结构**:
- `/dashboard/platform/ops` - 主仪表盘
- `/dashboard/platform/ops/partners` - 合作伙伴
- `/dashboard/platform/ops/matching` - 匹配管理
- `/dashboard/platform/ops/analytics` - 运营分析

## 实施步骤

### Phase 1: API Client (前端API封装)
1. 扩展 `src/lib/api.ts`，添加：
   - `dataAsset` 模块
   - `partnership` 模块
2. 定义所有 TypeScript 接口

### Phase 2: 共享组件
1. 创建 `src/components/reports/` - 报告相关组件
   - `ReportList.tsx` - 报告列表
   - `ReportCard.tsx` - 报告卡片
   - `ReportDetail.tsx` - 报告详情
2. 创建 `src/components/partnerships/` - 合作伙伴组件
   - `PartnerList.tsx` - 合作伙伴列表
   - `PartnerCard.tsx` - 合作伙伴卡片
   - `MatchList.tsx` - 匹配列表

### Phase 3: 角色仪表盘实现（优先级排序）

**Tier 1 (核心角色)**:
1. Hospital Admin
2. Pharma BD
3. Super Admin

**Tier 2 (次要角色)**:
4. Hospital Compliance
5. Pharma R&D
6. Regulatory Auditor

**Tier 3 (补充角色)**:
7. Hospital Research
8. Pharma Compliance
9. Research Admin
10. Research Lead
11. Compliance Inspector
12. Ops Manager

### Phase 4: 子页面实现
为每个角色创建子页面（reports, partners, matches等）

### Phase 5: 测试与优化
- 权限验证测试
- API 集成测试
- UX 优化

## 技术规范

### API Client 结构
```typescript
export const api = {
  dataAsset: {
    generate: (data: ReportGenerateRequest, token: string) => Promise<ReportResponse>,
    list: (token: string, filters?: {}) => Promise<ReportResponse[]>,
    get: (id: string, token: string) => Promise<ReportResponse>,
    download: (id: string, token: string) => Promise<Blob>,
    summary: (token: string) => Promise<ReportSummaryResponse>,
  },
  partnership: {
    createPartner: (data: PartnerCreateRequest, token: string) => Promise<PartnerResponse>,
    listPartners: (token: string, filters?: {}) => Promise<PartnerResponse[]>,
    getPartner: (id: string, token: string) => Promise<PartnerResponse>,
    updatePartner: (id: string, data: PartnerUpdateRequest, token: string) => Promise<PartnerResponse>,
    deletePartner: (id: string, token: string) => Promise<void>,
    match: (data: MatchRequest, token: string) => Promise<MatchResponse>,
    getMatches: (hospitalId: string, token: string) => Promise<MatchResultResponse[]>,
    updateMatchStatus: (matchId: string, data: MatchStatusUpdateRequest, token: string) => Promise<MatchResultResponse>,
  }
}
```

### 命名规范
- 文件名: `kebab-case`
- 组件名: `PascalCase`
- 变量名: `camelCase`
- 常量名: `UPPER_SNAKE_CASE`

### UI设计原则
- 遵循 Frontend Wizard Skill 指导
- 使用 Glassmorphism + Vibrant Colors
- 所有交互必须有 Feedback
- 使用 Skeleton Loaders

## 进度追踪

- [ ] Phase 1: API Client
- [ ] Phase 2: 共享组件
- [ ] Phase 3: Tier 1 仪表盘
- [ ] Phase 3: Tier 2 仪表盘
- [ ] Phase 3: Tier 3 仪表盘
- [ ] Phase 4: 子页面
- [ ] Phase 5: 测试优化
