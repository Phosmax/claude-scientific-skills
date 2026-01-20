# AuraMax B2B Analytics: End-to-End Demo Walkthrough

## 1. Scenario
**User Persona**: Senior Medical Researcher at a Pharma Company.
**Goal**: Validate the efficacy of *Gefitinib* in an EGFR+ NSCLC patient cohort using Real-World Evidence (RWE).

## 2. The Journey (Dashboard Flow)

### Phase 1: Cohort Selection
*   **Action**: User logs into `/professional/analytics`.
*   **UI Interaction**: Selects "NSCLC (EGFR+)" from the Cohort Dropdown.
*   **System Action**:
    *   Frontend calls `POST /api/v1/analytics/cohorts` to define the virtual cohort based on criteria `{"condition": "NSCLC", "mutation": "EGFR"}`.
    *   Backend (Mocked for Demo) generates a synthetic cohort of ~1200 patients.

### Phase 2: Survival Analysis (Real-Time Calculation)
*   **Action**: Dashboard automatically loads the Survival Curve.
*   **UI Interaction**: User observes two curves: "Experimental (Gefitinib)" vs "Standard Care".
*   **System Action**:
    *   Frontend calls `POST /api/v1/analytics/survival`.
    *   **Backend Engine**: 
        *   Retrieves patients.
        *   Calculates Kaplan-Meier probabilities using `lifelines` logic (simulated in `SurvivalEngine`).
        *   Computes Log-Rank test (P-Value < 0.001).
    *   **Result**: The "Experimental" curve shows higher survival probability, visually separating at month 2.

### Phase 3: Evidence Synthesis (Hybrid RAG)
*   **Action**: User notices the curve separation and types "Gefitinib efficacy EGFR" in the Evidence Search bar.
*   **System Action**:
    *   Frontend calls `GET /api/v1/analytics/evidence?q=Gefitinib...`.
    *   **RAG Engine**:
        *   **Recall**: SQL query finds articles with "Gefitinib" and "EGFR".
        *   **Re-rank**: Semantic scorer boosts "High Confidence" guidelines (e.g., N Engl J Med).
    *   **Display**: Dashboard shows *Live RAG* results with "HIGH Confidence" badges.

## 3. Technical Verification
To prove the system is running "Real Science", perform the following checks:

1.  **Molecular Validity**: The system now requires RDKit. Any attempt to verify molecule `COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1` (Gefitinib) will pass through the rigorous `MolecularDescriptorCalculator`.
2.  **Graceful Degradation**: Disconnect the Backend. The Dashboard shows a "Demo Mode" badge but remains interactive using high-fidelity mock data.
