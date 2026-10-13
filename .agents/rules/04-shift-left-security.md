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

## 3. Vanta Security & Scaling Guardrails Protocol
**Standard:** VantaInc Open-Source Architectural Patterns (Cost-Bounding, Zod Schema Gating, PII Redaction, Air-Gapped Privacy)
**CLI Command:** `vanta-guardrails <cost-calc|schema-validate|sanitize-prompt|cache-budget|audit-privacy>`
1. **Execution Cost Bounding (`cost-calc`):** Bound prompt tokens, tool iterations, and recursion depth to prevent runaway subagent loops.
2. **Tool Argument Schema Validation (`schema-validate`):** Strict type and key validation on all tool payloads prior to execution.
3. **Prompt Injection & DLP Sanitization (`sanitize-prompt`):** Strip instruction overrides and redact sensitive PII (emails, AWS keys, SSNs, API tokens).
4. **LRU Cache Budget Simulator (`cache-budget`):** Measure hit ratios and capacity thresholds under insertion-order eviction.
5. **Air-Gapped Privacy Audit (`audit-privacy`):** Guarantee 100% self-hosted, air-gapped compliance with zero external cloud egress.

## 4. Delivery Gating
If security score < 80 or Vanta scaling guardrails are violated, delivery is strictly blocked until remediated.
