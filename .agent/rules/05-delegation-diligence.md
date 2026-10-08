# Rule 5: Claude Academy 4D Delegation-Diligence Loop
**Framework:** Problem & Platform Awareness -> Deliberate Delegation -> Continuous Diligence -> Dynamic Calibration
**Verification:** TypeSafe System One Semantic Integrity

## 1. Problem & Platform Awareness
Before delegating tasks to subagents or executing tools:
- Assess task reversibility (irreversible: push, deploy, send, delete shared data; reversible: local edits).
- Authorization gate: Irreversible actions require user's explicit words (`AUTH: user said "..."`).

## 2. Mandatory Diligence (Zero-Blind-Trust)
- Never accept agent or tool work on inference alone.
- Verify work via direct observation: exit code 0, test pass, endpoint ping, file existence.

## 3. Dynamic Authority Calibration
- Diligence failures automatically reduce agent autonomy.
- Repeated errors (>2) trigger immediate freeze and supervisor escalation.

## 4. Credential & Environment Isolation
- All secrets must reside in `~/.gemini/config/.env` with strict `600` permissions (`-rw-------`).
