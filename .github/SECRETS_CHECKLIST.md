# GitHub Secrets 配置清单

**用途**: 配置 GitHub Actions CI/CD 所需的密钥  
**最后更新**: 2026-01-19

---

## 必需的 Secrets

在 GitHub 仓库设置页面 (Settings → Secrets and variables → Actions) 添加以下密钥：

### Vercel 部署

| Secret Name | 描述 | 获取方式 |
|-------------|------|----------|
| `VERCEL_TOKEN` | Vercel API Token | Vercel Dashboard → Settings → Tokens |
| `VERCEL_ORG_ID` | Vercel 组织 ID | `vercel env pull` 后查看 .vercel/project.json |
| `VERCEL_PROJECT_ID` | Vercel 项目 ID | 同上 |

### 生产服务器部署

| Secret Name | 描述 | 获取方式 |
|-------------|------|----------|
| `PROD_SERVER_HOST` | 服务器 IP 或域名 | 例: `123.45.67.89` |
| `PROD_SERVER_USER` | SSH 用户名 | 例: `deploy` |
| `PROD_SERVER_SSH_KEY` | SSH 私钥 | `cat ~/.ssh/id_rsa` (生成专用部署密钥) |

### 通知

| Secret Name | 描述 | 获取方式 |
|-------------|------|----------|
| `SLACK_WEBHOOK_URL` | Slack Webhook | Slack App → Incoming Webhooks |

### 测试覆盖率

| Secret Name | 描述 | 获取方式 |
|-------------|------|----------|
| `CODECOV_TOKEN` | Codecov 上传 Token | codecov.io → 仓库设置 |

---

## 可选的 Secrets

### 外部 API 服务

| Secret Name | 描述 | 用途 |
|-------------|------|------|
| `OPENAI_API_KEY` | OpenAI API | AI 分析功能 |
| `NVIDIA_API_KEY` | NVIDIA NIM API | 医学影像分析 |
| `SENDGRID_API_KEY` | SendGrid API | 邮件发送 |

---

## 配置示例

### 生成 SSH 部署密钥

```bash
# 在本地生成专用部署密钥 (不要使用已有密钥)
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_deploy_key

# 将公钥添加到服务器
ssh-copy-id -i ~/.ssh/github_deploy_key.pub deploy@your-server.com

# 将私钥内容复制到 GitHub Secret
cat ~/.ssh/github_deploy_key
# 复制输出内容并添加到 PROD_SERVER_SSH_KEY
```

### Vercel CLI 获取项目信息

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录并链接项目
cd auramax-web
vercel link

# 查看项目信息
cat .vercel/project.json
# 输出类似:
# {
#   "projectId": "prj_xxxxxxxxxxxxx",   <- VERCEL_PROJECT_ID
#   "orgId": "team_xxxxxxxxxx"          <- VERCEL_ORG_ID
# }
```

---

## Repository Variables (可选)

除了 Secrets，还可以配置 Variables (非敏感信息):

| Variable Name | 值 | 描述 |
|---------------|-----|------|
| `NODE_VERSION` | `20.x` | Node.js 版本 |
| `PYTHON_VERSION` | `3.11` | Python 版本 |
| `PROD_DOMAIN` | `auramax.com` | 生产环境域名 |

---

## 验证配置

配置完成后，可以手动触发一次 CI/CD 测试：

```bash
# 创建一个空提交来触发 CI
git commit --allow-empty -m "chore: trigger CI test"
git push origin main
```

然后在 GitHub Actions 页面查看运行结果。

---

## 安全注意事项

1. **永远不要在代码中硬编码密钥**
2. **定期轮换敏感密钥** (每90天)
3. **使用最小权限原则** - 只给必要的权限
4. **部署密钥应只读** - 不应有写入仓库权限
5. **生产数据库密码** - 使用强密码 (32+字符)

---

**配置完成检查**:

- [ ] VERCEL_TOKEN
- [ ] VERCEL_ORG_ID
- [ ] VERCEL_PROJECT_ID
- [ ] PROD_SERVER_HOST
- [ ] PROD_SERVER_USER
- [ ] PROD_SERVER_SSH_KEY
- [ ] SLACK_WEBHOOK_URL (可选)
- [ ] CODECOV_TOKEN (可选)
