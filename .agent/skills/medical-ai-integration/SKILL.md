---
name: medical-ai-integration
description: Architecture & Best Practices for AuraMax Clinical Co-Pilot (CoT & Hybrid AI)
---

# Clinical Co-Pilot Integration Guide

This skill documents the architecture, design patterns, and best practices for the AuraMax Clinical Co-Pilot system, integrating collaborative AI reasoning with structured clinical workflows.

## 1. Architecture Overview (The "Clean Store" Pattern)

To avoid "God Object" state stores, we strictly separate State Management from Clinical Decision Logic.

### 1.1 Store Layer (`consultationStore.ts`)
*   **Responsibility**: Holds `messages`, `stage`, `probabilities`, and `UI` state.
*   **Anti-Pattern**: Do NOT write complex `switch-case` medical logic directly here.
*   **Pattern**: Delegate action handling to pure logic functions.

```typescript
// INSTEAD OF:
runCoughScenario: (action) => { switch(action) { ... 100 lines ... } }

// USE:
import { handleCoughLogic } from './logic/coughScenario';
runCoughScenario: (action) => handleCoughLogic(action, get().suggestedQuestions, { ...actions })
```

### 1.2 Logic Layer (`stores/logic/*.ts`)
*   **Responsibility**: Pure functions that take `(action, currentContext)` and return/execute specific state updates.
*   **Benefit**: Unit testable, scalable to 100+ diseases without bloating the main store.

## 2. Design Patterns

### 2.1 Chain-of-Questions (Dynamic Replenishment)
**Problem**: Static question lists run out quickly, ending user engagement.
**Solution**: Implement a "Replenishment" logic where answering one question unlocks the next relevant one.

*   **Logic**: "If User answers 'Duration', remove 'Duration' AND push 'Severity' if not present."
*   **Result**: Endless, adaptive questioning flow mimicking a real doctor.

### 2.2 Hybrid AI Engine
The system uses a two-tier verification system:
1.  **Tier 1 (Instant)**: Frontend Rule-Based Logic (in `logic/*.ts`) for immediate UI feedback (e.g., changing probabilities based on keywords like "Smoke").
2.  **Tier 2 (Deep)**: Backend LLM (NVIDIA NIM/Llama-3) for comprehensive summary and differential diagnosis generation at the end of the session.

## 3. Observation & Evidence System

### 3.1 Observation Routing
We map abstract Observation IDs (`obs1`, `obs2`) to semantic actions (`observation_flushed`, `observation_wheeze`).

*   **Rule**: `completeObservation(taskId)` MUST route to a specific Scenario Handler.
*   **Check**: Always ensure every `taskId` defined in `observationTasks` has a corresponding `case` in the Logic Handler.

### 3.2 Evidence Simulation (Mocking)
For demos, we simulate external device integration (e.g., Blood Lab, OCR) using `setTimeout` + `System Messages`.
*   **UX**: Show "Uploading..." -> "OCR Complete" -> "Data Extracted" to build trust.
*   **Data**: Explicitly update clinical probabilities based on the "mocked" result (e.g., High WBC -> Boost Bacterial Pneumonia).

## 4. Interfaces & Data Models

### 4.1 Diagnosis Request (Backend Validated)
```json
{
  "chief_complaint": "string",
  "history": ["DOCTOR: note", "PATIENT: response"],
  "observations": [{"label": "Wheezing", "result": "Positive"}]
}
```

## 5. Privacy & Compliance
*   **PII Stripping**: Never send Patient Name/ID to the AI Node.
*   **Local Processing**: Tier 1 logic happens entirely in the browser (Client-Side), ensuring zero latency and high privacy for initial triage.
