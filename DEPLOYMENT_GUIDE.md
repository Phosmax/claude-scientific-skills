# AuraMax RBAC Dashboard - Deployment Guide

**Version**: 2.0  
**Last Updated**: 2026-01-20  
**Environment**: Production-Ready with Phase 2.2 Enhancements

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Setup](#database-setup)
6. [RBAC Configuration](#rbac-configuration)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Checklist](#security-checklist)
9. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum Specifications

**Backend Server**:
- CPU: 4 cores
- RAM: 8 GB
- Storage: 50 GB SSD
- OS: Ubuntu 22.04 LTS / RHEL 8+

**Frontend Server**:
- CPU: 2 cores
- RAM: 4 GB
- Storage: 20 GB SSD

**Database Server**:
- CPU: 4 cores
- RAM: 16 GB
- Storage: 200 GB SSD (RAID 10 recommended)

**Cache Server** (Redis):
- CPU: 2 cores
- RAM: 4 GB
- Storage: 10 GB

### Software Requirements

- Python 3.11+
- Node.js 18 LTS
- PostgreSQL 14+
- Redis 7+
- Nginx 1.22+ (or similar reverse proxy)
- Let's Encrypt (for SSL certificates)

---

## 🏗️ Infrastructure Setup

### Architecture Overview

```
                    ┌──────────────┐
                    │  CloudFlare  │ (Optional CDN)
                    │  /Let'sEncrypt│
                    └──────▲───────┘
                           │
                    ┌──────▼───────┐
                    │    Nginx     │ (Reverse Proxy + SSL)
                    │   Port 443   │
                    └──────▲───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼─────┐  ┌────▼────┐   ┌────▼─────┐
      │  Next.js  │  │ FastAPI │   │  Redis   │
      │  Port 3000│  │Port 8000│   │ Port 6379│
      └───────────┘  └────▲────┘   └──────────┘
                          │
                    ┌─────▼─────┐
                    │PostgreSQL │
                    │ Port 5432 │
                    └───────────┘
```

### Network Configuration

**Firewall Rules**:
```bash
# Allow SSH (change port for security)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Internal services (block external access)
sudo ufw deny 3000/tcp  # Next.js (only access via Nginx)
sudo ufw deny 8000/tcp  # FastAPI (only access via Nginx)
sudo ufw deny 5432/tcp  # PostgreSQL (only from app server)
sudo ufw deny 6379/tcp  # Redis (only from app server)

# Enable firewall
sudo ufw enable
```

---

## 🔧 Backend Deployment

### Step 1: System Setup

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# 3. Install system dependencies
sudo apt install build-essential libpq-dev redis-server nginx -y

# 4. Create deployment user
sudo useradd -m -s /bin/bash auramax
sudo usermod -aG sudo auramax
```

### Step 2: Application Deployment

```bash
# 1. Switch to app user
sudo su - auramax

# 2. Clone repository
git clone https://github.com/auramax/auramax-rbac.git
cd auramax-rbac/auramax-core

# 3. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

### Step 3: Environment Configuration

Create `/home/auramax/auramax-rbac/auramax-core/.env`:

```bash
# ========================================
# PRODUCTION ENVIRONMENT CONFIGURATION
# ========================================

# Application
APP_ENV=production
APP_NAME=AuraMax RBAC API
APP_VERSION=0.2.0

# Security
JWT_SECRET=<CHANGE_THIS_TO_RANDOM_64_CHAR_STRING>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS (Update with your frontend domain)
CORS_ALLOWED_ORIGINS=https://dashboard.auramax.ai

# Database
DATABASE_URL=postgresql://auramax:STRONG_PASSWORD@localhost:5432/auramax_prod
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# Redis (Rate Limiting & Caching)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=REDIS_STRONG_PASSWORD

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/auramax/api.log

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_STORAGE_URL=redis://localhost:6379/1

# Email (for notifications, optional)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=<SENDGRID_API_KEY>
SMTP_FROM=noreply@auramax.ai

# Feature Flags
ENABLE_MOCK_USERS=false  # IMPORTANT: Disable in production!
ENABLE_SWAGGER_UI=false  # Disable /docs in production
```

**Generate strong JWT secret:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

### Step 4: Database Migration

```bash
# Run migrations
cd /home/auramax/auramax-rbac/auramax-core
source venv/bin/activate
alembic upgrade head
```

### Step 5: Systemd Service

Create `/etc/systemd/system/auramax-api.service`:

```ini
[Unit]
Description=AuraMax RBAC API
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=auramax
Group=auramax
WorkingDirectory=/home/auramax/auramax-rbac/auramax-core
Environment="PATH=/home/auramax/auramax-rbac/auramax-core/venv/bin"
ExecStart=/home/auramax/auramax-rbac/auramax-core/venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 4 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/auramax/api-access.log \
    --error-logfile /var/log/auramax/api-error.log \
    auramax_api.main:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable auramax-api
sudo systemctl start auramax-api
sudo systemctl status auramax-api
```

---

## 🎨 Frontend Deployment

### Step 1: Build Frontend

```bash
# On build server or CI/CD
cd auramax-rbac/auramax-web

# Install dependencies
npm ci

# Create production build
npm run build

# Test build locally
npm run start
```

### Step 2: Deploy with PM2

```bash
# Install PM2
npm install -g pm2

# Start application
cd /home/auramax/auramax-rbac/auramax-web
pm2 start npm --name "auramax-web" -- start

# Configure PM2 to start on boot
pm2 startup
pm2 save
```

### Step 3: Environment Configuration

Create `/home/auramax/auramax-rbac/auramax-web/.env.production`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://api.auramax.ai
NEXT_PUBLIC_APP_URL=https://dashboard.auramax.ai

# Analytics (optional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

---

## 🗄️ Database Setup

### PostgreSQL Installation

```bash
# Install PostgreSQL 14
sudo apt install postgresql-14 postgresql-contrib-14

# Start service
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### Database Initialization

```bash
# Switch to postgres user
sudo -u postgres psql

-- Create database and user
CREATE DATABASE auramax_prod;
CREATE USER auramax WITH ENCRYPTED PASSWORD 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON DATABASE auramax_prod TO auramax;

-- Enable extensions
\c auramax_prod
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

\q
```

### PostgreSQL Configuration

Edit `/etc/postgresql/14/main/postgresql.conf`:

```ini
# Memory Settings
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
work_mem = 64MB

# Connection Settings
max_connections = 200

# Write-Ahead Log
wal_level = replica
max_wal_size = 2GB

# Query Planning
random_page_cost = 1.1  # For SSD
```

Edit `/etc/postgresql/14/main/pg_hba.conf`:

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   all             auramax                                 md5
host    auramax_prod    auramax         127.0.0.1/32           md5
```

**Restart PostgreSQL:**
```bash
sudo systemctl restart postgresql
```

### Backup Configuration

Create `/home/auramax/scripts/backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/auramax"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/auramax_prod_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

# Backup with compression
pg_dump -U auramax auramax_prod | gzip > $BACKUP_FILE

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
```

**Schedule with cron:**
```bash
# Daily backup at 2 AM
0 2 * * * /home/auramax/scripts/backup_db.sh
```

---

## 🔐 RBAC Configuration

### Production User Management

**IMPORTANT**: Disable `MOCK_USERS` in production!

Edit `auramax-core/src/auramax_api/main.py`:

```python
# In production, set:
if APP_ENV == "production":
    MOCK_USERS = {}  # Disable mock users
```

### Database-Backed User System

Create `users` table (via migration):

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    roles TEXT[] NOT NULL,
    tier VARCHAR(50) DEFAULT 'free',
    organization_id VARCHAR(100),
    organization_type VARCHAR(50),
    organization_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_org ON users(organization_id);
```

### Permission Matrix Deployment

The permission matrix is defined in:
- Backend: `auramax-core/src/auramax_api/auth/filters.py` (`CROSS_ORG_ROLES`)
- Frontend: `auramax-web/src/lib/permissions.ts` (`API_PERMISSIONS`)

**Sync these files** across deployments!

### Create Admin User

```python
# Run this script once to create first admin
from auramax_api.database.config import async_session
from auramax_api.database.models import User
import bcrypt
import asyncio

async def create_admin():
    async with async_session() as session:
        password_hash = bcrypt.hashpw(
            "SECURE_PASSWORD".encode(),
            bcrypt.gensalt()
        ).decode()
        
        admin = User(
            email="admin@yourcompany.com",
            password_hash=password_hash,
            full_name="System Administrator",
            roles=["user", "super_admin"],
            tier="enterprise",
            organization_type="Platform",
            organization_name="AuraMax Platform",
            is_verified=True
        )
        
        session.add(admin)
        await session.commit()
        print("Admin user created!")

asyncio.run(create_admin())
```

---

## 📊 Monitoring & Logging

### Redis Setup

```bash
# Install Redis
sudo apt install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
```

**Important settings:**
```ini
# Bind to localhost only
bind 127.0.0.1

# Set password
requirepass REDIS_STRONG_PASSWORD

# Memory limit
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
```

**Restart Redis:**
```bash
sudo systemctl restart redis
sudo systemctl enable redis
```

### ELK Stack (Elasticsearch, Logstash, Kibana)

#### 1. Install Elasticsearch

```bash
# Add Elastic repo
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

sudo apt update
sudo apt install elasticsearch

# Start service
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
```

#### 2. Install Logstash

```bash
sudo apt install logstash

# Create config
sudo nano /etc/logstash/conf.d/auramax.conf
```

**Logstash config:**
```ruby
input {
  file {
    path => "/var/log/auramax/api.log"
    start_position => "beginning"
    codec => "json"
  }
}

filter {
  json {
    source => "message"
  }
  
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "auramax-logs-%{+YYYY.MM.dd}"
  }
}
```

**Start Logstash:**
```bash
sudo systemctl enable logstash
sudo systemctl start logstash
```

#### 3. Install Kibana

```bash
sudo apt install kibana

# Configure
sudo nano /etc/kibana/kibana.yml
```

**Kibana config:**
```yaml
server.port: 5601
server.host: "localhost"
elasticsearch.hosts: ["http://localhost:9200"]
```

**Start Kibana:**
```bash
sudo systemctl enable kibana
sudo systemctl start kibana
```

### Monitoring Dashboard

Access Kibana at `http://localhost:5601` (via SSH tunnel or Nginx proxy)

**Create Index Pattern**: `auramax-logs-*`

**Useful Queries:**
```
# Failed login attempts
level:"WARNING" AND message:"Invalid credentials"

# Rate limit violations  
status:429

# Cross-org access attempts
message:"无权访问其他组织"

# Slow API calls
duration_ms:>5000

# Admin actions
user_roles:"super_admin" AND action:"DELETE"
```

---

## 🔒 Security Checklist

### Pre-Deployment

- [ ] Change all default passwords
- [ ] Generate strong JWT secret (64+ characters)
- [ ] Disable `MOCK_USERS` in production
- [ ] Disable Swagger UI (`/docs`) in production
- [ ] Configure CORS with specific origins (no wildcards)
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up firewall rules
- [ ] Configure Redis password
- [ ] Restrict database access to localhost
- [ ] Enable rate limiting with Redis backend
- [ ] Configure log rotation

### Post-Deployment

- [ ] Run security audit (see below)
- [ ] Test rate limiting
- [ ] Verify audit logs are working
- [ ] Test backup restoration
- [ ] Configure monitoring alerts
- [ ] Document all credentials in secure vault

### Security Audit Script

```bash
#!/bin/bash
echo "=== AuraMax Security Audit ==="

# 1. Check JWT secret
if grep -q "INSECURE" .env; then
    echo "❌ FAIL: Using insecure JWT secret!"
else
    echo "✅ PASS: JWT secret configured"
fi

# 2. Check mock users
if grep -q "ENABLE_MOCK_USERS=true" .env; then
    echo "❌ FAIL: Mock users enabled in production!"
else
    echo "✅ PASS: Mock users disabled"
fi

# 3. Check CORS
if grep -q "CORS_ALLOWED_ORIGINS=\*" .env; then
    echo "❌ FAIL: CORS allows all origins!"
else
    echo "✅ PASS: CORS properly configured"
fi

# 4. Check HTTPS
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "⚠️  WARNING: API accessible via HTTP"
else
    echo "✅ PASS: HTTPS enforced"
fi

# 5. Check rate limiting
if [ -f "/var/log/auramax/api.log" ]; then
    echo "✅ PASS: Logging configured"
else
    echo "❌ FAIL: Log file not found"
fi
```

---

## 🌐 Nginx Configuration

Create `/etc/nginx/sites-available/auramax`:

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=web_limit:10m rate=200r/m;

# Upstream servers
upstream auramax_api {
    server 127.0.0.1:8000 fail_timeout=10s max_fails=3;
}

upstream auramax_web {
    server 127.0.0.1:3000 fail_timeout=10s max_fails=3;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name dashboard.auramax.ai api.auramax.ai;
    return 301 https://$host$request_uri;
}

# API Server
server {
    listen 443 ssl http2;
    server_name api.auramax.ai;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.auramax.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.auramax.ai/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    
    # Rate Limiting
    limit_req zone=api_limit burst=20 nodelay;
    
    # Proxy to FastAPI
    location / {
        proxy_pass http://auramax_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Access logs
    access_log /var/log/nginx/api-access.log;
    error_log /var/log/nginx/api-error.log;
}

# Web Server
server {
    listen 443 ssl http2;
    server_name dashboard.auramax.ai;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/dashboard.auramax.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dashboard.auramax.ai/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;
    
    # Rate Limiting
    limit_req zone=web_limit burst=50 nodelay;
    
    # Proxy to Next.js
    location / {
        proxy_pass http://auramax_web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (for Next.js HMR in dev)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Access logs
    access_log /var/log/nginx/web-access.log;
    error_log /var/log/nginx/web-error.log;
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/auramax /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🚨 Troubleshooting

### API Not Starting

```bash
# Check logs
sudo journalctl -u auramax-api -n 100 --no-pager

# Check if port is in use
sudo lsof -i :8000

# Test manual start
cd /home/auramax/auramax-rbac/auramax-core
source venv/bin/activate
uvicorn auramax_api.main:app --host 0.0.0.0 --port 8000
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U auramax -d auramax_prod -h localhost

# Check connection limits
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

### Redis Issues

```bash
# Check Redis status
sudo systemctl status redis

# Test connection
redis-cli -a REDIS_PASSWORD ping

# Check memory usage
redis-cli -a REDIS_PASSWORD INFO memory
```

### High Memory Usage

```bash
# Check process memory
ps aux --sort=-%mem | head -10

# Restart services
sudo systemctl restart auramax-api
pm2 restart auramax-web
```

---

## 📚 Additional Resources

- **API Documentation**: https://api.auramax.ai/redoc
- **Health Check**: https://api.auramax.ai/health
- **Monitoring**: Kibana dashboard
- **Support**: support@auramax.ai

---

**Last Updated**: 2026-01-20  
**Maintained By**: AuraMax DevOps Team
