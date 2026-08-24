# Comprehensive Troubleshooting & Diagnostic Manual
## EGE-2: Epistemic Growth Engine & Quantum Epistemic System

---

## 📑 Diagnostic Ladder & Index
- [Level 1: System Boot, Runtime & Port Diagnostics](#level-1-system-boot-runtime--port-diagnostics)
- [Level 2: Model Adapter & Drop-In Connectivity](#level-2-model-adapter--drop-in-connectivity)
- [Level 3: Epistemic Graph & Invariant Rejection Errors](#level-3-epistemic-graph--invariant-rejection-errors)
- [Level 4: Quantum Computing & Superposition Anomalies](#level-4-quantum-computing--superposition-anomalies)
- [Level 5: Dual-Branch Cognitive Processing Errors ($\Phi, \Psi, \Sigma$)](#level-5-dual-branch-cognitive-processing-errors-phi-psi-sigma)
- [Level 6: Security, Secret Leaks & Git Hook Failures](#level-6-security-secret-leaks--git-hook-failures)
- [Level 7: Performance, Concurrency & High-Load Optimization](#level-7-performance-concurrency--high-load-optimization)
- [Comprehensive Error Code Glossary (EGE-001 to EGE-030)](#comprehensive-error-code-glossary)

---

## 🚀 Pre-Flight Diagnostic Health Check

Before troubleshooting individual modules, execute the automated 3-stage validation suite:

```bash
# Stage 1: Automated Unit & Invariant Test Suite (25 Tests)
python3 -m unittest test_ege2_quantum.py -v

# Stage 2: 10-Prompt Epistemic & Energy Benchmark
python3 -c "from model_dropin import ModelBenchmarker, MockLLM; res = ModelBenchmarker(MockLLM()).run_benchmark(verbose=True); assert res['accuracy_pct'] == 100.0"

# Stage 3: Security & Secret Leak Pre-Flight Audit
python3 -c "import os; assert os.system('grep -rn -E \"(AIza[0-9A-Za-z-_]{35}|sk-[a-zA-Z0-9]{32,}|ghp_[a-zA-Z0-9]{36})\" . --exclude-dir=.git --exclude-dir=__pycache__') != 0, 'Secrets found!'"
```

---

## Level 1: System Boot, Runtime & Port Diagnostics

### Problem 1.1: `[Errno 48] Address already in use` (Port Conflict)
- **Symptom:** Executing `python3 server.py` terminates with `OSError: [Errno 48] Address already in use`.
- **Root Cause:** Another process (e.g. an existing EGE-2 background instance, Node.js server, or NGINX) is listening on port 8000.
- **Diagnostic Command:**
  ```bash
  lsof -i :8000
  ```
- **Resolution:**
  1. **Option A (Terminate occupying PID):**
     ```bash
     kill -9 $(lsof -t -i :8000)
     ```
  2. **Option B (Bind to alternative port via environment variable):**
     ```bash
     PORT=8080 python3 server.py
     ```

---

### Problem 1.2: Python Version Mismatch (`SyntaxError` or Missing Stdlib Modules)
- **Symptom:** Syntax errors on type annotations (`list[str]` or `|` union operators) or module import failures.
- **Root Cause:** Running with Python $\le 3.8$. EGE-2 requires Python $3.9+$ (Python $3.10+$ recommended).
- **Diagnostic Command:**
  ```bash
  python3 --version
  ```
- **Resolution:**
  - Ensure your active environment is Python 3.9+:
    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

---

## Level 2: Model Adapter & Drop-In Connectivity

### Problem 2.1: `[Ollama Connection Error: HTTPConnectionPool ... Connection refused]`
- **Symptom:** `OllamaAdapter` returns fallback strings or connection errors during evaluation.
- **Root Cause:** The local Ollama daemon is not running, or is bound to a custom port/host.
- **Diagnostic Command:**
  ```bash
  curl -s http://localhost:11434/api/tags
  ```
- **Resolution:**
  1. Start the Ollama background daemon:
     ```bash
     ollama serve
     ```
  2. Ensure the required model is downloaded:
     ```bash
     ollama pull llama3
     ```
  3. Verify connectivity in Python:
     ```python
     from model_dropin import OllamaAdapter
     adapter = OllamaAdapter(model_name="llama3", base_url="http://localhost:11434")
     print(adapter.generate("Ping test"))
     ```

---

### Problem 2.2: OpenAI-Compatible Server Timeout (`vLLM / LMStudio / Groq`)
- **Symptom:** `OpenAICompatibleAdapter` times out after 10 seconds or returns HTTP 401/404.
- **Root Cause:** Incorrect endpoint URL (missing `/v1/chat/completions`) or invalid API key headers.
- **Resolution:**
  - Verify endpoint URL configuration:
    ```python
    from model_dropin import OpenAICompatibleAdapter
    adapter = OpenAICompatibleAdapter(
        base_url="http://localhost:1234/v1", # LMStudio or vLLM
        model_name="local-model",
        api_key=None
    )
    ```

---

## Level 3: Epistemic Graph & Invariant Rejection Errors

### Problem 3.1: `REJECTED_TIER_MISMATCH: Tier 7 cannot overwrite Tier 1`
- **Symptom:** Attempting to update a belief node fails with a rejection status.
- **Root Cause:** **The 7-Tier Evidence Invariant.** A lower-tier assertion ($T_7$ conversational claim) is attempting to mutate or delete a higher-tier node ($T_1$ Direct Telemetry or $T_2$ Controlled Experiment).
- **Resolution:**
  - This is a **core safety feature**, not an error.
  - If new empirical evidence has emerged, provide the update with equal or higher evidence rank ($T_{\text{new}} \le T_{\text{current}}$) and include empirical mechanism telemetry.

---

### Problem 3.2: `INVESTIGATION_TRIGGERED: Direct contradiction detected`
- **Symptom:** Node insertion is paused, and `INVESTIGATION_TRIGGERED` is returned.
- **Root Cause:** The proposed claim directly conflicts with an active node in the same domain.
- **Resolution:**
  - Retrieve the conflicting node IDs from the response payload.
  - Run **QUBO Global Coherence Arbitration** to resolve network consistency:
    ```python
    from ege2_quantum import QUBOArbitration
    conflicting_nodes = [graph.nodes["existing_id"], new_candidate_node]
    qubo = QUBOArbitration(conflicting_nodes)
    solution = qubo.solve_simulated_annealing(iterations=2000)
    print("Coherent subset:", [n.node_id for i, n in enumerate(conflicting_nodes) if solution[i]])
    ```

---

## Level 4: Quantum Computing & Superposition Anomalies

### Problem 4.1: Quantum Superposition State Non-Normalization
- **Symptom:** `AssertionError: State vector $|\alpha|^2 + |\beta|^2 \ne 1$` during custom belief initialization.
- **Root Cause:** Raw probability amplitudes were passed without normalizing $|\alpha|^2 + |\beta|^2 = 1$.
- **Resolution:**
  - Use the built-in `QuantumBeliefState.from_confidence(P)` factory, which automatically computes normalized amplitudes:
    ```python
    from ege2_quantum import QuantumBeliefState
    q_state = QuantumBeliefState.from_confidence(0.85)
    # Automatically computes: alpha = sqrt(0.85), beta = sqrt(0.15)
    ```

---

### Problem 4.2: Entanglement Consensus Not Propagating Across Swarm
- **Symptom:** Measuring Node A on Agent 1 does not collapse entangled Node B on Agent 2.
- **Root Cause:** Bell pair mapping was not registered in `node.entangled_with`.
- **Resolution:**
  - Register the bidirectional entanglement relationship before measurement:
    ```python
    graph.entangle_nodes("node_a_id", "node_b_id")
    # Now measuring node_a automatically collapses node_b
    graph.measure_node("node_a_id")
    ```

---

## Level 5: Dual-Branch Cognitive Processing Errors ($\Phi, \Psi, \Sigma$)

### Problem 5.1: $\Psi$-Engine False Positives on Technical Jargon
- **Symptom:** A legitimate urgent query (e.g. *"URGENT: Server CPU throttling at 99%"*) is downgraded with `CAUTION`.
- **Root Cause:** The $\Psi$-Engine matched the keyword "URGENT" as emotional pressure.
- **Resolution:**
  - The $\Sigma$-Cortex verifies that if the underlying technical claim in the $\Phi$-Engine is verified ($T_1$), the query is still accepted (`ACCEPT`), but accompanied by an explicit intent transparency note.

---

## Level 6: Security, Secret Leaks & Git Hook Failures

### Problem 6.1: Git Pre-Commit Hook Blocks Commit (`Potential secret detected`)
- **Symptom:** `git commit` is blocked by `.githooks/pre-commit`.
- **Root Cause:** Staged changes contain strings matching high-entropy API key patterns (`AIza...`, `sk-...`, `ghp_...`) or private key blocks.
- **Resolution:**
  1. Inspect staged changes:
     ```bash
     git diff --cached
     ```
  2. Remove hardcoded keys and place them in an ignored `.env` file.
  3. Verify `.gitignore` contains `.env*` and `credentials.json`.

---

## Level 7: Performance, Concurrency & High-Load Optimization

### Problem 7.1: Graph Lookup Latency on Large Datasets ($>100,000$ Nodes)
- **Symptom:** `graph.query()` latency increases past 50ms.
- **Root Cause:** Unindexed linear scan over all nodes in memory.
- **Resolution:**
  - Query using domain-specific partitions:
    ```python
    # Fast indexed lookup by domain:
    physics_nodes = graph.domain_index.get("physics", [])
    ```

---

## Comprehensive Error Code Glossary

| Error Code | Hex Code | Component | Description & Permanent Remedy |
|:---|:---:|:---:|:---|
| `EGE-001` | `0x101` | Evidence Gating | **Tier Overwrite Violation:** Lower evidence tier attempted to overwrite higher tier. *Remedy: Submit update with $T_{\text{new}} \le T_{\text{current}}$.* |
| `EGE-002` | `0x102` | Epistemic Graph | **Direct Contradiction:** Candidate claim logically contradicts active $T_1/T_2$ fact. *Remedy: Run QUBO arbitration.* |
| `EGE-003` | `0x103` | Quantum Engine | **State Vector Denormalization:** $|\alpha|^2 + |\beta|^2 \ne 1$. *Remedy: Use `QuantumBeliefState.from_confidence()`.* |
| `EGE-004` | `0x104` | $\Psi$-Engine | **Adversarial Urgency Detected:** Heavy emotional or coercive prompt injection. *Remedy: $\Sigma$-Cortex executes hard rejection.* |
| `EGE-005` | `0x105` | $\Psi$-Engine | **Authority Intimidation Vector:** False credential or coercive override attempted. *Remedy: Enforce evidence gating.* |
| `EGE-006` | `0x106` | Model Adapter | **Ollama Connection Refused:** Port 11434 unreachable. *Remedy: Run `ollama serve`.* |
| `EGE-007` | `0x107` | Model Adapter | **OpenAI Endpoint Timeout:** HTTP request timed out after 10s. *Remedy: Verify API endpoint & network route.* |
| `EGE-008` | `0x108` | Cryptography | **Provenance Hash Mismatch:** Node SHA-3-256 digest corrupted. *Remedy: Restore from verified backup.* |
| `EGE-009` | `0x109` | Cryptography | **Dilithium Signature Verification Failure:** Post-quantum lattice signature invalid. *Remedy: Check keypair.* |
| `EGE-010` | `0x10A` | Server Core | **Port Binding Conflict:** Port 8000 already in use. *Remedy: Specify custom `PORT=8080`.* |
| `EGE-011` | `0x10B` | QUBO Solver | **Annealing Divergence:** Simulated Annealing exceeded maximum iterations without finding minimum. *Remedy: Increase iterations to 5000.* |
| `EGE-012` | `0x10C` | Entanglement | **Orphan Bell Pair:** Entangled node ID not found in active graph. *Remedy: Clean up dangling references.* |
| `EGE-013` | `0x10D` | Serialization | **JSON Roundtrip Deserialization Error:** Malformed node payload. *Remedy: Validate schema against `EpistemicNode.to_dict()`.* |
| `EGE-014` | `0x10E` | Security | **Exposed Secret Detected:** Pre-commit hook blocked key commit. *Remedy: Move token to `.env`.* |
| `EGE-015` | `0x10F` | Multi-Agent | **Byzantine Sybil Attempt:** Low-tier consensus flooding detected. *Remedy: Discard $T_7$ votes in favor of $T_2$ telemetry.* |

---

## ⚠️ Disclaimers & Operational Notice

This troubleshooting guide is provided for informational and debugging purposes only. EGE-2 is research software provided "as is" under the [MIT License](LICENSE). For full disclaimers regarding liability, financial applications, and medical claims, see [`DISCLAIMER.md`](DISCLAIMER.md).
