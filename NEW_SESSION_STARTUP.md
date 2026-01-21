# 🚀 AuraMax RBAC - 新会话启动文档

**会话类型**: Phase 2.2 后端基础设施继续开发  
**上一会话完成时间**: 2026-01-20  
**当前进度**: Phase 2.2 (60% 完成)

---

## 📋 上下文总结

我正在为 **AuraMax B2B 医疗数据分析平台** 开发 **12角色RBAC仪表盘系统**。

### 项目背景
- **产品**: AuraMax Professional (B2B企业级)
- **目标客户**: 制药公司、CRO、研究机构
- **核心功能**: 
  1. 数据资产报告管理
  2. 合作匹配（Partnership CRM）
  3. 队列分析
  4. 证据合成

### 技术栈
- **后端**: FastAPI + SQLAlchemy + PostgreSQL
- **前端**: Next.js + TypeScript + Tailwind
- **认证**: JWT + 12角色RBAC

---

## ✅ 已完成工作

### Phase 2.1 - 前端基础设施 (100% ✅)

**交付成果**:
1. ✅ **5个核心Hooks**:
   - `useRoleGuard` - 权限守卫（解决Race Condition）
   - `useAPI` - 统一API调用
   - `useDataFetch` - 高级数据获取（分页、过滤、搜索）
   - 文档: `auramax-web/src/hooks/README.md`

2. ✅ **2个UI组件**:
   - `ErrorBoundary` - 错误边界
   - `LoadingSpinner` - 加载状态

3. ✅ **重构示例**:
   - `hospital/admin/page.tsx` - 展示正确使用模式

4. ✅ **完整文档**:
   - 系统审计报告
   - 实施计划
   - 任务清单

**关键成就**: 
- 代码复用率提升70%
- 解决了12个仪表盘的权限检查Race Condition
- 代码质量: 4.8/5

---

### Phase 2.2 - 后端基础设施 (60% ⏳)

**已完成**:
1. ✅ 结构化日志系统
   - 文件: `auramax-core/src/auramax_api/utils/structured_logging.py`
   - 功能: JSON格式日志、API访问审计、权限审计

2. ✅ API速率限制
   - 文件: `auramax-core/src/auramax_api/utils/rate_limiter.py`
   - 功能: 用户级/IP级限流、差异化限制策略

3. ✅ PermissionFilter分析
   - 现有实现已存在但需要优化

---

## 🎯 当前任务：完成 Phase 2.2

### 待完成任务清单

#### Task 2.2.1: PermissionFilter重构优化 (2小时)
**目标**: 简化权限过滤代码，消除重复

**需要做的**:
```python
# 在 auramax-core/src/auramax_api/auth/filters.py 中添加:

class PermissionFilter:
    # ... existing code ...
    
    def is_cross_org_user(self) -> bool:
        """判断是否为跨组织特权用户"""
        return any(role in self.CROSS_ORG_ROLES for role in self.current_user.roles)
    
    def filter_query_by_org(self, query, org_field_name: str = "organization_id"):
        """
        自动为查询添加组织过滤
        
        Args:
            query: SQLAlchemy查询对象
            org_field_name: 组织ID字段名（默认organization_id）
        
        Returns:
            添加组织过滤的查询（特权用户不过滤）
        """
        if self.is_cross_org_user():
            return query  # 特权用户看所有数据
        
        # 普通用户只看本组织
        return query.where(
            getattr(query.column_descriptions[0]['type'], org_field_name) 
            == self.current_user.organization_id
        )
    
    def require_same_org(self, resource_org_id: str, resource_type: str = "资源"):
        """
        要求资源属于同一组织（非特权用户）
        
        Args:
            resource_org_id: 资源所属组织ID
            resource_type: 资源类型（用于错误消息）
        
        Raises:
            HTTPException: 如果跨组织访问被拒绝
        """
        if self.is_cross_org_user():
            return  # 特权用户允许跨组织
        
        if resource_org_id != self.current_user.organization_id:
            raise HTTPException(
                status_code=403,
                detail=f"无权访问其他组织的{resource_type}。"
                       f"当前组织: {self.current_user.organization_id}, "
                       f"目标组织: {resource_org_id}"
            )
```

---

#### Task 2.2.2: Data Asset端点优化 (2小时)
**文件**: `auramax-core/src/auramax_api/routers/data_asset.py`

**执行步骤**:
1. 在所有端点导入结构化日志:
   ```python
   from ..utils.structured_logging import structured_logger
   from ..utils.rate_limiter import limiter, get_rate_limit
   ```

2. 添加速率限制装饰器:
   ```python
   @router.post("/generate")
   @limiter.limit(get_rate_limit("report_generate"))
   async def generate_report(...):
   ```

3. 替换手写权限检查:
   ```python
   # 更新前：
   if not any(role in perm_filter.CROSS_ORG_ROLES for role in user.roles):
       if request.hospital_id != user.organization_id:
           raise HTTPException(403, ...)
   
   # 更新后：
   perm_filter.require_same_org(request.hospital_id, "医院报告")
   ```

4. 添加审计日志:
   ```python
   structured_logger.data_access(
       action="CREATE",
       resource_type="data_asset_report",
       resource_id=str(report.id),
       user_id=user.sub,
       organization_id=user.organization_id
   )
   ```

5. 优化查询过滤:
   ```python
   # 更新前：
   stmt = select(DataAssetReport)
   if not any(role in perm_filter.CROSS_ORG_ROLES for role in user.roles):
       stmt = stmt.where(DataAssetReport.hospital_id == user.organization_id)
   
   # 更新后：
   stmt = select(DataAssetReport)
   if not perm_filter.is_cross_org_user():
       stmt = stmt.where(DataAssetReport.hospital_id == user.organization_id)
   ```

---

#### Task 2.2.3: Partnership端点优化 (2小时)
**文件**: `auramax-core/src/auramax_api/routers/partnership.py`

**执行步骤**: 
（与Task 2.2.2类似，应用到partnership端点）

1. 添加速率限制（匹配端点使用`matching`限制）
2. 使用`perm_filter.require_same_org()`
3. 添加数据访问审计日志
4. 简化查询过滤逻辑

---

#### Task 2.2.4: 集成到main.py (0.5小时)
**文件**: `auramax-core/src/auramax_api/main.py`

**添加代码**:
```python
# 1. 导入
from .utils.rate_limiter import limiter, _rate_limit_exceeded_handler
from .utils.structured_logging import structured_logger
from slowapi.errors import RateLimitExceeded
import logging

# 2. 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',  # 只输出消息（已是JSON）
    handlers=[logging.StreamHandler()]
)

# 3. 注册速率限制
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 4. 中间件：记录所有API请求
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = (time.time() - start_time) * 1000  # 转为毫秒
    
    # 获取用户信息（如果已认证）
    user_id = getattr(request.state, "user", {}).get("sub", "anonymous")
    user_roles = getattr(request.state, "user", {}).get("roles", [])
    
    structured_logger.api_access(
        endpoint=request.url.path,
        method=request.method,
        user_id=user_id,
        user_roles=user_roles,
        status=response.status_code,
        duration_ms=duration
    )
    
    return response
```

---

### Phase 2.3 - 文档 (待执行)
1. 生成OpenAPI文档
2. 创建开发者指南
3. 更新DEPLOYMENT_GUIDE.md

---

## 📚 重要文件路径

### 前端
- Hooks: `auramax-web/src/hooks/`
- 组件: `auramax-web/src/components/`
- API Client: `auramax-web/src/lib/api.ts`
- 示例页面: `auramax-web/src/app/dashboard/hospital/admin/page.tsx`

### 后端
- 权限过滤: `auramax-core/src/auramax_api/auth/filters.py`
- Data Asset: `auramax-core/src/auramax_api/routers/data_asset.py`
- Partnership: `auramax-core/src/auramax_api/routers/partnership.py`
- 结构化日志: `auramax-core/src/auramax_api/utils/structured_logging.py`
- 速率限制: `auramax-core/src/auramax_api/utils/rate_limiter.py`

### 文档
- 审计报告: `AURAMAX_RBAC_AUDIT_AND_PLAN.md`
- 任务清单: `PHASE_2_TASK_CHECKLIST.md`
- Phase 2.1完成: `PHASE_2.1_COMPLETION_REPORT.md`
- Phase 2.2进度: `PHASE_2.2_PARTIAL_COMPLETION.md`

---

## 🎯 我的下一步要求

请帮我完成 **Phase 2.2 的剩余任务**：

1. **Task 2.2.1** - 重构PermissionFilter，添加便捷方法
2. **Task 2.2.2** - 优化data_asset.py端点
3. **Task 2.2.3** - 优化partnership.py端点  
4. **Task 2.2.4** - 集成到main.py

每完成一个子任务后，请进行代码审计并记录。

完成后创建 **Phase 2.2 Checkpoint 审计报告**。

---

## 📖 参考资料

### 现有实现示例
参考 `auramax-web/src/app/dashboard/hospital/admin/page.tsx` 查看：
- 如何使用 `useRoleGuard`
- 如何使用 `useAPI`
- Loading状态处理模式

### 权限矩阵
参考 `auramax-web/src/lib/permissions.ts` 中的 `API_PERMISSIONS`

### 测试账号
所有测试账号密码: `Demo@2025`  
详情见: `docs/TEST_ACCOUNTS.md`

---

## ✅ 成功标准

Phase 2.2 完成后应达到：
- [ ] 所有API端点有组织ID过滤
- [ ] 所有API端点有速率限制
- [ ] 所有数据访问操作有审计日志
- [ ] 代码重复率\u003c10%
- [ ] PermissionFilter使用一致

---

**开始吧！让我们完成 Phase 2.2！** 🚀
