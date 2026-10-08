# Rule 7: Iterative Semi-Trust Learning (ISTL) & Supervisor Layer
**Framework:** Graded Confidence & Supervisory Governance
**Confidence Range:** [0.00, 0.99] (Absolute 1.0 Forbidden)

## 1. Graded Confidence Updates
- Success on independent verification: +0.08 confidence.
- Contradiction / test failure: -0.18 confidence.
- Outlier / unmodeled behavior: -0.35 confidence.
- Bound: Maximum 5 passes or delta < 0.05 convergence.

## 2. In-Silico Perturbation Testing
Simulate assumption negation, input noise, and tool failure before executing high-stakes transactions. If confidence collapses (>0.30 drop), halt for review.

## 3. CEO Supervisor Layer Interventions
The Supervisor intervenes when:
- Worker confidence falls below 0.30.
- Same failure repeated >= 2 times.
- Execution deviates > 2 steps from approved plan.
- Security score drops below 50.
- Mind virus or unverified propagation detected.
