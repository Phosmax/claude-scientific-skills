# AuraMax RBAC Dashboard - Developer Guide

**Version**: 1.0  
**Last Updated**: 2026-01-20  
**Target Audience**: Backend/Frontend Developers

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Adding New Roles](#adding-new-roles)
3. [Adding New API Endpoints](#adding-new-api-endpoints)
4. [Adding New Dashboard Pages](#adding-new-dashboard-pages)
5. [Permission System](#permission-system)
6. [Testing](#testing)
7. [Best Practices](#best-practices)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+ (production only)

### Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/auramax/auramax-rbac.git
cd auramax-rbac

# 2. Backend setup
cd auramax-core
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd ../auramax-web
npm install

# 4. Environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Run backend
cd ../auramax-core
uvicorn auramax_api.main:app --reload --port 8000

# 6. Run frontend
cd ../auramax-web
npm run dev
```

**Access**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 👤 Adding New Roles

### Step 1: Define Role in Permission Matrix

**File**: `auramax-web/src/lib/permissions.ts`

```typescript
// 1. Add to ROLES constant
export const ROLES = {
  // ... existing roles
  CRO_MANAGER: 'cro_manager',      // New: CRO Manager
  CRO_RESEARCHER: 'cro_researcher', // New: CRO Researcher
} as const;

// 2. Add to ROLE_CATEGORIES
export const ROLE_CATEGORIES = {
  // ... existing categories
  cro: ['cro_manager', 'cro_researcher'],
};

// 3. Define permissions in API_PERMISSIONS
export const API_PERMISSIONS = {
  // ... existing permissions
  
  // New CRO permissions
  cro_manager: {
    dataAsset: { list: true, view: true, generate: false },
    partnership: { list: true, view: true, create: false, update: true },
    cohort: { list: true, view: true, create: true },
  },
  cro_researcher: {
    dataAsset: { list: true, view: true, generate: false },
    partnership: { list: true, view: true, create: false, update: false },
    cohort: { list: true, view: true, create: true },
  },
};

// 4. Add to ROLE_NAMES (i18n keys)
export const ROLE_NAMES = {
  // ... existing
  cro_manager: 'roles.croManager',
  cro_researcher: 'roles.croResearcher',
};
```

### Step 2: Add Backend Role

**File**: `auramax-core/src/auramax_api/main.py`

```python
# Add to MOCK_USERS (for testing)
MOCK_USERS = {
    # ... existing users
    
    "cro.manager@auramax.ai": {
        "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "cro.manager@auramax.ai")),
        "email": "cro.manager@auramax.ai",
        "password_hash": DEFAULT_HASH,
        "roles": ["user", "cro_manager"],
        "tier": "enterprise",
        "full_name": "CRO Manager",
        "organization_type": "CRO",
        "organization_name": "Example CRO Inc.",
    },
    "cro.researcher@auramax.ai": {
        "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "cro.researcher@auramax.ai")),
        "email": "cro.researcher@auramax.ai",
        "password_hash": DEFAULT_HASH,
        "roles": ["user", "cro_researcher"],
        "tier": "enterprise",
        "full_name": "CRO Researcher",
        "organization_type": "CRO",
        "organization_name": "Example CRO Inc.",
    },
}
```

### Step 3: Add Translation Keys

**File**: `auramax-web/messages/en.json`

```json
{
  "roles": {
    "croManager": "CRO Manager",
    "croResearcher": "CRO Researcher"
  },
  "dashboard": {
    "cro": {
      "title": "CRO Dashboard",
      "manager": {
        "title": "CRO Manager Portal"
      },
      "researcher": {
        "title": "CRO Researcher Portal"
      }
    }
  }
}
```

**File**: `auramax-web/messages/zh.json`

```json
{
  "roles": {
    "croManager": "CRO管理员",
    "croResearcher": "CRO研究员"
  },
  "dashboard": {
    "cro": {
      "title": "CRO仪表盘",
      "manager": {
        "title": "CRO管理员门户"
      },
      "researcher": {
        "title": "CRO研究员门户"
      }
    }
  }
}
```

### Step 4: Update PermissionFilter (if needed)

**File**: `auramax-core/src/auramax_api/auth/filters.py`

```python
class PermissionFilter:
    # If CRO roles need cross-org access:
    CROSS_ORG_ROLES = {
        "super_admin", 
        "ops_manager", 
        "regulatory_auditor", 
        "compliance_inspector",
        # "cro_manager",  # Uncomment if CRO needs cross-org access
    }
```

---

## 🔌 Adding New API Endpoints

### Step 1: Create Router File

**File**: `auramax-core/src/auramax_api/routers/my_feature.py`

```python
"""
My Feature Router - Description of this feature
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..database.models import MyModel
from ..auth.middleware import require_roles
from ..auth.jwt_handler import TokenData
from ..auth.filters import get_perm_filter, PermissionFilter
from ..utils.structured_logging import structured_logger
from ..utils.rate_limiter import limiter, get_rate_limit

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/my-feature", tags=["My Feature"])


# ====== Pydantic Models ======

class MyRequest(BaseModel):
    """Request model for creating resource"""
    name: str = Field(..., min_length=1, max_length=200)
    organization_id: str = Field(..., description="Organization ID")


class MyResponse(BaseModel):
    """Response model"""
    id: str
    name: str
    organization_id: str
    created_at: datetime


# ====== API Endpoints ======

@router.post("/", response_model=MyResponse, status_code=201)
@limiter.limit(get_rate_limit("data_query"))
async def create_resource(
    req: Request,
    request: MyRequest,
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(require_roles(["hospital_admin", "super_admin"])),
    perm_filter: PermissionFilter = Depends(get_perm_filter)
):
    """
    Create a new resource
    
    Permissions:
    - hospital_admin: Create for own organization
    - super_admin: Create for any organization
    """
    try:
        # 1. Permission check
        perm_filter.require_same_org(request.organization_id, "资源")
        
        # 2. Business logic
        resource = MyModel(
            name=request.name,
            organization_id=request.organization_id
        )
        
        session.add(resource)
        await session.commit()
        await session.refresh(resource)
        
        # 3. Audit logging
        structured_logger.data_access(
            action="CREATE",
            resource_type="my_resource",
            resource_id=str(resource.id),
            user_id=user.sub,
            organization_id=user.organization_id
        )
        
        return MyResponse(
            id=str(resource.id),
            name=resource.name,
            organization_id=resource.organization_id,
            created_at=resource.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[MyResponse])
@limiter.limit(get_rate_limit("data_query"))
async def list_resources(
    req: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(require_roles(["hospital_admin", "super_admin"])),
    perm_filter: PermissionFilter = Depends(get_perm_filter)
):
    """List resources with pagination"""
    try:
        from sqlalchemy import select
        
        stmt = select(MyModel)
        
        # Organization-level filtering
        if not perm_filter.is_cross_org_user():
            stmt = stmt.where(MyModel.organization_id == user.organization_id)
        
        stmt = stmt.offset(skip).limit(limit)
        
        result = await session.execute(stmt)
        resources = result.scalars().all()
        
        return [
            MyResponse(
                id=str(r.id),
                name=r.name,
                organization_id=r.organization_id,
                created_at=r.created_at
            )
            for r in resources
        ]
        
    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 2: Register Router in Main

**File**: `auramax-core/src/auramax_api/main.py`

```python
# 1. Import router
from .routers.my_feature import router as my_feature_router

# 2. Include router (add before health router)
app.include_router(my_feature_router, tags=["My Feature"])
```

### Step 3: Create Database Model

**File**: `auramax-core/src/auramax_api/database/models.py`

```python
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class MyModel(Base):
    __tablename__ = "my_resources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    organization_id = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Step 4: Create Migration

```bash
cd auramax-core
alembic revision -m "add my_resources table"
# Edit the generated migration file
alembic upgrade head
```

---

## 🖥️ Adding New Dashboard Pages

### Step 1: Create Page Component

**File**: `auramax-web/src/app/dashboard/my-feature/page.tsx`

```typescript
'use client';

import { useTranslations } from 'next-intl';
import { useRoleGuard } from '@/hooks/useRoleGuard';
import { useDataFetch } from '@/hooks/useDataFetch';
import { api } from '@/lib/api';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function MyFeaturePage() {
  const t = useTranslations('dashboard.myFeature');
  
  // Permission guard
  const { isAuthorized, isLoading: authLoading } = useRoleGuard({
    allowedRoles: ['hospital_admin', 'super_admin'],
    requireAll: false,
  });
  
  // Data fetching with pagination
  const {
    data: resources,
    loading,
    error,
    pagination,
    fetchData,
  } = useDataFetch({
    fetchFn: (token, page, limit) => 
      api.myFeature.list(token, { skip: (page - 1) * limit, limit }),
    enabled: isAuthorized,
    pageSize: 20,
  });
  
  if (authLoading || loading) {
    return <LoadingSpinner />;
  }
  
  if (!isAuthorized) {
    return (
      <div className="p-8 text-center">
        <h1 className="text-2xl font-bold text-red-600">
          {t('accessDenied')}
        </h1>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="p-8 text-center">
        <h1 className="text-xl text-red-600">{error}</h1>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">{t('title')}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {resources?.map((resource) => (
          <div key={resource.id} className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-semibold">{resource.name}</h3>
            <p className="text-sm text-gray-600">
              {new Date(resource.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
      
      {/* Pagination */}
      <div className="mt-6 flex justify-center gap-2">
        <button
          onClick={() => pagination.goToPage(pagination.currentPage - 1)}
          disabled={pagination.currentPage === 1}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Previous
        </button>
        <span className="px-4 py-2">
          Page {pagination.currentPage} of {pagination.totalPages}
        </span>
        <button
          onClick={() => pagination.goToPage(pagination.currentPage + 1)}
          disabled={pagination.currentPage >= pagination.totalPages}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

### Step 2: Add API Client Method

**File**: `auramax-web/src/lib/api.ts`

```typescript
export const api = {
  // ... existing methods
  
  myFeature: {
    list: async (token: string, params?: { skip?: number; limit?: number }) => {
      return apiRequest<MyResource[]>(
        '/api/v1/my-feature/',
        { method: 'GET', params },
        token
      );
    },
    
    create: async (token: string, data: CreateMyResourceRequest) => {
      return apiRequest<MyResource>(
        '/api/v1/my-feature/',
        { method: 'POST', body: JSON.stringify(data) },
        token
      );
    },
  },
};
```

### Step 3: Add Navigation Menu Item

**File**: `auramax-web/src/components/NavigationMenu.tsx`

```typescript
const menuItems = [
  // ... existing items
  {
    href: '/dashboard/my-feature',
    label: t('menu.myFeature'),
    icon: '🚀',
    roles: ['hospital_admin', 'super_admin'],
  },
];
```

### Step 4: Add Translations

**File**: `auramax-web/messages/en.json`

```json
{
  "dashboard": {
    "myFeature": {
      "title": "My Feature",
      "accessDenied": "Access Denied",
      "empty": "No resources found"
    }
  },
  "menu": {
    "myFeature": "My Feature"
  }
}
```

---

## 🔒 Permission System

### Frontend Permission Guard

```typescript
import { useRoleGuard } from '@/hooks/useRoleGuard';

// Option 1: Any role
const { isAuthorized } = useRoleGuard({
  allowedRoles: ['hospital_admin', 'super_admin'],
  requireAll: false,  // User needs ANY of these roles
});

// Option 2: All roles
const { isAuthorized } = useRoleGuard({
  allowedRoles: ['user', 'hospital_admin'],
  requireAll: true,  // User needs ALL these roles
});

// Option 3: Custom check
const { isAuthorized, hasRole } = useRoleGuard({
  allowedRoles: [],
  customCheck: (roles) => {
    return roles.includes('super_admin') || 
           (roles.includes('hospital_admin') && someCondition);
  },
});
```

### Backend Permission Check

```python
from ..auth.middleware import require_roles
from ..auth.filters import get_perm_filter, PermissionFilter

# Option 1: Role-based (endpoint level)
@router.get("/")
async def my_endpoint(
    user: TokenData = Depends(require_roles(["hospital_admin", "super_admin"]))
):
    pass

# Option 2: Organization-based (data level)
@router.get("/{resource_id}")
async def get_resource(
    resource_id: str,
    perm_filter: PermissionFilter = Depends(get_perm_filter)
):
    resource = await get_resource_by_id(resource_id)
    
    # Enforce same-org access
    perm_filter.require_same_org(resource.organization_id, "Resource")
    
    return resource

# Option 3: Custom permission logic
@router.post("/")
async def create_resource(
    request: MyRequest,
    user: TokenData = Depends(get_current_user),
    perm_filter: PermissionFilter = Depends(get_perm_filter)
):
    # Custom check
    if user.tier != "enterprise":
        raise HTTPException(403, "Enterprise tier required")
    
    # Organization check
    perm_filter.require_same_org(request.organization_id, "Resource")
```

---

## 🧪 Testing

### Backend Unit Tests

Create `tests/test_my_feature.py`:

```python
import pytest
from fastapi.testclient import TestClient
from auramax_api.main import app

client = TestClient(app)

def test_create_resource_success():
    # Login
    response = client.post("/api/v1/auth/login", json={
        "email": "hospital.admin@auramax.ai",
        "password": "Demo@2025"
    })
    token = response.json()["access_token"]
    
    # Create resource
    response = client.post(
        "/api/v1/my-feature/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Resource",
            "organization_id": "test-org-id"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Resource"

def test_create_resource_cross_org_denied():
    # Login as hospital admin
    response = client.post("/api/v1/auth/login", json={
        "email": "hospital.admin@auramax.ai",
        "password": "Demo@2025"
    })
    token = response.json()["access_token"]
    
    # Try to create for different org
    response = client.post(
        "/api/v1/my-feature/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Resource",
            "organization_id": "other-org-id"  # Different org
        }
    )
    
    assert response.status_code == 403

def test_rate_limiting():
    response = client.post("/api/v1/auth/login", json={
        "email": "hospital.admin@auramax.ai",
        "password": "Demo@2025"
    })
    token = response.json()["access_token"]
    
    # Make 100 requests
    for i in range(100):
        response = client.get(
            "/api/v1/my-feature/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if i < 60:
            assert response.status_code == 200
        else:
            # Should hit rate limit (60/min)
            assert response.status_code == 429
```

### Frontend Component Tests

Create `__tests__/MyFeaturePage.test.tsx`:

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import MyFeaturePage from '@/app/dashboard/my-feature/page';

jest.mock('@/hooks/useRoleGuard', () => ({
  useRoleGuard: () => ({
    isAuthorized: true,
    isLoading: false,
    hasRole: jest.fn(),
  }),
}));

jest.mock('@/hooks/useDataFetch', () => ({
  useDataFetch: () => ({
    data: [
      { id: '1', name: 'Test Resource', created_at: '2026-01-20' }
    ],
    loading: false,
    error: null,
    pagination: {
      currentPage: 1,
      totalPages: 1,
      goToPage: jest.fn(),
    },
  }),
}));

describe('MyFeaturePage', () => {
  it('renders page title', async () => {
    render(<MyFeaturePage />);
    
    await waitFor(() => {
      expect(screen.getByText('My Feature')).toBeInTheDocument();
    });
  });
  
  it('displays resources', async () => {
    render(<MyFeaturePage />);
    
    await waitFor(() => {
      expect(screen.getByText('Test Resource')).toBeInTheDocument();
    });
  });
});
```

---

## 📝 Best Practices

### 1. Always Use PermissionFilter

❌ **Don't do this**:
```python
if user.organization_id != resource.organization_id:
    raise HTTPException(403, "Access denied")
```

✅ **Do this**:
```python
perm_filter.require_same_org(resource.organization_id, "Resource")
```

### 2. Add Audit Logging for Sensitive Operations

```python
structured_logger.data_access(
    action="DELETE",  # CREATE, READ, UPDATE, DELETE, DOWNLOAD
    resource_type="patient_record",
    resource_id=patient_id,
    user_id=user.sub,
    organization_id=user.organization_id
)
```

### 3. Use Rate Limiting

```python
@router.post("/expensive-operation")
@limiter.limit(get_rate_limit("report_generate"))  # 5/min
async def expensive_op(req: Request, ...):
    pass
```

### 4. Frontend: Always Use Hooks

❌ **Don't fetch data directly**:
```typescript
const [data, setData] = useState([]);
useEffect(() => {
  fetch('/api/...').then(...);
}, []);
```

✅ **Use useDataFetch**:
```typescript
const { data, loading, error } = useDataFetch({
  fetchFn: (token) => api.myFeature.list(token),
  enabled: true,
});
```

### 5. Consistent Error Handling

```python
try:
    # Business logic
    pass
except HTTPException:
    raise  # Re-raise HTTP exceptions
except Exception as e:
    logger.error(f"Error in my_endpoint: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

### 6. i18n for All UI Text

❌ **Hard-coded strings**:
```typescript
<h1>My Dashboard</h1>
```

✅ **Use translations**:
```typescript
const t = useTranslations('dashboard.myFeature');
<h1>{t('title')}</h1>
```

---

## 🔗 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Frontend Storybook**: (TODO: Phase 3)
- **Database Schema**: `auramax-core/docs/DATABASE_SCHEMA.md`
- **Permission Matrix**: `auramax-web/src/lib/permissions.ts`
- **Test Accounts**: `docs/TEST_ACCOUNTS.md`

---

## 🆘 Troubleshooting

### Problem: "Permission denied" errors

**Solution**: Check:
1. User has correct role in `MOCK_USERS`
2. Endpoint uses `require_roles()` with correct roles
3. Frontend `allowedRoles` matches backend

### Problem: Rate limiting errors

**Solution**:
- Development: Restart server to reset limits
- Production: Check Redis connection

### Problem: i18n keys not found

**Solution**:
1. Add keys to both `en.json` and `zh.json`
2. Restart Next.js dev server

---

**Last Updated**: 2026-01-20  
**Maintained By**: AuraMax Development Team
