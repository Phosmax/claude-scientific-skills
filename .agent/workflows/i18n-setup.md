---
description: 为 AuraMax 系统添加多语言国际化支持 (i18n)
---

# AuraMax 多语言支持工作流

本工作流将指导你为 AuraMax 系统添加完整的多语言支持。

## 前置准备

// turbo
1. 确保前端开发服务器正在运行
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-web
npm run dev
```

## 第一步：安装 i18n 依赖

// turbo
2. 安装 next-intl 国际化库
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-web
npm install next-intl
```

## 第二步：创建语言文件结构

3. 创建语言文件目录和翻译文件：

**目录结构：**
```
auramax-web/
├── messages/
│   ├── en.json      # 英文翻译
│   ├── zh.json      # 中文翻译
│   └── ja.json      # 日文翻译（可选）
├── src/
│   └── i18n/
│       ├── config.ts    # i18n 配置
│       └── request.ts   # 请求处理
```

4. 创建 `messages/zh.json`（中文，作为基础）：
```json
{
  "common": {
    "loading": "加载中...",
    "error": "出错了",
    "save": "保存",
    "cancel": "取消",
    "confirm": "确认",
    "delete": "删除",
    "edit": "编辑",
    "back": "返回",
    "next": "下一步",
    "submit": "提交"
  },
  "auth": {
    "login": "登录",
    "logout": "退出登录",
    "register": "注册",
    "email": "邮箱地址",
    "password": "密码",
    "forgotPassword": "忘记密码？",
    "resetPassword": "重置密码",
    "rememberMe": "记住我"
  },
  "dashboard": {
    "title": "仪表盘",
    "welcome": "欢迎回来",
    "totalAnalyses": "分析总数",
    "recentActivity": "最近活动"
  },
  "settings": {
    "title": "设置",
    "language": "语言",
    "theme": "主题",
    "notifications": "通知"
  }
}
```

5. 创建 `messages/en.json`（英文）：
```json
{
  "common": {
    "loading": "Loading...",
    "error": "Something went wrong",
    "save": "Save",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "delete": "Delete",
    "edit": "Edit",
    "back": "Back",
    "next": "Next",
    "submit": "Submit"
  },
  "auth": {
    "login": "Login",
    "logout": "Logout",
    "register": "Register",
    "email": "Email Address",
    "password": "Password",
    "forgotPassword": "Forgot password?",
    "resetPassword": "Reset Password",
    "rememberMe": "Remember me"
  },
  "dashboard": {
    "title": "Dashboard",
    "welcome": "Welcome back",
    "totalAnalyses": "Total Analyses",
    "recentActivity": "Recent Activity"
  },
  "settings": {
    "title": "Settings",
    "language": "Language",
    "theme": "Theme",
    "notifications": "Notifications"
  }
}
```

## 第三步：配置 next-intl

6. 创建 `src/i18n/config.ts`：
```typescript
export const locales = ['zh', 'en'] as const;
export const defaultLocale = 'zh' as const;

export type Locale = (typeof locales)[number];
```

7. 创建 `src/i18n/request.ts`：
```typescript
import { getRequestConfig } from 'next-intl/server';
import { cookies } from 'next/headers';
import { defaultLocale, locales, type Locale } from './config';

export default getRequestConfig(async () => {
  const cookieStore = await cookies();
  const localeCookie = cookieStore.get('locale')?.value;
  
  const locale: Locale = locales.includes(localeCookie as Locale) 
    ? (localeCookie as Locale) 
    : defaultLocale;

  return {
    locale,
    messages: (await import(`../../messages/${locale}.json`)).default,
  };
});
```

8. 更新 `next.config.ts` 添加 i18n 插件：
```typescript
import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts');

const nextConfig = {
  // 现有配置...
};

export default withNextIntl(nextConfig);
```

## 第四步：创建语言切换组件

9. 创建 `src/components/LanguageSwitcher.tsx`：
```typescript
'use client';

import { useTransition } from 'react';
import { useLocale } from 'next-intl';
import { Button } from '@/components/ui/button';
import { Globe } from 'lucide-react';

const languages = [
  { code: 'zh', name: '中文' },
  { code: 'en', name: 'English' },
];

export function LanguageSwitcher() {
  const locale = useLocale();
  const [isPending, startTransition] = useTransition();

  const handleChange = (newLocale: string) => {
    startTransition(() => {
      document.cookie = `locale=${newLocale};path=/;max-age=31536000`;
      window.location.reload();
    });
  };

  return (
    <div className="flex items-center gap-2">
      <Globe className="h-4 w-4" />
      {languages.map((lang) => (
        <Button
          key={lang.code}
          variant={locale === lang.code ? 'default' : 'ghost'}
          size="sm"
          onClick={() => handleChange(lang.code)}
          disabled={isPending}
        >
          {lang.name}
        </Button>
      ))}
    </div>
  );
}
```

## 第五步：在组件中使用翻译

10. 在页面中使用翻译：
```typescript
import { useTranslations } from 'next-intl';

export default function DashboardPage() {
  const t = useTranslations('dashboard');
  
  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('welcome')}</p>
    </div>
  );
}
```

## 第六步：添加语言切换到布局

11. 在 `(dashboard)/layout.tsx` 添加语言切换器：
```typescript
import { LanguageSwitcher } from '@/components/LanguageSwitcher';

// 在用户区域添加
<LanguageSwitcher />
```

## 验证步骤

// turbo
12. 重启开发服务器
```bash
cd /Users/franklin/Github/claude-scientific-skills/auramax-web
npm run dev
```

13. 在浏览器中测试：
   - 打开 http://localhost:3000/dashboard
   - 点击语言切换按钮
   - 确认界面文字正确切换

## 后续扩展

- 添加更多语言（日语、韩语等）
- 为后端 API 错误消息添加国际化
- 添加 RTL（从右到左）语言支持（阿拉伯语、希伯来语）
- 使用 Crowdin 或 Lokalise 进行翻译管理
