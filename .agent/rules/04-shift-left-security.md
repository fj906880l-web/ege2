# Rule 4: IBM 5 Shift-Left Security & Safe Shell Guard
**Standard:** IBM 5 Shift-Left AI Security Principles & Zero-Trust Protocol
**Gating:** Security Score >= 80/100 Mandatory

## 1. The IBM 5 Principles
1. **P1: Fail-Safe Verification & Atomic State Writes:** Every state update, wash sale ledger, or risk state must use atomic replace (`os.replace` / atomic write). Zero fail-open risks.
2. **P2: Shift-Left Secrets Scanning & Git Hygiene:** Zero plain-text credentials, tokens, or private keys. Enforce `.gitignore` exclusion of `.env*`, `*.key`, `*.pem`, `*secret*`.
3. **P3: Supply-Chain Dependency Auditing:** Pin all dependencies explicitly. No vulnerable or deprecated packages (e.g. legacy `alpaca-trade-api`).
4. **P4: Business Intent & 50% Capital Cap:** Single-trade capital allocations must never exceed 50% equity. Enforce authentic order IDs.
5. **P5: Agentic Boundary Enclosure:** Block path traversal, unrestricted file write sinks, and external host bindings (`0.0.0.0` prohibited in sensitive listeners).

## 2. Pre-Execution Safe Shell Guard
Destructive shell commands (`rm -rf /`, raw disk writes, `mkfs`, fork bombs) are unconditionally blocked by `/Users/malcolm/.gemini/config/scripts/safe_shell_guard.py`.

## 3. Delivery Gating
If security score < 80, delivery is strictly blocked until remediated.
