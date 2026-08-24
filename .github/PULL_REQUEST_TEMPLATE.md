## 🛡️ EGE-2 Contribution & Pull Request Checklist

### 1. Branch Isolation & Purpose
- [ ] This PR originates from a dedicated feature/fix branch (e.g. `feature/xyz`, `fix/abc`, `security/audit`, `research/experiment`), **not directly from `main`**.
- [ ] Description of changes:

---

### 2. Epistemic Invariant & Safety Verification
- [ ] **Evidence Hierarchy Preservation:** Gated rules ($T_1 \dots T_7$) remain strictly intact (lower tiers cannot overwrite higher tiers).
- [ ] **Dual-Branch Isolation:** $\Phi$-Engine (causal physics) and $\Psi$-Engine (social intent) remain decoupled.
- [ ] **Automated Test Suite:** Ran `python3 -m unittest test_ege2_quantum.py -v` (All 21+ tests passing).
- [ ] **Model Drop-In Benchmark:** Ran `python3 model_dropin.py` (10/10 benchmarks passing).

---

### 3. Security & Privacy Assurance (Max Hardening)
- [ ] **Zero Exposed Secrets:** Scanned for API keys, bearer tokens, private keys, passwords, and `.env` files.
- [ ] **Zero Data Exfiltration / Privacy:** No third-party tracking, analytics, telemetry, or remote data exfiltration added.
- [ ] **Acceptable Use & Anti-Misuse:** Verified that proposed changes do not weaponize or facilitate automated deception, malicious persuasion, or illicit access.
