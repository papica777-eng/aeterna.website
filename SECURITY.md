# Security Policy — AETERNA Sovereign Cognitive Engine

## Supported Versions & Frameworks

| Subsystem / Layer | Release / Status | Supported |
| :--- | :--- | :---: |
| **AETERNA Core Engine (Rust NAPI)** | `v0.1.0+` (Deterministic zero-copy) | :white_check_mark: |
| **AETERNA Virtual Human Twin (VHT)** | `TRL-7` Clinical Oncology & Longevity HUDs | :white_check_mark: |
| **UKAME / OMNI-VIVISECTOR** | 4-State Catuṣkoṭi Formal Verification Engine | :white_check_mark: |
| **FastAPI Backend Gateway (`backend/server.py`)** | License Verification & Deterministic Dispatch | :white_check_mark: |
| **Client Web HUDs & Visualizers** | Single-File Deterministic Client Workspaces | :white_check_mark: |

---

## Cryptographic & Security Guarantees

1. **Deterministic Execution:**
   All core arithmetic and state transitions are verified for $\Delta S = 0.0000$ entropy. Financial license computations are strictly handled using atomic fixed-precision integers.
2. **Post-Quantum Cryptography (PQC):**
   Tactical communication and satellite laser mesh prototypes utilize NIST-standardized quantum-resistant algorithms:
   * **ML-KEM-1024** (`pqcrypto-kyber`)
   * **ML-DSA-87** (`pqcrypto-dilithium`)
3. **One-Shot Consumable Licensing:**
   License keys follow deterministic SHA-256 cryptographic signatures and are permanently burned after execution (`aeterna_consumed_license_keys`), preventing replay attacks.

---

## Reporting a Vulnerability

We prioritize responsible disclosure and immediate cryptographic remediation for all discovered vulnerabilities.

* **Principal Investigator & Lead Architect:** Dimitar Stavrev Prodromov
* **Direct Secure Channel:** `papica777@gmail.com`
* **ORCID ID:** [`0009-0004-8070-1348`](https://orcid.org/0009-0004-8070-1348)
* **Consortium PIC Code:** `865986222` (AETERNA Technologies)

### Response Timelines:
* **Initial Acknowledgment:** Within 12 hours.
* **Triage & Formal Vivisection:** Within 24 hours.
* **Deterministic Hotfix Deployment:** Within 48 hours.
