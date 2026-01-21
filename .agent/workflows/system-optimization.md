---
description: AuraMax 系统优化与加固综合工作流 (HIPAA合规与企业级架构)
---

# AuraMax 系统优化与加固实施计划

本工作流旨在将 AuraMax 从开发原型转化为生产就绪、HIPAA 合规的医疗分析平台。

## Phase 0: Pre-flight Checks (Environment)
- [ ] Verify Codebase Consistency (Lint/Audit)
- [ ] Confirm Python 3.11+ & Node Environment
- [ ] Check Docker Availability

## Phase 1: 基础设施核心升级 (Infrastructure Core)
**目标**: 迁移出 SQLite，建立高可用、强一致性的数据库层。

### 1.1 Docker Compose 生产化
- [ ] 创建 `docker-compose.prod.yml`
- [ ] 配置 PostgreSQL 16 (带健康检查和数据卷持久化)
- [ ] 配置 Redis 7 (用于缓存和任务队列)
- [ ] **// turbo** 配置必要的环境变量 (API_PORT, DB_PORT等)

### 1.2 数据库迁移 (Migration)
- [ ] 修改 `src/auramax_api/database/config.py` 以支持 PostgreSQL 连接串
- [ ] 创建新的 Alembic 迁移脚本 `init_postgres`
- [ ] 验证数据迁移 (Schema 兼容性)

### 1.3 依赖更新
- [ ] **// turbo** 添加 `cryptography` (安全加密) 依赖
- [ ] **// turbo** 添加 `fhir.resources` (FHIR标准库) 依赖

## Phase 2: 安全与合规加固 (Security & Compliance)
**目标**: 满足 HIPAA 对数据加密和审计的要求。

### 2.1 字段级加密 (Encryption at Rest)
- [ ] 实现 `EncryptedType` SQLAlchemy 类型 (基于 Fernet)
- [ ] 将 `Patient` 和 `User` 表中的敏感字段 (如 `full_name`, `email`, `mrn`) 标记为加密列
- [ ] 更新 `User` 模型，迁移现有明文数据(如果有)

### 2.2 审计日志增强 (Audit Logging)
- [ ] 扩展 `AuditLog` 模型，增加 `read` 操作类型支持
- [ ] 创建全局 Middleware 或 DAO 装饰器，自动记录所有 PHI 数据的访问 (Read Access)
- [ ] 确保审计日志本身的不可篡改性 (逻辑层)

## Phase 3: 医疗互操作性重构 (FHIR Interoperability)
**目标**: 使用行业标准重构脆弱的手动集成。

### 3.1 FHIR 客户端重构
- [ ] 使用 `fhir.resources` 库重写 `src/auramax_api/fhir/client.py`
- [ ] 实现 `Patient`, `Observation`, `MedicationStatement` 资源的规范化构建和解析
- [ ] 增加输入验证，确保发出的 FHIR 数据符合 R4 规范

## Phase 4: 前端体验与性能 (Frontend & Performance)
**目标**: 提升用户体验并覆盖关键的患者端场景。

### 4.1 患者门户前端
- [ ] 创建患者登录/注册入口 (User Role = PATIENT)
- [ ] 实现 "我的报告" 页面 (只读权限)
- [ ] 优化移动端响应式布局

### 4.2 性能优化
- [ ] 引入 `Sentry` 或类似前端监控 (Mock setup)
- [ ] 优化 Next.js 构建配置 (Tree shaking)

---
**执行说明**:
- 请按顺序执行 Phase 1 -> 4。
- 每完成一个 Phase 需进行集成测试。
