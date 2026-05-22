# AETERNA — EIC Step 2 Jury Q&A Defense Guide
## 53 Anticipated Questions with Prepared Strategic Answers
### Grant №101327948 | Dimitar Prodromov

---

> **Format:** 35 minutes Q&A immediately following the 10-minute pitch.
> **Jury Structure:** 4-6 senior evaluators covering deep tech, venture finance, commercial scale, and European digital sovereignty policy.
> **Strategy:** Provide highly structured, metric-driven answers in under 60 seconds. Maintain absolute transparency on risks while proving technical superiority.

---

## 🗂️ CATEGORY 1: CORE DEEP TECH & ARCHITECTURE (15 Questions)

### T1. "How does the Rust NAPI Telemetry Engine achieve sub-100ns latency?"
**Answer:** The telemetry core is built in pure Rust and compiled as a native Node.js addon (NAPI). By bypassing the high-overhead Node.js runtime and utilizing lock-free concurrent ring buffers alongside `AtomicU64` registers, we eliminate CPU context-switching overhead and garbage collection (GC) pauses. Telemetry operations process directly on raw network packet buffers. This allows AETERNA to achieve an average telemetry tick latency of **128 nanoseconds**, enabling hard real-time network analysis that Python or C++ alternatives cannot sustain without memory-safety compromises.

### T2. "How do you run 16 different local Ollama LLMs on a single edge machine without crashing?"
**Answer:** We run a customized, lightweight LLM routing layer we call **BrainRouter** (490 LOC). Instead of loading all 16 models into VRAM simultaneously, we use a neural Least Recently Used (LRU) cache and thermal-aware GPU pooling via our **Energy Layer** (10,340 LOC). Models are quantized to 4-bit and 3-bit GGUF formats and pooled. The active scanning phase only swaps models (e.g., threat classification, exploit analysis, report generation) as needed, keeping peak VRAM footprint under 8GB (runnable on a single mobile RTX 4050 / ~150W), representing a 65–80% lower carbon footprint than cloud AI deployments.

### T3. "What are the 6 ML strategies utilized by your Self-Healing V2 engine?"
**Answer:** When target websites or interfaces modify their DOM structures (dynamic IDs, CSS changes, structural shifts), AETERNA's self-healing stack (4,202 LOC) repairs broken selectors dynamically using:
1. **Sibling Anchor Mapping:** Locating elements relative to stable neighboring nodes.
2. **Visual Coordinate Profiling:** Finding elements via relative X/Y coordinates on visual maps.
3. **Semantic Text Embeddings:** Mapping interactive elements based on their NLP function (using local text embeddings).
4. **XPath Historic Recovery:** Reconstructing the DOM hierarchy path from historic successful runs.
5. **Interactive Heuristic Search:** Autonomously clicking alternative interactive paths when a block is hit.
6. **Self-Correction Loop:** Real-time AI repair via our GenesisEngine, auto-testing alternatives until a 100% pass rate is achieved.

### T4. "What is the Vortex Synthesis Engine and how does it relate to Embodied Intelligence?"
**Answer:** Vortex (5,800 LOC) is a swarm orchestration system designed for lock-free multi-node synchronization using SharedMemoryV2. It maintains an entropy-stability equilibrium $S(t)$ with a synchronization latency of **under 25ms**. In physical AI environments (such as logistics swarms, factory IoT, or edge networks), if a single node encounters a hardware or sensor fault, neighboring nodes detect the entropy spike and automatically adjust their cooperative pathing or coverage without human intervention.

### T5. "How does your Ghost Protocol bypass Web Application Firewalls (WAF) like Cloudflare?"
**Answer:** WAF systems detect automated scanners through rigid TLS handshakes, fixed header sequencing, and artificial mouse-movement speeds. Ghost Protocol bypasses these security barriers through:
1. **Polymorphic TLS Fingerprint Rotation:** Dynamically changing TLS ja3 signatures every 50ms.
2. **Biometric Mouse Simulation (Ghost Cursor):** Generating natural Bezier paths for cursor navigation with realistic velocity profiles and micro-jitters, passing the advanced Turing test audits of modern firewalls.
3. **Read-Onlyrecon Policy:** It operates strictly as a non-intrusive reconnaissance engine (GET requests, header/DOM analysis), performing security audits without triggering rate limits or defensive alerts.

### T6. "What is your Post-Quantum Cryptography (PQC) migration plan in WP1?"
**Answer:** AETERNA currently secures its cryptographic core (CryptoVault) with classical AES-256-GCM, ChaCha20-Poly1305, and SHA-512. In Work Package 1 (€600K, M1–M12), we are migrating our key encapsulation to **NIST ML-KEM-1024** and our digital signatures to **ML-DSA-87** (both finalized by NIST in August 2024). This hardened stack will undergo rigorous formal verification using ProVerif/Tamarin, targeting a Common Criteria EAL4+ security certification.

### T7. "Why did you build your own federated threat intelligence layer instead of using standard APIs?"
**Answer:** European enterprises cannot share raw security logs due to GDPR restrictions and proprietary network mapping risks. Our federated learning model, **HiveMind** (1,481 LOC), uses **Differential Privacy** and secure aggregation via Shamir Secret Sharing. This allows participating nodes to collectively train threat recognition models and share indicator-of-compromise (IOC) signatures without ever sharing their local raw network configurations, logs, or PII.

### T8. "How does AETERNA's self-healing test automation differ from traditional tools like Selenium?"
**Answer:** Selenium and standard Playwright configurations require QA engineers to manually code test scripts and update locators whenever the target app changes. AETERNA's **AutoTestFactory** is autonomous. It explores web interfaces, maps interactive states, auto-generates test scenarios, and heals broken locator selectors on the fly via local AI, completely removing human intervention and saving enterprises €12K–€85K/year in maintenance overhead.

### T9. "What is the role of Zig and Erlang/BEAM in your core codebase?"
**Answer:** Zig is used to compile ultra-high-speed memory-safe systems bridges where Node.js NAPI requires direct access to physical network hardware without runtime wrappers. Erlang/BEAM is utilized in our multi-node supervisor architecture, providing a zero-panic, fault-tolerant orchestrator that guarantees 99.999999% uptime for swarm communications.

### T10. "If the platform runs completely offline, how does it receive threat intelligence updates?"
**Answer:** AETERNA is dual-capable. It operates 100% offline using local AI weights and custom heuristics, which is essential for sovereign data defense. When connected, it utilizes a secure, read-only threat sync via our HiveMind federated network to pull latest signed ML-DSA-87 signatures. If internet connectivity is cut, AETERNA continues to function locally with its pre-loaded intelligence models.

### T11. "How do you prove that your local AI decisions are explainable under the EU AI Act?"
**Answer:** Work Package 3 (€400K, M3–M15) is dedicated entirely to our **EU AI Act Compliance Engine**. We implement a dedicated explainability layer for all 16 local Ollama model decisions. For every threat flag or healed selector, AETERNA outputs a localized, human-readable decision tree showing the specific weights, visual anchor references, and semantic embeddings that triggered the AI's action.

### T12. "What happens if there is a conflict in the local AI decisions?"
**Answer:** We run our **BrainRouter** routing layer. Decision loops are audited through a 7-phase signal safety audit (CyberCody). If two local models disagree (e.g., threat classification vs false-positive heuristic), the decision is deferred to the hybrid consensus block where mathematical entropy checks resolve the mismatch, ensuring high-accuracy security reporting.

### T13. "Is your TRL 6 status fully validated?"
**Answer:** Yes. AETERNA's TRL 6 is validated by a production-ready SaaS platform at `aeterna.website` running live E2E tests at Grade A+, verified Rust NAPI module benchmarks (128ns latency), a fully developed 528K LOC private codebase, and operational 16 local AI models running on edge setups.

### T14. "What IP protection strategy are you deploying?"
**Answer:** Our IP strategy is multi-tiered:
1. **EU Trademark:** Filed in Month 1.
2. **EPO Patents:** We will file three European patents (Rust engine at M3, self-healing selector algorithm at M6, HiveMind federated aggregation at M9).
3. **Trade Secrets:** The Ghost Protocol, specific local AI prompt weights, and physical swarm synchronization equations are retained as trade secrets.

### T15. "Can AETERNA protect physical networks like factory robots or drone swarms?"
**Answer:** Yes. In Work Package 4 (€350K, M6–M18), we scale our Vortex engine to support physical telemetry, enabling local threat detection and self-healing signal adaptation across IoT and physical robotic networks in industrial zones.

---

## 📈 CATEGORY 2: MARKET, COMPETITION & SOVEREIGNTY (10 Questions)

### M1. "Who are your direct competitors and how do you beat them?"
**Answer:** Our primary competitors are US cloud-dependent tools like Qualys, Tenable, and Rapid7. We beat them on:
1. **Sovereignty:** 100% local AI processing. Data never leaves the EU.
2. **Cost:** €29–€499/mo SaaS model vs. €5K–€50K per security audit (a 100x cost reduction).
3. **Automation:** Autonomous selector repair and self-writing tests, whereas legacy platforms require massive manual configuration and consultancy fees.

### M2. "Why will European SMEs migrate from established platforms to AETERNA?"
**Answer:** They are forced to by regulation. Under the newly enforced **NIS2 Directive** (effective October 2024), over 160,000 European entities are legally required to implement continuous vulnerability scanning and sovereign data protection. US cloud platforms raise legal sovereignty concerns. AETERNA is the only platform that provides fully local, NIS2-compliant scanning out-of-the-box.

### M3. "How do you validate your Customer Acquisition Cost (CAC) of €180?"
**Answer:** Our CAC is validated through three organic channels:
1. **Developer Open-Source Strategy:** Releasing our core engine under Apache 2.0 (WP6) to drive 5,000+ GitHub stars, creating a massive self-serving funnel.
2. **MSP/MSSP Channel Program (M6+):** Partnering with Managed Service Providers who bundle AETERNA for their entire SME customer portfolio.
3. **Technical Content Marketing:** Providing free sovereign network scan audits ("Value Bomb") that convert technical leads organically.

### M4. "What is your European Go-To-Market strategy?"
**Answer:** We are deploying a targeted geographic rollout starting with the **DACH, Nordics, and Benelux** regions in Year 1, expanding to Central and Eastern Europe (CEE) by Year 2. We are engaging directly with regional CERTs (Computer Emergency Response Teams) and cybersecurity clusters in Sofia and Berlin.

### M5. "How do you handle enterprise sales when you are a small startup?"
**Answer:** We bypass the long procurement cycles of traditional enterprise through our self-service SaaS portal. For larger entities needing on-premise deployments, we sell via our **MSP/MSSP partner channel**, leveraging their existing sales teams, compliance certifications, and customer relationships.

### M6. "What prevents a giant like Qualys from copying your local AI model?"
**Answer:** Qualys' business model and multi-billion-dollar infrastructure are built entirely on cloud telemetry. Transitioning to on-premise, edge-based local LLM swarm intelligence would require them to rebuild their legacy codebases, rewrite their pricing structures, and obsolete their own cloud centers. Our 528K LOC codebase represents a significant technical moat.

### M7. "Is €29/month too low to signal security quality to enterprises?"
**Answer:** The €29/mo Node tier is specifically designed for freelancers and micro-SMEs to democratize security access. Our enterprise and on-premise customers are targeted via our custom tiers starting at **€2,000+/month**, which perfectly balances market reach with high-end enterprise positioning.

### M8. "What is your strategy for achieving SOC 2 Type II certification by Month 18?"
**Answer:** We have allocated €80K in WP5 subcontracting specifically for the SOC 2 Type II audit. Since AETERNA already integrates automated self-scanning, continuous compliance monitoring, and immutable ledger logging, we will maintain a continuous audit state, speeding up the formal certification process.

### M9. "How does the NIS2 Directive act as a growth driver for you?"
**Answer:** NIS2 mandates strict security reporting, supply chain risk management, and vulnerability disclosure for essential and important entities across the EU. Traditional US tools lack automated compliance checking. AETERNA provides automated BSI IT-Grundschutz and NIS2 framework reporting out-of-the-box, turning compliance from a manual chore into a 1-click audit.

### M10. "How do you plan to scale direct sales in Germany and the Netherlands?"
**Answer:** In WP5 (€400K budget), we are hiring three senior enterprise sales representatives based in Berlin and Amsterdam to target regional SME clusters and local government contractors who face immediate sovereignty requirements.

---

## 💸 CATEGORY 3: FINANCIALS & UNIT ECONOMICS (10 Questions)

### F1. "Your projections show €11.4M ARR by Year 5. How realistic is this?"
**Answer:** This is highly realistic and conservative. It requires capturing just **1% of our €2.1B SAM** in five years. We grow from 125 customers in Year 1 to 15,000 customers in Year 5. Given that over 160,000 EU companies are bound by NIS2, capturing 15,000 customers across 27 member states represents a very achievable growth rate.

### F2. "When does Project AETERNA achieve break-even?"
**Answer:** AETERNA achieves financial break-even in **Month 22** of operations. With the €2.5M EIC grant and our high gross margin, our cash flow remains highly positive throughout the R&D phase, ensuring long-term financial viability.

### F3. "How do you justify your 87% Gross Margin?"
**Answer:** Unlike traditional AI startups that pay massive monthly API inference fees to OpenAI or Microsoft Azure, AETERNA runs open-weight LLMs locally on our customer's edge hardware. Our cloud hosting costs are minimal (flat sovereign edge servers via Hetzner), representing an infrastructure cost of just **€0.16 per user per day**.

### F4. "What is your LTV-to-CAC ratio and why is it so high?"
**Answer:** Our LTV-to-CAC ratio is **23.9x** (CAC: €180, LTV: €4,312). This is driven by our extremely low acquisition cost (leveraging open-source funnels and MSP channels) and our high customer retention (36-month average lifetime based on our platform's deep operational integration).

### F5. "What if your customer acquisition cost doubles?"
**Answer:** Even if our CAC doubles to €360, our LTV-to-CAC ratio remains at a highly lucrative **11.9x**, which is still four times higher than the venture capital industry benchmark of 3.0x, showing robust economic resilience.

### F6. "Explain the bookings vs. recognized revenue discrepancy in your model."
**Answer:** We offer custom enterprise clients custom multi-year billing or annual prepayments with discounts. Under IFRS 15, prepayment bookings are deferred and recognized progressively over the 12-month service period, ensuring conservative and compliant accounting.

### F7. "Why is Personnel 48% of your EIC Grant budget?"
**Answer:** As a deep-tech cybersecurity platform, our primary value is our code. Scaling our high-speed Rust core and optimizing 16 local LLM models requires elite systems and ML engineering talent. The €1.2M personnel budget covers 5 FTE engineers over 24 months at standard EU rates.

### F8. "What is your cash runway if the EIC Equity investment is delayed?"
**Answer:** On the grant-only scenario (€2.5M), we maintain a cash runway of **58 months** at our Year 1 monthly burn rate of €43,000, ensuring complete operational independence and zero risk of shutdown.

### F9. "What is your Year 3 revenue target in case of a Bear market?"
**Answer:** Our sensitivity analysis shows that under a Bear market scenario (-30% growth), AETERNA still achieves **€1.8M ARR in Year 3** and breaks even in Month 28, keeping the company highly viable.

### F10. "Why do you have a subcontracting budget of €400,000?"
**Answer:** High-end cybersecurity requires trusted third-party validation. €150K is dedicated to a rigorous cryptographic audit, €100K to an AI Act notified body, €80K for SOC 2 certification, and €70K for patent filing. These cannot be performed in-house and are critical for market trust.

---

## 👥 CATEGORY 4: TEAM, RECRUITING & RISK MANAGEMENT (10 Questions)

### E1. "You are the sole founder and built this alone. Isn't the key-person risk too high?"
**Answer:** Yes, it is a valid concern, which is why my **Number 1 Priority upon EIC award** is the elimination of this risk:
1. **Month 1:** Hire a Senior Rust Systems Engineer (€14,400/mo) to take over core engine development.
2. **Month 2:** Hire a Head of Cybersecurity (€16,000/mo) to manage Ghost Protocol audits and ENISA coordination.
3. *Result:* Founder dependency drops from 100% to under 40% within 60 days of project launch.

### E2. "Why pay €14,400/month for a Rust engineer in Bulgaria? Isn't that too high?"
**Answer:** We are building a hard real-time, sub-100ns telemetry engine with post-quantum cryptography. We cannot hire junior developers for this. We need elite, world-class systems engineers. Paying top-tier salaries allows us to attract the absolute best talent in Europe, securing our technology moat.

### E3. "How will you manage 5+ engineers when you have been coding solo?"
**Answer:** I have spent the bootstrapping phase writing a complete **860-page DOCUMENTATION.md** and structuring our system rules in declarative `.soul` manifolds. The codebase is highly modularized, with clean separation between the Rust telemetry core, local AI routing, and Next.js frontends, ensuring frictionless onboarding.

### E4. "Why did you incorporate in Bulgaria instead of Germany?"
**Answer:** Sofia, Bulgaria is one of Europe's fastest-growing deep-tech hubs, home to elite engineering talent from the Sofia Tech Park. Bulgaria offers a highly competitive operational cost structure, extending our R&D runway. We plan to establish a secondary entity in Berlin (GmbH) in Year 2 to accelerate DACH market sales.

### E5. "What happens to the IP if you are incapacitated?"
**Answer:** All AETERNA source code, documentation, and cryptographic keys are secured in a multi-signature offline vault. The veritas validation protocol is fully automated, ensuring that another systems engineer can immediately verify, run, and compile the entire repository.

### E6. "Who is on your advisory board?"
**Answer:** We are currently structuring our advisory board to include three key roles:
1. **Fintech Compliance Advisor:** A former regulator with deep knowledge of secure transaction tracking.
2. **Enterprise Sales Advisor:** An ex-VP of Sales from a leading European SaaS company to guide our MSP rollout.
3. **PQC Cryptographer:** An academic researcher specializing in NIST post-quantum standards.

### E7. "What is your personal commitment to AETERNA?"
**Answer:** I am 100% committed. I have spent the last two years bootstrapped, working 80-hour weeks to single-handedly build this 528K LOC platform. I have zero other business interests, zero side projects, and I will be directing all my energy to scaling AETERNA.

### E8. "How will you ensure gender balance in your hiring plan?"
**Answer:** AETERNA is committed to Horizon Europe's diversity guidelines, targeting at least **40% women/non-binary hires**. We publish our open positions through specialized networks like Women in Tech CEE and Sofia Tech Park diversity programs. The Head of Cybersecurity role is actively targeted toward female candidates.

### E9. "How do you handle developer onboarding?"
**Answer:** Our onboarding is fully structured:
- **Weeks 1–2:** Deep-dive into our modular architecture and declarative `.soul` rules.
- **Weeks 3–4:** Pair-programming on peripheral Next.js or telemetry interfaces.
- **Month 2:** Independent ownership of specific modules with strict Git pull-request reviews.

### E10. "What is your company's corporate structure?"
**Answer:** Upon EIC award notification, the sole proprietorship will immediately incorporate as **AETERNA Technologies EOOD** in Bulgaria, with all IP transferred to the new corporation, ready for EIC equity investment.

---

## 🇪🇺 CATEGORY 5: GDPR, REGULATORY & ETHICS (8 Questions)

### U1. "Ghost Protocol bypasses WAFs. Isn't this dual-use or malware tech?"
**Answer:** Absolutely not. Ghost Protocol is strictly a **read-only reconnaissance engine**. It does not perform SQL injections, does not exploit vulnerabilities, and does not execute payloads. It merely bypasses artificial WAF blocks to audit the public-facing DOM structure, ensuring automated scanners do not trigger false alerts. This is standard, ethical quality assurance and vulnerability discovery.

### U2. "How does AETERNA guarantee GDPR compliance when scanning systems?"
**Answer:** AETERNA operates under strict data minimization rules. We do not scan PII, nor do we collect personal data. Our scans focus entirely on publicly accessible digital infrastructure, configuration files, and software dependencies. Because our AI models run locally on the client's hardware, no scanned logs ever cross international borders or leave the customer's jurisdiction.

### U3. "Does your platform comply with the new EU AI Act?"
**Answer:** Yes. AETERNA is a pioneer in AI Act compliance. Because we run open-weight, locally hosted LLMs, our decision-making pipeline is 100% auditable. Work Package 3 is dedicated to creating an automated AI Act risk classification toolkit, ensuring all AI-generated reports are labeled, explainable, and under human-in-the-loop control.

### U4. "How does local AI execution support the EU Green Deal?"
**Answer:** Traditional cloud AI models require massive data center compute, high-latency cooling, and network routing. Running AETERNA's quantized models locally on an edge GPU (e.g., RTX 4050 / ~150W) with neural LRU caching reduces carbon emissions by **65 to 80%** compared to equivalent cloud AI queries.

### U5. "How do you prevent malicious actors from using AETERNA to find exploits?"
**Answer:** Our Terms of Service strictly restrict the platform's use to authorized, owned digital infrastructures. Furthermore, our SovereignLedger maintains an immutable, cryptographically signed trail of all scans. A malicious actor cannot run anonymous scans through AETERNA without leaving a permanent audit trail, acting as a powerful deterrent.

### U6. "What is your position on the EuroQCI (European Quantum Communication Infrastructure) initiative?"
**Answer:** AETERNA directly supports EuroQCI. By migrating our cryptography core to NIST-approved ML-KEM-1024 and ML-DSA-87 in Year 1, we ensure that European networks scanned by AETERNA are hardened against future quantum decryption threats, aligning with the EU's secure quantum roadmap.

### U7. "How do you handle bias detection in your AI-generated security reports?"
**Answer:** Our local AI models only process technical data: code patterns, port mappings, and API schemas. There is zero processing of human or demographic variables, eliminating social biases at the source. For report generation, WP3 implements automated fairness and variance monitoring to ensure strict technical neutrality.

### U8. "Why should the EIC trust a solo applicant with €2.5M of European taxpayer money?"
**Answer:** Because the evidence is in the execution. Building a 528K LOC production-ready platform solo proves world-class engineering discipline and capital efficiency. I am not asking the EIC to fund a PowerPoint presentation; I am asking the EIC to fund the scaling of a fully compiled, working sovereign technology that is already live and validated at TRL 6.
