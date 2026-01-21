---
description: AuraMax Internal Core Skills Integration Plan
---

# AuraMax Internal Core Skills Integration Workflow

This workflow focuses on integrating high-value "Internal Skills" (Bio-Age, PPRL, Survival Analysis) into the frontend dashboards, which were identified as missing in the strategic alignment audit.

## Phase 1: Bio-Age Calculator Integration (Clinical Dashboard)
**Goal**: Allow clinicians to calculate biological age vs chronological age for patients.

1. **Backend Verification**:
   - Check `auramax-core/src/auramax_api/services/bio_age.py`.
   - Ensure a Router endpoint exists (e.g., `POST /api/v1/bio-age/calculate`) exposing this service.
   - If not, create `auramax-core/src/auramax_api/routers/bio_age.py`.

2. **Frontend Implementation**:
   - Create `src/components/clinical/BioAgeCalculator.tsx`.
   - Inputs: Chronological Age, Biomarkers (Albumin, Creatinine, Glucose, CRP, etc.).
   - Visuals: Gauge chart showing Age Gap (Bio Age - Chrono Age).
   - Integrate into `/dashboard/clinical/page.tsx` as a new tab or widget.

3. **Audit**:
   - Run `audit-department` on the new component and API endpoint.

## Phase 2: Survival Analysis Integration (Research Dashboard)
**Goal**: Allow researchers to visualize survival curves (Kaplan-Meier) for cohorts.

1. **Backend Verification**:
   - Check `auramax_analysis` or `EndToEndTrialAnalysis` workflow availability.
   - Ensure API accepts CSV uploads or Dataset IDs for analysis.

2. **Frontend Implementation**:
   - Refactor `src/components/clinical/ClinicalAnalyst.tsx` to be more modular.
   - Rename/Move to `src/components/research/SurvivalAnalyst.tsx` if appropriate.
   - Integrate into `/dashboard/clinical/research/page.tsx`.

3. **Audit**:
   - Validate input sanitization and error handling.

## Phase 3: Secure Data Linkage (PPRL) (Data Dashboard)
**Goal**: Allow Admins to configure privacy-preserving record linkage.

1. **Backend Verification**:
   - Check `auramax-core/src/auramax_api/routers/privacy.py`.
   - Ensure endpoints for hashing/bloom filter creation exist.

2. **Frontend Implementation**:
   - Create `src/components/admin/data/PPRLConfigurator.tsx`.
   - Visuals: Visual flow of "Hashing -> Salt -> Linkage".
   - Integrate into `/dashboard/admin/data-assets/privacy`.

3. **Audit**:
   - STRICT Security Audit (PII handling).

---

## Execution Log

| Date | Phase | Status | Notes |
|------|-------|--------|-------|
| 2026-01-20 | 1. Bio-Age | Pending | Starting now. |
