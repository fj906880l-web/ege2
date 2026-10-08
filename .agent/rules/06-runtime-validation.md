# Rule 6: Rigorous Runtime Validation Protocol (Closing the Loop)
**Standard:** Grounded Runtime Proof
**Rule:** You are not done when code is written; you are done when execution is verified.

## 1. Test Suite Verification
- Run associated test suites (`pytest tests/`, `npm test`) after modifying any logic, risk, or execution layers.
- A passing targeted check with a broken overall build is a failed verification.

## 2. Telemetry & Metrics Verification
- Validate metrics collection by querying local Prometheus endpoints (`http://localhost:8000`) or health endpoints.
- Ensure telemetry payloads stream authentic, verifiable data.

## 3. Zero Live Execution Invariant
- Environment configuration must default strictly to mock/sandbox endpoints.
- Active production execution is prohibited unless manually toggled and confirmed by human operator.

## 4. Three-Strike Self-Correction Protocol
- Parse exact console traceback.
- Formulate fix preserving risk and safety invariants.
- Re-run test command.
- If failure persists after 3 attempts, halt and generate a "Diagnostic Report Artifact".
