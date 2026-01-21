# AuraMax 测试账号清单

**环境**: 开发环境  
**更新日期**: 2026-01-19  

---

## 📋 12角色测试账号

> **统一密码**: `Demo@2025`

### 🏥 医院类 (Hospital)

| 角色 | 邮箱 | 密码 | 权限说明 |
|------|------|------|----------|
| 医院管理员 | `hospital.admin@auramax.ai` | `Demo@2025` | 管理医院用户、查看全院数据 |
| 医院合规官 | `hospital.compliance@auramax.ai` | `Demo@2025` | 合规审查、数据隐私管理 |
| 医院科研负责人 | `hospital.research@auramax.ai` | `Demo@2025` | 临床试验、科研数据分析 |

### 💊 药企类 (Pharmaceutical)

| 角色 | 邮箱 | 密码 | 权限说明 |
|------|------|------|----------|
| 药企商务拓展 | `pharma.bd@auramax.ai` | `Demo@2025` | 合作伙伴管理、商务报告 |
| 药企研发 | `pharma.rd@auramax.ai` | `Demo@2025` | 研发数据、临床试验分析 |
| 药企合规官 | `pharma.compliance@auramax.ai` | `Demo@2025` | 药品合规、审计日志 |

### 🔬 研究机构类 (Research Institution)

| 角色 | 邮箱 | 密码 | 权限说明 |
|------|------|------|----------|
| 研究机构管理员 | `research.admin@auramax.ai` | `Demo@2025` | 机构管理、用户权限 |
| 研究项目负责人 | `research.lead@auramax.ai` | `Demo@2025` | 项目管理、队列分析 |

### 🏛️ 平台/监管类 (Platform/Regulatory)

| 角色 | 邮箱 | 密码 | 权限说明 |
|------|------|------|----------|
| 监管审核员 | `regulatory.auditor@auramax.ai` | `Demo@2025` | 监管审核、合规检查 |
| 合规检查员 | `compliance.inspector@auramax.ai` | `Demo@2025` | 现场检查、违规追踪 |
| 运营经理 | `ops.manager@auramax.ai` | `Demo@2025` | 平台运营、用户管理 |
| 超级管理员 | `super.admin@auramax.ai` | `Demo@2025` | 全部权限 |

---

## 🎯 基础测试账号

> **注意**: 这些账号保持原有密码

| 角色 | 邮箱 | 密码 | 权限说明 |
|------|------|------|----------|
| 普通用户 | `user@auramax.ai` | `user1234` | 免费版功能 |
| 专业用户 | `pro@auramax.ai` | `pro1234` | Pro版功能 |
| 管理员 | `admin@auramax.ai` | `Admin@2025` | 管理员权限 |

---

## 🔐 登录方式

### API 登录
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "hospital.admin@auramax.ai", "password": "Demo@2025"}'
```

### 前端登录
1. 打开 http://localhost:3000/login
2. 输入邮箱和密码
3. 系统会根据角色自动跳转到对应仪表盘

---

## 📊 角色路由映射

| 角色 | 默认仪表盘路由 |
|------|----------------|
| `hospital_admin` | `/dashboard/hospital/admin` |
| `hospital_compliance` | `/dashboard/hospital/compliance` |
| `hospital_research` | `/dashboard/hospital/research` |
| `pharma_bd` | `/dashboard/pharma/business` |
| `pharma_rd` | `/dashboard/pharma/research` |
| `pharma_compliance` | `/dashboard/pharma/compliance` |
| `research_admin` | `/dashboard/research/admin` |
| `research_lead` | `/dashboard/research/lead` |
| `regulatory_auditor` | `/dashboard/regulatory/auditor` |
| `compliance_inspector` | `/dashboard/regulatory/compliance` |
| `ops_manager` | `/dashboard/platform/ops` |
| `super_admin` | `/dashboard/platform/admin` |

---

## ⚠️ 安全提醒

1. **仅限开发环境使用** - 生产环境Mock用户会被禁用
2. **不要使用弱密码** - 生产环境应使用强密码策略
3. **定期轮换密钥** - JWT_SECRET应定期更换

---

**文档维护者**: AuraMax DevOps  
**最后更新**: 2026-01-19
