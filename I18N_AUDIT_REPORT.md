# 🌐 i18n Audit Report

**Date**: 2026-01-20
**Auditor**: Code Quality Specialist (Acting i18n Lead)
**Scope**: New feature pages created in Session 2

---

## 🚨 Critical Findings: Hardcoded Strings

The following files contain user-facing text that is HARDCODED in English and NOT using the translation system. This violates the system's internationalization requirements.

### 1. Molecular Analysis Module
**File**: `src/app/dashboard/pharma/molecular/page.tsx`
- [ ] Title: "Molecular Descriptor Analysis"
- [ ] Labels: "SMILES", "Molecular Weight", "LogP", "H-Bond Donors"
- [ ] Buttons: "Calculate", "Export"
- [ ] Warnings: "Invalid SMILES"

**File**: `src/app/dashboard/pharma/molecular/similarity/page.tsx`
- [ ] Title: "Similarity Search"
- [ ] Labels: "Query Molecule", "Fingerprint Type", "Threshold"
- [ ] dropdown options: "Morgan", "MACCS"

**File**: `src/app/dashboard/pharma/molecular/library/page.tsx`
- [ ] Title: "Molecular Library"
- [ ] Collections: "Favorites", "Screening"

### 2. GRADE Module
**File**: `src/app/dashboard/clinical/grade/page.tsx`
- [ ] Title: "GRADE Evidence Assessment"
- [ ] Form Labels: "Risk of Bias", "Inconsistency", "Indirectness"
- [ ] Help text and tooltips

**File**: `src/app/dashboard/clinical/grade/batch/page.tsx`
- [ ] Title: "Batch GRADE Assessment"
- [ ] Table headers: "Study", "Grade", "Quality"

### 3. Data Asset Module
**File**: `src/app/dashboard/admin/data-assets/reports/page.tsx`
- [ ] Template names: "Comprehensive Data Asset Report"
- [ ] Descriptions

**File**: `src/app/dashboard/admin/data-assets/quality/page.tsx`
- [ ] Dashboard titles: "System Health Overview"
- [ ] Metric labels: "Completeness", "Accuracy"

### 4. Home Page
**File**: `src/app/page.tsx`
- [ ] Greeting: "Good morning/afternoon" linked to hardcoded English
- [ ] Module descriptions

---

## 🛠️ Remediation Plan

1.  **Extract Strings**: Move all identified strings to `messages/en.json` and `messages/zh.json`.
2.  **Define Namespaces**:
    - `molecular`: For Pharma tools
    - `grade`: For Clinical tools
    - `dataAssets`: For Admin tools
    - `home`: For the new dashboard
3.  **Refactor Code**: Replace strings with `const t = useTranslations('namespace')`.
4.  **Verify**: Ensure language switching works instantly.

---

**Severity**: **HIGH**
**Recommendation**: **BLOCK** release until fixed.
