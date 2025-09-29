# SentinelFlow

**SentinelFlow** is a microservices-based platform for **policy-aware AI orchestration**.  
It demonstrates how governance, risk, and compliance (GRC) controls (e.g., Purview-style policies, AIMS enforcement) can be integrated directly into AI service pipelines, with full observability and evidence tracking.

---

## ✨ Features
- **Gateway** → Entry point, routes requests and enforces decisions  
- **PEP** → Policy Enforcement Point, delegates to PDP  
- **AIMS (PDP)** → Policy Decision Point, evaluates rules & logs evidence  
- **RAG Service** → Adds retrieval-augmented context before inference  
- **Tools Service** → Stub for external APIs/tools  
- **Models Service** → Simple hosted model stub (echo + context)  
- **Audit/Evidence** → Evidence store via AIMS (`/v1/evidence`)

---

## 🗂️ Architecture

```mermaid
flowchart TB
  subgraph User["User & Apps"]
    A1[Microsoft 365]
    A2[Teams]
    A3[SharePoint]
    A4[LOB Apps]
  end

  subgraph Gateway["Gateway Service"]
    G1[/Route API/]
  end

  subgraph PEP["Policy Enforcement Point"]
    PEP1[/Decide/]
  end

  subgraph AIMS["AI Management System (PDP)"]
    AIM1[Rules]
    AIM2[Risk Register]
    AIM3[Evidence Store]
  end

  subgraph Runtime["Runtime Services"]
    RAG[RAG Service]
    TOOLS[Tools Broker]
    MODELS[Model Service]
  end

  A1 --> G1
  A2 --> G1
  A3 --> G1
  A4 --> G1

  G1 --> PEP1
  PEP1 --> AIM1
  AIM1 --> AIM3
  PEP1 -->|allow| RAG
  PEP1 -->|deny| AIM3

  RAG --> TOOLS
  TOOLS --> MODELS
  MODELS --> G1
```
## ✨ Features
- **Gateway** → Entry point, routes requests and enforces decisions  
- **PEP** → Policy Enforcement Point, delegates to PDP  
- **AIMS (PDP)** → Policy Decision Point, evaluates rules & logs evidence  
- **RAG Service** → Adds retrieval-augmented context before inference  
- **Tools Service** → Stub for external APIs/tools  
- **Models Service** → Simple hosted model stub (echo + context)  
- **Audit/Evidence** → Evidence store via AIMS (`/v1/evidence`)


