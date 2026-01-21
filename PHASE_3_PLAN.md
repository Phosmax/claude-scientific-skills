# Phase 3 执行计划：测试与CI/CD

**版本**: 1.0  
**开始日期**: 2026-01-20  
**预计完成**: 2026-01-27 (1周)  
**当前状态**: 🚀 Phase 3 启动

---

## 📋 Phase 3 总览

### 目标

为 AuraMax RBAC Dashboard 建立完整的测试体系和CI/CD流程：

- ✅ **Backend Unit Tests**: 覆盖核心业务逻辑
- ✅ **Frontend Component Tests**: React组件测试
- ✅ **Integration Tests**: API端到端测试
- ✅ **CI/CD Pipeline**: 自动化测试和部署
- ✅ **Code Coverage**: 目标 >80%

### 技术栈

**Backend Testing**:
- pytest (测试框架)
- pytest-asyncio (异步测试)
- pytest-cov (覆盖率)
- httpx (HTTP测试客户端)
- faker (测试数据生成)

**Frontend Testing**:
- Jest (测试框架)
- React Testing Library (组件测试)
- @testing-library/user-event (用户交互)
- MSW (Mock Service Worker - API mocking)

**CI/CD**:
- GitHub Actions (主要CI/CD平台)
- Docker (容器化)
- Pre-commit Hooks (本地质量检查)

---

## 📅 Phase 3.1: Backend Unit Tests (Day 1-2)

### 3.1.1 测试框架设置 ✅

**文件**: `auramax-core/tests/conftest.py`

**内容**:
- Pytest配置
- 测试数据库设置（SQLite in-memory）
- Fixture定义（app, client, session, auth_tokens）
- Mock用户创建

**预计时间**: 1小时

---

### 3.1.2 PermissionFilter测试 ✅

**文件**: `auramax-core/tests/test_permission_filter.py`

**测试用例**:
1. ✅ `test_is_cross_org_user_with_super_admin` - 特权用户检测
2. ✅ `test_is_cross_org_user_with_regular_user` - 普通用户检测
3. ✅ `test_require_same_org_success` - 同组织访问允许
4. ✅ `test_require_same_org_denied` - 跨组织访问拒绝
5. ✅ `test_require_same_org_allowed_for_privileged` - 特权用户跨组织

**预计时间**: 1.5小时

---

### 3.1.3 Data Asset端点测试 ✅

**文件**: `auramax-core/tests/test_data_asset_endpoints.py`

**测试用例**:
1. ✅ `test_generate_report_success` - 报告生成成功
2. ✅ `test_generate_report_cross_org_denied` - 跨组织生成拒绝
3. ✅ `test_list_reports_organization_filter` - 列表组织过滤
4. ✅ `test_get_report_success` - 获取报告成功
5. ✅ `test_download_report_success` - 下载报告成功
6. ✅ `test_rate_limiting_generate_report` - 速率限制测试

**预计时间**: 2小时

---

### 3.1.4 Partnership端点测试 ✅

**文件**: `auramax-core/tests/test_partnership_endpoints.py`

**测试用例**:
1. ✅ `test_create_partner_success` - 创建合作伙伴
2. ✅ `test_list_partners_org_filter` - 列表组织过滤
3. ✅ `test_update_partner_cross_org_denied` - 跨组织更新拒绝
4. ✅ `test_match_hospital_to_partners` - 匹配算法测试
5. ✅ `test_get_hospital_matches_permission` - 权限检查
6. ✅ `test_rate_limiting_matching` - 匹配速率限制

**预计时间**: 2小时

---

### 3.1.5 结构化日志测试 ✅

**文件**: `auramax-core/tests/test_structured_logging.py`

**测试用例**:
1. ✅ `test_api_access_logging` - API访问日志
2. ✅ `test_data_access_logging` - 数据访问日志
3. ✅ `test_permission_denied_logging` - 权限拒绝日志
4. ✅ `test_log_format_json` - JSON格式验证

**预计时间**: 1小时

**Day 1-2 总计**: ~7.5小时

---

## 📅 Phase 3.2: Frontend Component Tests (Day 3)

### 3.2.1 测试框架设置 ✅

**文件**: `auramax-web/jest.config.js`

**配置**:
- Jest + React Testing Library
- TypeScript支持
- MSW (Mock Service Worker)
- Coverage配置

**预计时间**: 0.5小时

---

### 3.2.2 useRoleGuard Hook测试 ✅

**文件**: `auramax-web/__tests__/hooks/useRoleGuard.test.tsx`

**测试用例**:
1. ✅ `test_authorized_with_allowed_role` - 授权成功
2. ✅ `test_unauthorized_without_allowed_role` - 未授权
3. ✅ `test_require_all_roles` - 需要所有角色
4. ✅ `test_custom_check_function` - 自定义检查

**预计时间**: 1小时

---

### 3.2.3 useDataFetch Hook测试 ✅

**文件**: `auramax-web/__tests__/hooks/useDataFetch.test.tsx`

**测试用例**:
1. ✅ `test_successful_data_fetch` - 数据获取成功
2. ✅ `test_error_handling` - 错误处理
3. ✅ `test_pagination` - 分页功能
4. ✅ `test_refetch` - 重新获取
5. ✅ `test_enabled_false` - 禁用状态

**预计时间**: 1.5小时

---

### 3.2.4 Dashboard Page测试 ✅

**文件**: `auramax-web/__tests__/pages/hospital-admin.test.tsx`

**测试用例**:
1. ✅ `test_renders_for_authorized_user` - 授权用户渲染
2. ✅ `test_access_denied_for_unauthorized` - 未授权拒绝
3. ✅ `test_displays_report_list` - 显示报告列表
4. ✅ `test_pagination_controls` - 分页控件

**预计时间**: 1.5小时

**Day 3 总计**: ~4.5小时

---

## 📅 Phase 3.3: CI/CD Pipeline (Day 4-5)

### 3.3.1 GitHub Actions - Backend CI ✅

**文件**: `.github/workflows/backend-ci.yml`

**流程**:
1. ✅ Checkout代码
2. ✅ 设置Python 3.11
3. ✅ 安装依赖
4. ✅ 运行pytest
5. ✅ 生成coverage报告
6. ✅ 上传到Codecov

**触发条件**:
- Push to `main` branch
- Pull Request

**预计时间**: 1.5小时

---

### 3.3.2 GitHub Actions - Frontend CI ✅

**文件**: `.github/workflows/frontend-ci.yml`

**流程**:
1. ✅ Checkout代码
2. ✅ 设置Node.js 18
3. ✅ 安装依赖
4. ✅ 运行Jest测试
5. ✅ 运行ESLint
6. ✅ 构建Next.js
7. ✅ 上传coverage

**预计时间**: 1.5小时

---

### 3.3.3 Pre-commit Hooks ✅

**文件**: `.pre-commit-config.yaml`

**Hooks**:
1. ✅ trailing-whitespace
2. ✅ end-of-file-fixer
3. ✅ check-yaml
4. ✅ black (Python格式化)
5. ✅ isort (Python import排序)
6. ✅ flake8 (Python linting)
7. ✅ prettier (Frontend格式化)

**预计时间**: 1小时

---

### 3.3.4 Docker容器化 ✅

**文件**: 
- `auramax-core/Dockerfile`
- `auramax-web/Dockerfile`
- `docker-compose.yml`

**内容**:
- Multi-stage builds
- Production优化
- Health checks
- Volume配置

**预计时间**: 2小时

**Day 4-5 总计**: ~6小时

---

## 📅 Phase 3.4: Integration Tests (Day 6)

### 3.4.1 API集成测试 ✅

**文件**: `auramax-core/tests/integration/test_api_workflow.py`

**测试用例**:
1. ✅ `test_full_report_generation_workflow`
   - 登录 → 生成报告 → 获取报告 → 下载报告
2. ✅ `test_partnership_matching_workflow`
   - 创建Partner → 执行匹配 → 更新状态
3. ✅ `test_cross_org_access_denied_workflow`
   - 测试组织隔离

**预计时间**: 2小时

---

### 3.4.2 端到端测试 (可选)

**工具**: Playwright / Cypress

**测试用例**:
1. ✅ 用户登录流程
2. ✅ 报告生成和下载
3. ✅ 权限拒绝场景

**预计时间**: 2小时 (Phase 3.5可选)

**Day 6 总计**: ~4小时

---

## 📅 Phase 3.5: 文档与优化 (Day 7)

### 3.5.1 测试文档 ✅

**文件**: `docs/TESTING_GUIDE.md`

**内容**:
- 如何运行测试
- 如何编写新测试
- 测试最佳实践
- CI/CD流程说明

**预计时间**: 1.5小时

---

### 3.5.2 Coverage报告 ✅

**文件**: `COVERAGE_REPORT.md`

**内容**:
- Backend coverage统计
- Frontend coverage统计
- 未覆盖区域分析
- 改进建议

**预计时间**: 0.5小时

---

### 3.5.3 Phase 3完成报告 ✅

**文件**: `PHASE_3_COMPLETION_REPORT.md`

**内容**:
- 所有测试结果
- CI/CD配置总结
- 质量指标
- 下一步建议

**预计时间**: 1小时

**Day 7 总计**: ~3小时

---

## 🎯 Phase 3 成功标准

### 代码覆盖率目标

| 组件 | 目标覆盖率 | 最低要求 |
|------|-----------|---------|
| Backend - 核心逻辑 | >80% | >70% |
| Backend - 端点 | >75% | >60% |
| Frontend - Hooks | >90% | >80% |
| Frontend - Components | >70% | >60% |

### CI/CD指标

- ✅ 所有PR必须通过CI
- ✅ 测试运行时间<5分钟
- ✅ 自动部署到staging环境
- ✅ 代码质量检查通过

### 质量门禁

- ✅ 无critical/high安全漏洞
- ✅ 代码覆盖率>70%
- ✅ 所有测试通过
- ✅ Linting无错误

---

## 📊 预计时间分配

| Phase | 任务 | 时间 |
|-------|------|------|
| 3.1 | Backend Tests | 7.5h |
| 3.2 | Frontend Tests | 4.5h |
| 3.3 | CI/CD | 6h |
| 3.4 | Integration Tests | 4h |
| 3.5 | 文档 | 3h |
| **总计** | | **~25h** |

**实际预期**: 1周内完成（每天4-5小时工作）

---

## 🚀 执行顺序

### Day 1-2: Backend Tests (High Priority)
```
✅ 测试框架设置
✅ PermissionFilter测试
✅ Data Asset端点测试
✅ Partnership端点测试
✅ 日志测试
```

### Day 3: Frontend Tests
```
✅ Jest配置
✅ Hook测试
✅ 组件测试
```

### Day 4-5: CI/CD
```
✅ GitHub Actions (Backend)
✅ GitHub Actions (Frontend)
✅ Pre-commit Hooks
✅ Docker容器化
```

### Day 6: Integration Tests
```
✅ API工作流测试
✅ 端到端测试 (可选)
```

### Day 7: Polish & Docs
```
✅ 测试文档
✅ Coverage报告
✅ 完成报告
```

---

## 📝 备注

### 测试优先级

**P0 (必须)**:
- PermissionFilter测试
- Data Asset核心端点
- useRoleGuard Hook
- CI/CD基础

**P1 (重要)**:
- Partnership端点
- useDataFetch Hook
- 日志系统测试
- Docker配置

**P2 (建议)**:
- 端到端测试
- 负载测试
- 安全扫描

### 技术债务追踪

**已知问题**:
1. Rate limiter使用内存存储（需迁移Redis）
2. Mock用户系统（生产需迁移数据库）
3. 部分端点缺少输入验证测试

**Phase 4建议**:
1. 性能测试（Locust）
2. 安全扫描（Bandit, Safety）
3. 负载测试
4. Kubernetes部署

---

## 🔗 相关文档

- **Phase 2完成**: `PHASE_2_COMPLETE_SUMMARY.md`
- **开发者指南**: `docs/DEVELOPER_GUIDE.md`
- **部署指南**: `DEPLOYMENT_GUIDE.md`

---

**创建时间**: 2026-01-20  
**状态**: 🚀 Phase 3 Ready to Start  
**负责人**: Antigravity AI
