# AETERNA — EIC Step 2: Jury Q&A Preparation
## Master Cybersecurity & Physical AI Interview Q&A
### Proposal ID №101327948 | Applicant: Dimitar Prodromov

---

> **Format:** 35 minutes Q&A after 10-minute pitch.
> **Jury:** 4-6 evaluators (cybersecurity expert, physical AI systems specialist, finance expert, EU policy lead).
> **Strategy:** Keep answers under 60 seconds. Quantify. Address solo-founder risk immediately and pitch the local, sovereign AI paradigm.

---

## CATEGORY 1: TECHNOLOGY & ARCHITECTURE (15 Questions)

### T1. "How does the Rust NAPI performance engine achieve sub-100ns latency?"
**A:** The engine compiles as a native Node.js binary via NAPI, utilizing Rust's zero-cost abstractions and strict compile-time borrow checking. By using atomic operations (`AtomicU64`) and lock-free concurrent ring buffers, we process security telemetry in-memory without garbage collection (zero GC pauses). This enables a deterministic tick-latency of **89ns**, allowing us to run 3,000 Monte Carlo security simulations in under **1 millisecond**.

### T2. "Why are local Ollama AI models superior to cloud-based APIs like OpenAI?"
**A:** Three reasons: (1) **Data Sovereignty:** Telemetry and vulnerability details never leave European borders or client hardware, ensuring 100% GDPR data residency. (2) **Zero Dependency:** The scanner runs fully offline, immune to external network outages or API pricing spikes. (3) **Cost Efficiency:** Running 16 local Ollama models on a client's GPU cuts cloud inference fees, reducing our infrastructure cost to just **€0.16/user/day**.

### T3. "How does Cognitive Core V2 self-heal broken security test suites?"
**A:** In web-based digital infrastructure, UIs and selectors change frequently, breaking traditional tests. Cognitive Core V2 combines Playwright with our NeuralMapEngine and AutoTestFactory (4,202 LOC). It maps the application tree visually, self-learns selector anchors, and uses 6 ML healing strategies to dynamically repair selectors in real time. Broken security and QA tests are automatically self-healed in **under 30 seconds** without human intervention.

### T4. "What is your Post-Quantum Cryptography roadmap in Work Package 1?"
**A:** During WP1 (€600K, M1–M12), we are migrating our modular CryptoVault to NIST-finalized quantum-safe standards. Specifically, we are integrating **ML-KEM-1024** for secure key encapsulation and **ML-DSA-87** for digital signatures, alongside formal verification using ProVerif and Tamarin. This positions AETERNA as one of the first European SaaS platforms with Common Criteria EAL4+ certification on a PQC-hardened stack.

### T5. "How does the Ghost Protocol bypass Cloudflare and WAFs ethically?"
**A:** AETERNA performs non-intrusive, read-only reconnaissance (GET requests, header analysis). Ghost Protocol uses software-defined network (SDN) techniques to rotate TLS fingerprints every 50ms and apply biometric timing loops. This mimics human cursor movements and organic latency (Turing likeness score of 98.67%), letting us assess public-facing assets without triggering false alarms or getting blocked by security proxies.

### T6. "What is the role of the Federated HiveMind protocol?"
**A:** HiveMind (1,481 LOC) enables secure threat intelligence sharing across organizations. Instead of centralizing sensitive network topologies, it uses **differential privacy** and secure aggregation. Nodes local to each enterprise pool indicators of compromise (IoCs) and pattern observations, feeding threat intel back into the network without ever exposing private customer infrastructure or PII.

### T7. "Why is a 9-month project duration specified in the administrative forms?"
**A:** The **9-month EIC Grant phase** is highly focused on shipping our highest-risk deep-tech modules: WP1 (Post-Quantum Cryptographic CryptoVault integration), WP2 (Federated HiveMind scaling), and WP3 (EU AI Act compliance certification). This rapid duration is possible because the founder has already solo-developed a massive **1.85 million lines of code** foundation, allowing us to focus EIC funding entirely on advanced hardening rather than basic product development.

### T8. "How does the Energy Layer reduce carbon footprint by 65–80%?"
**A:** The Energy Layer (10,340 LOC across 22 modules) implements thermal-aware GPU pooling and neural LRU caching. Running 16 local AI models on-premise on a single local GPU (~150W) is vastly more energy-efficient than routing requests through multi-tenant cloud datacenters, which involve high networking, virtualization, and cooling overhead.

### T9. "What is the GenesisEngine in your evolution layer?"
**A:** The GenesisEngine (part of our 5,368 LOC evolution layer) is an autonomous code-that-creates-code system. It implements a 5-layer entity lifecycle and a SelfCorrectionLoop. When the scanner identifies a security gap or broken test, the AI self-correction loop generates, validates, and refines remediation scripts until a 100% pass rate is achieved.

### T10. "How does AETERNA align with Physical AI and Embodied Intelligence?"
**A:** Our Vortex Synthesis Engine coordinates networks of autonomous physical units (factory robots, logistics swarms, drone fleets). It computes entropy-stability S(t) with mathematical guarantees, processing LiDAR and telemetry at sub-microsecond latency. If a unit experiences sensor failure, Vortex triggers a fleet-wide adaptation in <25ms via lock-free SharedMemoryV2, allowing neighboring units to compensate without human intervention.

### T11. "How do you verify the system's TRL 6 status?"
**A:** Evaluators can verify TRL 6 live on my laptop: (1) Running the compiled Rust NAPI module to confirm sub-100ns tick latency. (2) Executing a mock scan showing Ghost Protocol's active polymorphic identity mutation. (3) Reviewing E2E test results showing a 14/14 PASS Grade A+ verification.

### T12. "What are the six layers of your technical architecture?"
**A:** (1) **Rust NAPI Scan Engine** (<100ns/tick telemetry). (2) **AI Brain** (16 local Ollama models). (3) **Self-Healing** (Cognitive Core V2, 6 ML strategies). (4) **Security Substrate** (PQC ML-KEM/ML-DSA). (5) **Vortex Swarm Orchestration** (SharedMemV2, <25ms IPC). (6) **SaaS Delivery** (Vercel/Next.js).

### T13. "Is there single-point-of-failure risk in your solo-developed stack?"
**A:** It is a risk, but it's heavily mitigated. The codebase is fully modular, documented across a comprehensive 860-page guide, and uses strict version control. Furthermore, our Month 1 and Month 2 hiring plans immediately recruit a Senior Rust Engineer and a Head of Cybersecurity, dropping founder dependency to under 40% in 60 days.

### T14. "Why did you choose Next.js 14 and Vercel for SaaS delivery?"
**A:** Vercel and Next.js 14 provide immediate, high-performance European market access with serverless deployment. It allows us to scale the control dashboard and user billing interfaces easily while keeping the heavy scanning, cryptographic, and neural processing isolated on local edge nodes.

### T15. "What are your 3 EPO patents pending?"
**A:** We are filing patents in Month 3, Month 6, and Month 9 for: (1) Our sub-100ns Rust NAPI telemetry tick engine. (2) The Cognitive Core V2 self-healing algorithm. (3) The HiveMind federated threat intelligence protocol.

---

## CATEGORY 2: MARKET, COMPETITION & BUSINESS (10 Questions)

### M1. "Who are your direct competitors?"
**A:** The market is dominated by centralized, cloud-dependent US scanners: Qualys, Tenable, and Rapid7. Unlike them, AETERNA operates entirely locally, utilizing local AI with zero cloud dependency. This guarantees complete European digital sovereignty, GDPR compliance, and NIS2 reporting compatibility.

### M2. "Why would a client switch from Burp Suite or OWASP ZAP to AETERNA?"
**A:** Traditional pentesting tools like Burp Suite or OWASP ZAP take minutes to scan a page and produce static reports that require manual security engineering. AETERNA's Rust engine scans at sub-100ns speed, self-heals discovered vulnerabilities automatically via Playwright scripts, and integrates local AI explainability out of the box.

### M3. "How big is your addressable market?"
**A:** The European cybersecurity market is projected to reach **€78B** by 2030, with automated security testing growing at 20.8% CAGR. We target a **TAM of €15B**, a **SAM of €2.1B**, and a **SOM of €50M** within 5 years.

### M4. "How does NIS2 act as a market accelerator?"
**A:** The NIS2 Directive mandates strict cyber risk management and incident reporting for over **160,000 European critical entities**. AETERNA is a NIS2 compliance accelerator, offering automated testing, local vulnerability mapping, and instant generation of NIS2-compliant reports without exposing infrastructure data.

### M5. "What is your SaaS pricing strategy?"
**A:** We offer a 3-tier subscription: **Node Access (€29/mo)** for freelancers; **Sovereign Empire (€99/mo)** for mid-sized teams; and **Galactic Core (€499/mo)** for enterprises, plus custom on-premise licensing (€2,000+/mo). This represents a **100× cost reduction** vs. US tools.

### M6. "How will you acquire your first 500 customers?"
**A:** Through three channels: (1) **Content Marketing & Value Bomb:** Publishing free local scan diagnostics. (2) **Open-Source release:** Distributing our core scanning engine under Apache 2.0 to build trust. (3) **MSP/MSSP partner channel:** Onboarding managed security service providers who bundle AETERNA for their SME clients.

### M7. "Why is your blended ARPU so low compared to enterprise tools?"
**A:** Centralized enterprise security tools require six-figure budgets. By pricing AETERNA starting at €99/mo, we remove procurement friction for SMEs. Because our local AI architecture keeps infrastructure costs at **€0.16/user/day**, we maintain an **87% gross margin** even at these low price points.

### M8. "What is your customer retention strategy?"
**A:** Our retention is driven by: (1) **Automated Schedules:** Security scans run continuously 24/7. (2) **HiveMind Network Effects:** The more nodes join, the faster our federated AI recognizes emerging zero-day threats. We project a conservative **15% annual churn**.

### M9. "When does the business achieve break-even?"
**A:** At **Month 26**. Our low cost of capital and extremely efficient local-hosting architecture enable rapid profitability as recurring subscriptions scale.

### M10. "How do you project Y5 revenue of €11.4M?"
**A:** By scaling from **125 active customers (€88.5K ARR)** in Year 1, to **3,000 customers (€2.34M ARR)** in Year 3, and **15,000 customers (€11.4M ARR)** in Year 5, capturing just **1% of our European SAM**.

---

## CATEGORY 3: BUDGET, RISKS & EXECUTION (10 Questions)

### B1. "How will the €2,500,000 grant budget be spent?"
**A:** **48% (€1.2M)** on systems engineering and security research salaries; **16% (€400K)** on subcontracting (Common Criteria EAL4+ audit, AI Act conformity, SOC 2); **6% (€150K)** on GPU and HSM equipment; **6% (€150K)** on consumables; **8% (€200K)** on direct GTM costs; **4% (€100K)** on travel; and **12% (€300K)** on indirect overhead.

### B2. "Why recruit a Senior Rust Engineer at €14,400/mo in Month 1?"
**A:** This senior hire is our **highest-priority mitigation** for founder risk. By matching top-tier European salaries, we recruit an exceptional engineer in the Sofia hub within 30 days, taking over core WP1 PQC integration and reducing founder dependency immediately.

### B3. "Why recruit a Head of Cybersecurity at €16,000/mo in Month 2?"
**A:** This role leads our NIS2 compliance acceleration and acts as our liaison with independent security audit bodies. Hiring a world-class cybersecurity expert ensures our threat mapping matches ENISA standards and drops founder dependency to **<40%** within 60 days.

### B4. "How do you address key-person risk before hires are onboarded?"
**A:** The entire architecture is private but completely modular, backed by an **860-page system specification manual** mapping every module, function, and state machine. If I am incapacitated, a systems engineer can pick up the codebase instantly.

### B5. "What if AI Act requirements exceed your project scope?"
**A:** We have dedicated **Work Package 3 (€400K, M3–M15)** entirely to AI Act compliance. AETERNA's models are local, open-weight, and fully auditable. We will complete a full conformity assessment with a notified body by Month 12 to secure our compliance toolkit.

### B6. "What if quantum computers arrive slower than expected?"
**A:** Post-quantum readiness is a proactive defense. European enterprises and critical infrastructure must prepare now to protect historic encrypted backups from being harvested. Even if quantum hardware is delayed, our PQC compliance provides a major marketing and compliance advantage.

### B7. "Why is your team located in Sofia, Bulgaria?"
**A:** Bulgaria is a premier high-tech hub in Eastern Europe, housing world-class systems engineering talent. High-performance developer salaries are highly competitive, which significantly extends our EIC funding runway compared to Western Europe.

### B8. "How will you structure the company formation?"
**A:** Upon grant notification (Month 0), I will incorporate the business as **AETERNA Technologies EOOD** in Sofia, Bulgaria, or **AETERNA Technologies GmbH** in Berlin, transferring all proprietary IP and codebases to the new legal entity.

### B9. "How will you handle the €5M equity component?"
**A:** The equity co-investment from the EIC Fund is structured to fund our rapid European commercial scale-up: expanding our enterprise sales team across Berlin and Amsterdam, scaling MSP channels, and securing regional edge infrastructure.

### B10. "What is your long-term exit plan?"
**A:** To establish AETERNA as the dominant European sovereign cybersecurity engine. Potential exit paths include an IPO at a €150M+ valuation driven by high recurring revenues, or a strategic acquisition by a sovereign EU technology conglomerate.

---

*Package Version: 3.0 | Prepared for Proposal ID №101327948*
*System State: SECURE | AETERNA est Resiliens.*
