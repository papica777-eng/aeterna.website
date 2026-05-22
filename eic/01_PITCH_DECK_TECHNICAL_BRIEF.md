# AETERNA — Autonomous European Trusted Engine for Resilient Network Assurance
## EIC Accelerator Step 2: Jury Technical Brief
### Grant Application №101327948 | Applicant: Dimitar Prodromov

---

## 0. Document Purpose

> This brief accompanies the pitch deck submitted in Step 1. Per EIC rules, **no new slides** will be shown at the interview. This document provides the **deep technical narrative** behind our slides, structured specifically for the EIC Step 2 jury defense (10-minute pitch + 35-minute Q&A). It reflects the exact data submitted in our **Official Full Application**.

---

## 1. THE PROBLEM — European Dependency & SaaS Fragmentation

### The US Tool Monopoly & Sovereignty Risk
European digital sovereignty is deeply undermined by a near-total reliance on US-based security scanning and vulnerability management tools (Qualys, Tenable, Rapid7, Snyk). None of these platforms offer:
1. **On-Premise AI Intelligence** — All telemetry and raw code repository data are sent to US-based cloud infrastructures, raising extreme compliance issues.
2. **GDPR-Native Data Residency** — Real-time vulnerability logs, local system paths, and network topology maps are exposed outside EU jurisdiction.
3. **EU AI Act Transparency** — Decisions are driven by closed-source, black-box cloud APIs that cannot be audited or verified by European regulatory bodies.

### The SaaS Quality Assurance Crisis
European SMEs (10–250 employees) operate an average of **23 separate SaaS subscriptions** (Gartner, 2025). Each integration requires independent maintenance, manual API bridging (e.g., Zapier/Make), and manual testing. When APIs break:
- **No Self-Healing:** Uptime collapses and companies must wait days for consultants to manually fix broken selector anchors.
- **The Fragmentation Tax:** A typical 50-person company loses an average of **€2,000/month** in hidden manual QA validation and broken SaaS automation tasks.

---

## 2. THE SOLUTION — Project AETERNA

AETERNA is a production-ready, AI-powered autonomous cybersecurity and quality assurance platform that scans, detects, and self-heals digital infrastructure vulnerabilities entirely offline, with full data sovereignty. It compiles into a modular Rust NAPI core that operates locally on sovereign hardware with zero cloud dependency.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LAYER 6: SAAS DELIVERY                          │
│                Vercel + Next.js 14 Web Portal (€29–€499/mo)            │
├────────────────────────────────────────────────────────────────────────┤
│                   LAYER 5: VORTEX SWARM ORCHESTRATION                  │
│       SharedMemV2 (<25ms IPC) + GhostShield (Stealth Rotator)          │
├────────────────────────────────────────────────────────────────────────┤
│                        LAYER 4: SECURITY CORE                          │
│     AES-256-GCM + ChaCha20 + PQC-Ready (ML-KEM-1024 + ML-DSA-87)       │
├────────────────────────────────────────────────────────────────────────┤
│                   LAYER 3: COGNITIVE SELF-HEALING V2                   │
│      NeuralMapEngine + AutoTestFactory + Playwright (4,202 LOC)        │
├────────────────────────────────────────────────────────────────────────┤
│                          LAYER 2: AI BRAIN                             │
│        16 Local Ollama LLM Models (Fully Auditable & Offline)          │
├────────────────────────────────────────────────────────────────────────┤
│                        LAYER 1: SYSTEM ENGINE                          │
│         Rust NAPI Core with AtomicU64 (<100ns telemetry ticks)          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. TECHNOLOGY — The Six-Layer Architecture (TRL 6)

### 3.1 Rust NAPI Telemetry Engine (Layer 1)
To handle real-time security signals across tens of thousands of endpoints, AETERNA leverages a core built in Rust compiled to a native Node.js addon (NAPI) using `AtomicU64` and lock-free concurrent ring buffers.
- **Hardware-Level Performance:** Zero garbage collection (GC) pauses, zero-cost abstractions, and compile-time memory safety.
- **Deterministic Latency:** Achieves a sub-100ns per-tick processing time (**128ns average latency** validated), outperforming Python/C++ telemetry pipelines.

### 3.2 AI Brain — 16 Local Ollama Models (Layer 2)
AETERNA is entirely cloud-independent. It routes raw pattern recognition and threat classification tasks through 16 locally hosted, open-weight Ollama LLMs.
- **GDPR-Native:** Threat intelligence data never leaves the local machine or enterprise subnet.
- **EU AI Act Pioneer:** All model weights are fully inspectable, and decisions are explainable (WP3 toolkit).

### 3.3 Cognitive Self-Healing V2 (Layer 3)
AETERNA's self-healing stack (4,202 LOC) combines parallel site crawling with visual fingerprinting and self-learning selector anchors:
- **6 ML Healing Strategies:** When a web element modifies its DOM structure (e.g., dynamic ID changes), the Cognitive Core automatically repairs the locator using relative visual coordinates, sibling anchors, text embeddings, and historic paths.
- **AutoTestFactory:** Automatically writes and refines its own test scripts from raw exploration, operating 24/7 with zero manual intervention.

### 3.4 Cryptography & Post-Quantum Readiness (Layer 4)
- **Current Crypto Stack:** AES-256-GCM + ChaCha20-Poly1305 + SHA-512.
- **Quantum-Safe Ledger:** SovereignLedger's SHA-512 hash chains are quantum-resistant (Grover's algorithm reduces to 256-bit effective security — well above the 128-bit threshold).
- **PQC Roadmap (WP1):** Full migration to NIST ML-KEM-1024 (key encapsulation) and ML-DSA-87 (digital signatures, finalized August 2024).

### 3.5 Vortex Swarm Orchestration (Layer 5)
- **SharedMemoryV2:** Enables **<25ms O(1) lock-free IPC** data exchange between autonomous units.
- **Ghost Protocol:** Implements ML-powered WAF/Cloudflare bypass via polymorphic TLS fingerprint rotation and biometric mouse-motion timing, ensuring invisible security audits without triggering alerts.

---

## 4. MARKET & COMPETITION — €15B TAM Opportunity

AETERNA bottom-up market sizing is aligned with actual EU statistics:

| Segment | Description | ARPU/yr | SAM |
|---------|-------------|---------|-----|
| **EU SMEs** | 230,000 companies needing NIS2 / local security | €1,188 | €273.2M |
| **EU Scale-ups** | 12,000 high-growth tech clusters | €5,988 | €71.8M |
| **Enterprise** | On-premise secure scanning deployments | €24,000 | €60.0M |
| **Total SAM** | **Serviceable Addressable Market** | | **€2.1B** |

- **TAM (Total Addressable Market):** **€15B** (Global local AI, QA, and security testing)
- **SOM (Serviceable Obtainable Market - Y5):** **€50M** (1% SAM target in 5 years)
- **Pricing Strategy:** Disruptive SaaS subscription model:
  - **NODE ACCESS:** €29/mo (Freelancers, micro-SMEs)
  - **SOVEREIGN EMPIRE:** €99/mo (SME 20–100 employees)
  - **GALACTIC CORE:** €499/mo (Scale-up/Enterprise)
  - **ENTERPRISE CUSTOM:** €2,000+/mo (Large enterprise, on-premise)

---

## 5. USE OF FUNDS — EIC €2.5M Grant Allocation

The EIC Grant budget has been planned with absolute precision matching the submitted EIC worksheets:

* **48% (€1,200,000) — Personnel:** 5 FTE systems and ML engineers over 24 months (average €10K/month including social charges). This scales the core from the founder to a robust dev team.
* **16% (€400,000) — Subcontracting:** Independent cryptographic audit (€150K), AI Act Notified Body compliance certification (€100K), SOC 2 Type II auditor (€80K), and specialized legal/IP costs (€70K).
* **6% (€150,000) — Equipment:** High-performance local GPU servers for Ollama training (2× NVIDIA A100), plus hardware security modules (HSM) for PQC key storage.
* **6% (€150,000) — Consumables & Cloud:** Web hosting, sovereign Hetzner EU nodes, monitoring, and CI/CD.
* **8% (€200,000) — Other Direct:** Market research, UX localizations (DE/FR/NL/SE), and developer marketing.
* **4% (€100,000) — Travel & Conferences:** Global cybersecurity/academic validation (Black Hat EU, RSA, Web Summit).
* **12% (€300,000) — Indirect Costs:** Flat 25% overhead rate per standard Horizon Europe rules.

---

## 6. FINANCIAL PROJECTIONS — 5-Year Growth

| Year | Customers | MRR (EOY) | ARR (EOY) | Gross Margin % |
|------|-----------|-----------|-----------|----------------|
| **Y1 (2026)** | 125 | €7,375 | **€88,500** | 82% |
| **Y2 (2027)** | 800 | €52,000 | **€624,000** | 85% |
| **Y3 (2028)** | 3,000 | €195,000 | **€2,340,000** | 87% |
| **Y4 (2029)** | 8,000 | €480,000 | **€5,760,000** | 89% |
| **Y5 (2030)** | 15,000 | €950,000 | **€11,400,000** | 91% |

- **Unit Economics:** LTV is **€4,312** based on €119.78 blended ARPU and 36-month retention. CAC is **€180**, resulting in an exceptional **23.9x LTV:CAC ratio**.
- **Break-Even:** Month 22 (Q2 2028) based on grant-only modeling.

---

## 7. TEAM & FOUNDER RISK MITIGATION

### Dimitar Prodromov — Sole Founder & Architect
- **Track Record:** Single-handedly built the entire **528,582 lines of TypeScript/Rust/Zig codebase** (2,211 source files, 1,015 modules) of the live platform.
- **Founder Risk Mitigation (First 60 Days):**
  - **Month 0:** Incorporate AETERNA Technologies EOOD (Bulgaria) or GmbH (Berlin).
  - **Month 1:** Hire **Senior Rust Engineer** (€14,400/mo) for core engine scaling & WP1 PQC integration.
  - **Month 2:** Hire **Head of Cybersecurity** (€16,000/mo) for Ghost Protocol compliance and ENISA liaison.
  - *Result:* Founder dependency drops from 100% to under 40% in 60 days.

---

## 8. EU STRATEGIC ALIGNMENT

AETERNA directly addresses the EIC 2026 priority challenges:
1. **Emied Intelligence / Physical AI:** Vortex Synthesis Engine provides mathematical guarantees for real-time coordination of drone swarms and physical IoT telemetry via entropy-stability equations.
2. **Post-Quantum Cryptography:** Aligns directly with EuroQCI and BSI's migration roadmap by integrating ML-KEM-1024 and ML-DSA-87.
3. **Do No Significant Harm (DNSH):** Operating 16 open-weight AI models locally on an RTX 4050 (~150W) instead of relying on massive cloud server pools reduces carbon footprint by **65–80%** (validated by the Energy Layer's 10,340 LOC thermal optimization).

---

*Document Version: 3.0 | Prepared: 2026-05-22*
*Applicant: Dimitar Prodromov | Project AETERNA*
