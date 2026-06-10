# Stellar Community Fund (SCF) - Build Award Submission Draft
## Project Name: VERTEX FINANCE (AETERNA VORTEX)
### Category: Smart Contract Infrastructure & Developer Tooling

---

### 1. Project Abstract
**VERTEX FINANCE** (formerly AETERNA K2) is a decentralized, zero-entropy lending protocol and automated liquidation pipeline built natively on the Stellar Soroban smart contract platform. The system is designed using a strict Hexagonal Architecture (Ports & Adapters) and is coupled with a production-ready off-chain keeper daemon (`AutoBrokerDaemon`) and a real-time telemetry terminal. 

To meet the highest standards of security and reliability required for institutional capital, VERTEX implements:
1.  **ML-KEM-1024 Post-Quantum Security:** Transport-layer data exchange between off-chain keepers and API nodes is protected by hybrid post-quantum cryptography.
2.  **Zero-Entropy Mechanics:** Fixed liquidation incentives (5% cap) and pure Rust math boundaries prevent cascading predatory liquidations.
3.  **Akash DeCloud Hosting:** The off-chain keeper infrastructure runs autonomously on the decentralized Akash Network.

---

### 2. Problem & Solution
*   **The Problem:** Existing DeFi credit markets on EVM chains suffer from systemic "entropy" (reentrancy risks, oracle manipulation, and sandwich/frontrunning MEV attacks) which drain user collateral. On Soroban, there is a lack of production-grade, open-source liquidation keepers and zero-friction onboarding primitives (like gasless interactions) for institutional-scale lending.
*   **The Solution:** VERTEX FINANCE solves this by introducing a Zero-Entropy routing contract (`k2_kinetic_router`) coupled with a localized keeper. The protocol intercepts MEV by routing 2.5% of covered debt directly to the protocol treasury (`k2_treasury`) as permanent reserves. It is integrated with a high-performance Node.js/TypeScript keeper daemon (`AutoBrokerDaemon`) running on Akash Network, executing batch liquidations and using automated RPC failovers to guarantee zero-downtime execution.

---

### 3. Product Readiness & Live Akash Ingress
VERTEX is not a concept; it is a live, running autonomous system. The off-chain keeper infrastructure has been containerized and successfully deployed to the decentralized cloud (Akash Network DeCloud).

*   **Live Ingress Endpoint:** [http://k50tkat9l19np9le8ovbgkmpgs.ingress.hurricane.akash.pub](http://k50tkat9l19np9le8ovbgkmpgs.ingress.hurricane.akash.pub)
*   **Health Status Route:** [http://k50tkat9l19np9le8ovbgkmpgs.ingress.hurricane.akash.pub/health](http://k50tkat9l19np9le8ovbgkmpgs.ingress.hurricane.akash.pub/health)
*   **Docker Registry Image:** `papica777/aeterna:v1.0.1`
*   **Active Deployment DSEQ:** `1781036268078`

#### Live Status API Payload
```json
{
  "status": "SUCCESS",
  "timestamp": "2026-06-10T17:58:11.407Z",
  "uptime_seconds": 77992.18517477199,
  "infrastructure": "10M+ EDGE NODES",
  "pqc_status": "ML-KEM-1024_ACTIVE",
  "entropy": "0.0000",
  "authority": "VERIFIED"
}
```

---

### 4. Stellar Quest & Native Feature Validation
The lead architect ([**dp08685**](https://quest.stellar.org/profile/dp08685) / **papica777**) is **16/16 Stellar Quest certified** (verified proof screenshot: [Stellar Quest 16/16 Verification Proof](./assets/stellar_quest_proof.png)) with programmatic verification scripts included directly in the pipeline repository. Advanced Stellar features are built into the protocol core:
*   **Fee-Bump Transactions:** Utilized by the routing middleware to sponsor ledger transaction fees from the protocol's treasury, allowing gasless Web3 onboarding. Users can pay fees in USDC or fiat via Stripe integration adapters.
*   **Muxed Accounts:** Supported natively to isolate institutional liquidity streams and prevent cross-account contamination in enterprise-custodial wallets.

---

### 5. Advanced DeFi Optimizations (The Pillars)

1.  **Transaction Batching:** The keeper engine aggregates multiple unhealthy positions into single liquidation transactions. This eliminates frontrunning risks and reduces network fees. If simulation checks detect a single position failure, the adapter atomically splits the batch to execute successful liquidations.
2.  **Dynamic Fee-Bumping:** The system automatically wraps user smart contract interactions in fee-bump envelopes sponsored by `k2_treasury`, offering a frictionless UX.
3.  **State Self-Healing (RPC Fallback):** The keeper includes a network fallback circuit breaker. Upon detecting high latency, network splits, or node crashes, it automatically rotates to backup RPC providers (e.g. `stellar-testnet.publicnode.com`) to preserve uptime.

---

### 6. Milestones, Tranches & Budget Allocation
We request a total budget of **$60,000 in XLM equivalent** split across three distinct project milestones:

#### **Tranche 1: Core Soroban Contracts & Security Hardening (Month 1-2)**
*   **Requested Funding:** $15,000 in XLM equivalent.
*   **Objective:** Optimize and secure the smart contract suite on Stellar Testnet.
*   **Deliverables:**
    1.  Fully audited Rust smart contracts (`k2_kinetic_router`, `k2_treasury`, `k2_incentives`).
    2.  Testnet deployment hashes and verification in workspace optimizer.
    3.  Mathematical whitepaper documenting zero-entropy boundary proofs.
*   **Verification:** GitHub repository links and contract hashes on Stellar.

#### **Tranche 2: Kinetic Terminal UI & Freighter Integration (Month 3-4)**
*   **Requested Funding:** $20,000 in XLM equivalent.
*   **Objective:** Release the high-speed Web3 telemetry terminal.
*   **Deliverables:**
    1.  Web3 frontend dashboard with Freighter wallet integration.
    2.  Real-time WebSocket telemetry for pool tracking.
    3.  A 3-minute video walkthrough demonstrating a liquidation loop.
*   **Verification:** Live UI URL and video demo link.

#### **Tranche 3: Keeper Network Expansion & Mainnet Launch (Month 5)**
*   **Requested Funding:** $25,000 in XLM equivalent.
*   **Objective:** Deploy the full protocol to Stellar Mainnet and publish the keeper daemon.
*   **Deliverables:**
    1.  Audited smart contract deployment on Stellar Mainnet.
    2.  Production-ready open-source `AutoBrokerDaemon` Docker image.
    3.  Third-party security audit report.
*   **Verification:** Mainnet contract addresses, keeper repository, and audit PDF.
