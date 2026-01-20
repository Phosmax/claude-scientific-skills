import { test, expect } from '@playwright/test';

test.describe('Admin Dashboard - Public Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/admin');
  });

  test('should load admin page without crash', async ({ page }) => {
    await expect(page).toHaveTitle(/AuraMax|Admin/);
  });

  test('should display AuraMax branding', async ({ page }) => {
    await expect(page.locator('text=AuraMax').first()).toBeVisible({ timeout: 10000 });
  });

  test('should handle access to restricted routes', async ({ page }) => {
    await page.goto('http://localhost:3000/admin/dashboard');
    await expect(page).toHaveTitle(/AuraMax|Admin|登录|Login/i, { timeout: 10000 });
  });

  test('should load without critical JavaScript errors', async ({ page }) => {
    const errors: string[] = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    await page.goto('http://localhost:3000/admin');
    await page.waitForLoadState('networkidle');
    
    const criticalErrors = errors.filter(e => 
      !e.includes('favicon') && 
      !e.includes('404') &&
      !e.includes('hydration') &&
      !e.includes('MISSING_MESSAGE') &&
      !e.includes('IntlError')
    );
    
    expect(criticalErrors).toHaveLength(0);
  });
});
