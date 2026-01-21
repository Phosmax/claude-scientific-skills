# AuraMax Architecture & Design Documentation

## 1. System Overview

AuraMax is an advanced **Clinical Intelligence Platform** designed to bridge the gap between raw medical data and actionable clinical insights. It employs a **multi-agent AI architecture** orchestrated via the Model Context Protocol (MCP) to provide role-specific dashboards for 12 distinct healthcare personas.

### Key Capabilities
*   **Clinical Reasoning**: Chain-of-Thought (CoT) inference with evidence grading (GRADE).
*   **Bio-Computation**: Genomics (VCF), Pharmacogenomics (ClinPGx), and Pathway Analysis (KEGG/Reactome).
*   **Medical Imaging**: AI-powered segmentation (NVIDIA VISTA-3D) for CT/MRI/X-Ray.
*   **Molecular Analysis**: SMILES-to-PDB structure generation and 3D visualization.
*   **Enterprise Security**: HIPAA-compliant audit logging, RBAC, and data isolation.

## 2. High-Level Architecture

```mermaid
graph TD
    User[Client / Browser] --> WAF[Web App Firewall]
    WAF --> FE[Next.js Frontend]
    
    subgraph "AuraMax Platform"
        FE --> API[FastAPI Backend Gateway]
        
        subgraph "Core Services"
            API --> Auth[Auth Service (JWT)]
            API --> Audit[Audit Service (HIPAA)]
            API --> Billing[Billing Service (Stripe)]
        end
        
        subgraph "Intelligence Layer"
            API --> Reasoning[Reasoning Engine]
            API --> BioComp[Bio-Compute Engine]
            API --> Imaging[Imaging Engine (VISTA-3D)]
            API --> Molecular[Molecular Engine (RDKit)]
        end
        
        subgraph "Data Layer"
            Auth --> DB[(PostgreSQL)]
            Audit --> DB
            BioComp --> FS[File Storage (S3/Local)]
            Imaging --> FS
        end
    end
```

## 3. Module Details

### 3.1 Molecular Analysis Engine
*   **Format Supported**: SMILES (Input) -> PDB (Output).
*   **Core Library**: RDKit (Python) for 3D embedding `ETKDGv3` and MMFF94 optimization.
*   **Visualization**:
    *   **NGL.js**: For professional PDB structure rendering (Cartoons, Surfaces).
    *   **React Three Fiber**: For lightweight ball-and-stick fallback.
*   **API Endpoint**: `POST /api/v1/molecular/structure/pdb`

### 3.2 Medical Imaging Engine (VISTA-3D)
*   **Model**: NVIDIA VISTA-3D (Foundation Model for Medical Imaging).
*   **Function**: Automatic organ segmentation and volumetry.
*   **Modes**:
    *   **Live**: Connects to NVIDIA NIM API.
    *   **Simulation**: Returns pre-computed masks for standard diverse datasets (Liver, Spleen, Kidneys).
*   **Privacy**: Images processed in memory (or temp storage), not permanently stored in basic tier.

### 3.3 Audit & Compliance System
*   **Standard**: HIPAA Security Rule (Audit Controls §164.312(b)).
*   **Implementation**:
    *   **Middleware**: Intercepts critical actions (Login, Patient View, Report Export).
    *   **Immutability**: Logs stored in append-only table structure.
    *   **Export**: Support for CSV/PDF audit trails for regulatory submission.

## 4. Technology Stack (Current)

*   **Frontend**: Next.js 14, TailwindCSS, Framer Motion, Lucide Icons, ShadcnUI.
*   **Backend**: Python 3.11, FastAPI, Pydantic 2.0.
*   **Database**: SQLite (Dev) / PostgreSQL (Planned Prod).
*   **AI/ML**: RDKit, NVIDIA NIM (Mock/Real), LangChain (Reasoning).
*   **DevOps**: Docker, GitHub Actions, uv (Package Manager).

## 5. Security Architecture

*   **Authentication**: OAuth2 with Password Flow + JWT.
*   **Authorization**: 12-Role RBAC (Super Admin, Hospital Admin, Pharma Researcher, etc.).
*   **Data Protection**:
    *   **At Rest**: Field-level encryption for PII (Planned).
    *   **In Transit**: TLS 1.3 enforced.
    *   **Audit**: Granular logs for "Break-Glass" scenarios.

## 6. Future Roadmap (System Optimization)

*   **Infrastructure**: Migration from SQLite to PostgreSQL + Redis.
*   **Performance**: Async task queues (Celery/Arq) for heavy bio-computation.
*   **Interoperability**: HL7 FHIR R4 API Refactoring.
