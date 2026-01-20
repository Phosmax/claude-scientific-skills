# AuraMax 生产环境部署指南

**版本**: 1.0  
**日期**: 2026-01-19  
**状态**: ✅ 生产就绪

---

## 📋 概述

本文档提供AuraMax系统（前端 + 后端）在生产环境部署的完整指南。

### 系统架构

```
                    ┌─────────────────┐
                    │   CloudFlare    │
                    │   (CDN/WAF)     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                              │
     ┌────────▼────────┐          ┌─────────▼─────────┐
     │   Vercel        │          │  Cloud Server     │
     │  (Frontend)     │          │  (Backend)        │
     │                 │          │                   │
     │  Next.js 15     │   ──►    │  FastAPI          │
     │  auramax.com    │          │  api.auramax.com  │
     └─────────────────┘          └─────────┬─────────┘
                                            │
                          ┌─────────────────┴─────────────────┐
                          │                                    │
               ┌──────────▼──────────┐            ┌────────────▼────────────┐
               │   PostgreSQL 16     │            │      Redis 7            │
               │   (Primary DB)      │            │   (Cache/Session)       │
               └─────────────────────┘            └─────────────────────────┘
```

---

## 🚀 快速开始

### 前置条件

| 组件 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Node.js | 18.x | 20.x |
| Python | 3.10 | 3.11 |
| Docker | 20.x | 24.x |
| PostgreSQL | 15 | 16 |
| Redis | 6 | 7 |

### 环境变量

#### 前端 (auramax-web)

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.auramax.com
NEXT_PUBLIC_APP_URL=https://auramax.com
NEXT_TELEMETRY_DISABLED=1
```

#### 后端 (auramax-core)

```bash
# .env.production
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@db-host:5432/auramax
POSTGRES_USER=auramax_prod
POSTGRES_PASSWORD=<STRONG_PASSWORD>
POSTGRES_DB=auramax

# Redis
REDIS_URL=redis://redis-host:6379/0

# Security (CRITICAL - Use strong values)
JWT_SECRET=<RANDOM_64_CHAR_STRING>
ENCRYPTION_KEY=<FERNET_KEY_BASE64>

# API
API_HOST=0.0.0.0
API_PORT=8000

# External Services (Optional)
OPENAI_API_KEY=<YOUR_KEY>
NVIDIA_API_KEY=<YOUR_KEY>
```

---

## 🐳 Docker 部署

### 方式1: Docker Compose (推荐)

```bash
# 1. 克隆代码
git clone https://github.com/your-org/auramax.git
cd auramax/auramax-core

# 2. 创建生产环境配置
cp .env.example .env.production
vim .env.production  # 编辑配置

# 3. 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 4. 验证服务状态
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health
```

### 方式2: 独立Docker镜像

```bash
# 构建后端镜像
cd auramax-core
docker build -t auramax-api:latest .

# 构建前端镜像
cd auramax-web
docker build -t auramax-web:latest .

# 运行后端
docker run -d \
  --name auramax-api \
  -p 8000:8000 \
  --env-file .env.production \
  auramax-api:latest

# 运行前端
docker run -d \
  --name auramax-web \
  -p 3000:3000 \
  auramax-web:latest
```

---

## ☁️ 云服务部署

### Vercel (前端)

1. **连接仓库**
   - 登录 Vercel Dashboard
   - Import Project → 选择 auramax-web 目录

2. **配置环境变量**
   ```
   NEXT_PUBLIC_API_URL = https://api.auramax.com
   ```

3. **部署设置**
   ```
   Framework Preset: Next.js
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm ci
   ```

### AWS / Azure / GCP (后端)

#### AWS ECS 部署

```bash
# 1. 推送镜像到ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag auramax-api:latest <account>.dkr.ecr.<region>.amazonaws.com/auramax-api:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/auramax-api:latest

# 2. 更新ECS服务
aws ecs update-service --cluster auramax-prod --service auramax-api --force-new-deployment
```

---

## 🔒 安全配置

### HTTPS/TLS

使用 Let's Encrypt 或云服务商证书：

```nginx
# nginx.conf (SSL部分)
server {
    listen 443 ssl http2;
    server_name api.auramax.com;
    
    ssl_certificate /etc/letsencrypt/live/api.auramax.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.auramax.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### CORS 配置

后端已配置正确的CORS策略：

```python
# 生产环境仅允许特定域名
CORS_ORIGINS = [
    "https://auramax.com",
    "https://www.auramax.com",
]
```

### 安全检查清单

- [x] HTTPS 强制启用
- [x] JWT Token 过期时间合理 (1h access, 7d refresh)
- [x] 密码强度要求
- [x] SQL注入防护 (ORM)
- [x] XSS防护 (Next.js内置)
- [x] CSRF Token
- [x] Rate Limiting
- [x] 敏感数据加密
- [x] 日志脱敏

---

## 📊 监控与告警

### 健康检查端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 基础健康检查 |
| `/health/db` | GET | 数据库连接状态 |
| `/health/redis` | GET | Redis连接状态 |
| `/metrics` | GET | Prometheus指标 |

### 日志管理

```bash
# 查看容器日志
docker-compose -f docker-compose.prod.yml logs -f api

# 日志输出格式 (JSON)
{"timestamp": "2026-01-19T16:00:00Z", "level": "INFO", "message": "Request completed", ...}
```

### 告警配置 (Prometheus + Alertmanager)

```yaml
# alerts.yml
groups:
  - name: auramax-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "高错误率告警"
```

---

## 🔄 CI/CD 流程

### GitHub Actions 工作流

已配置完整的CI/CD流程 (`.github/workflows/ci.yml`)：

```
触发条件:
├── push to main/develop
└── pull_request to main/develop

Job流程:
├── frontend-test (Lint + Type + Unit)
├── backend-test (Ruff + Mypy + Pytest)
├── security-scan (npm audit + safety + bandit)
├── docker-build (构建测试)
├── e2e-test (Playwright)
├── deploy-preview (PR预览 → Vercel)
└── deploy-production (main → Vercel + Server)
```

### 部署触发

```bash
# 部署生产环境
git checkout main
git merge develop
git push origin main  # 自动触发CI/CD
```

---

## 📋 运维命令速查

### 数据库

```bash
# 备份
docker exec auramax-db pg_dump -U auramax auramax > backup_$(date +%Y%m%d).sql

# 恢复
docker exec -i auramax-db psql -U auramax auramax < backup.sql

# 迁移
docker exec auramax-api alembic upgrade head
```

### 服务管理

```bash
# 重启服务
docker-compose -f docker-compose.prod.yml restart api

# 查看资源使用
docker stats

# 清理无用镜像
docker system prune -f
```

---

## 🆘 故障排查

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 502 Bad Gateway | API未启动 | 检查容器状态 |
| 数据库连接失败 | 密码错误/网络问题 | 检查环境变量和网络 |
| JWT验证失败 | 密钥不一致 | 确保前后端使用相同密钥 |
| CORS错误 | 域名未配置 | 添加域名到CORS白名单 |

### 紧急联系

- **On-Call**: ops@auramax.com
- **Slack**: #auramax-ops
- **Dashboard**: https://status.auramax.com

---

## 📚 相关文档

- [API文档](https://api.auramax.com/docs)
- [架构设计文档](./docs/ARCHITECTURE.md)
- [安全策略](./docs/SECURITY.md)
- [数据库Schema](./docs/DATABASE.md)

---

**文档维护者**: AuraMax DevOps Team  
**最后更新**: 2026-01-19
