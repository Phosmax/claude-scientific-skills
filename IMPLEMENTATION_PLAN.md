# AuraMax "Resuscitation" Implementation Plan

This plan is based on the "Code Roaster" audit and follows a strict **Plan -> Execute -> Audit -> Fix** cycle.

## Phase 1: Data Integrity & Compliance ("Stop the Bleeding")

### Step 1.1: Fix Ghost Reports
- **Goal**: Ensure generated reports are actually stored in the database.
- **Action**:
    - Update `models.py` to add `content` (JSON) column to `Report`.
    - Update `reporting_service.py` to save the generated JSON into this column.
- **Audit Target**: `reporting_service.py`, `models.py`

### Step 1.2: HIPAA Read Access Auditing
- **Goal**: Log every read access to patient data, not just write operations.
- **Action**:
    - Update `routers/patients.py` to inject `AuditService` (or log logic) into `get_patient`.
    - Ensure `VIEW_PATIENT` action is logged with user ID, IP, and patient ID.
- **Audit Target**: `routers/patients.py`

## Phase 2: Architecture Decoupling ("Orthodontics")

### Step 2.1: Dependency Injection for Services
- **Goal**: Remove hardcoded service instantiation inside other services.
- **Action**:
    - Refactor `ReportingService.__init__` to accept `pgx_service`, `wearable_service`, etc.
    - Update `routers/reports.py` (or wherever it's called) to assemble dependencies.
- **Audit Target**: `services/reporting_service.py`, `routers/reports.py` (if exists) or caller.

### Step 2.2: Async Background Tasks
- **Goal**: Prevent logging/notifications from blocking the main thread.
- **Action**:
    - Use FastAPI `BackgroundTasks` for audit logging and email notifications in `routers/auth.py` and `routers/patients.py`.
- **Audit Target**: `routers/auth.py`, `routers/patients.py`

## Phase 3: Realism ("Eliminate the Mocks")

### Step 3.1: Replace Hardcoded Logic with Knowledge Base
- **Goal**: Remove `if drug == 'warfarin'` checks.
- **Action**:
    - Create a small JSON/Dict based "Knowledge Base" for Pharmacogenomics in `pharmacogenomics.py`.
    - logic should query this KB genericly.
- **Audit Target**: `services/pharmacogenomics.py`
