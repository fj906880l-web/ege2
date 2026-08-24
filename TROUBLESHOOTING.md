# EGE-2 Troubleshooting Guide & Diagnostic Ladder

This guide provides step-by-step diagnostic workflows, error code references, and resolution procedures for the **EGE-2 Quantum Epistemic System**.

---

## 🚦 Quick Diagnostic Health Check

Run the comprehensive local diagnostic verification suite:

```bash
# 1. Verify Core Test Suite (All 21 tests should pass)
python3 -m unittest test_ege2_quantum.py -v

# 2. Run Model Drop-In Benchmark Suite
python3 -c "from model_dropin import ModelBenchmarker, MockLLM; res = ModelBenchmarker(MockLLM()).run_benchmark(verbose=False); print('Accuracy:', res['accuracy_pct'], '%')"

# 3. Test Full-Stack Server Health Endpoint
python3 -c "import urllib.request, json; resp = urllib.request.urlopen('http://localhost:8000/health'); print(json.loads(resp.read().decode()))"
```

---

## 🔍 Common Issues & Resolution Matrix

### 1. `REJECTED_TIER_MISMATCH`
- **Symptom:** `graph.update_belief()` returns `REJECTED_TIER_MISMATCH: Tier 7 cannot overwrite Tier 1`.
- **Root Cause:** A lower-tier claim (e.g. $T_7$ conversational input or $T_6$ secondhand rumor) attempted to mutate or supersede a higher-tier node ($T_1$ Direct Telemetry or $T_2$ Controlled Experiment).
- **Resolution:**
  - This is an **expected safety invariant**, not a bug.
  - To legitimately update a node, provide equal or higher-quality evidence ($T_{\text{new}} \le T_{\text{current}}$), such as reproducible experimental telemetry or verified peer consensus.

---

### 2. `INVESTIGATION_TRIGGERED: Direct contradiction detected`
- **Symptom:** Belief update is paused and flagged with `INVESTIGATION_TRIGGERED`.
- **Root Cause:** The new claim contains propositions directly contradicting existing active nodes in the same domain (e.g. claiming water boils at 50°C at 1 atm).
- **Resolution:**
  - Review conflicting node IDs returned in the error payload.
  - Run QUBO arbitration to evaluate global coherence across the competing hypotheses:
    ```python
    from ege2_quantum import QUBOArbitration
    qubo = QUBOArbitration([conflicting_node_a, new_node_b])
    solution = qubo.solve_simulated_annealing()
    ```

---

### 3. `[Ollama Connection Error: ... Is Ollama running on http://localhost:11434?]`
- **Symptom:** `OllamaAdapter` returns connection refused or timeout errors.
- **Root Cause:** Local Ollama daemon is stopped or listening on a non-standard port.
- **Resolution:**
  1. Start Ollama in your terminal:
     ```bash
     ollama serve
     ```
  2. Verify your desired model is pulled and ready:
     ```bash
     ollama pull llama3
     ollama run llama3 "Hello"
     ```
  3. Re-run `python3 model_dropin.py`.

---

### 4. Port 8000 Already in Use (`[Errno 48] Address already in use`)
- **Symptom:** `server.py` fails to bind to port 8000.
- **Root Cause:** Another process or development server is using port 8000.
- **Resolution:**
  - Launch `server.py` on a custom port via the `PORT` environment variable:
    ```bash
    PORT=8080 python3 server.py
    ```
  - Or find and terminate the occupying PID:
    ```bash
    lsof -i :8000
    kill -9 <PID>
    ```

---

### 5. Quantum Superposition State Not Collapsing
- **Symptom:** `node.quantum_state.measured` remains `False` after querying.
- **Root Cause:** By design, standard read queries (`query()`) do **not** collapse superposition states to preserve unmeasured hypothesis uncertainty.
- **Resolution:**
  - To explicitly trigger measurement collapse, call:
    ```python
    graph.measure_node("node_id")
    ```
  - Measurement collapses the state vector $|\psi\rangle$ into a classical eigenstate (`True` or `False`) according to the Born probability rule.

---

### 6. Git Pre-Commit Hook Rejection
- **Symptom:** `git commit` fails with `❌ ERROR: Potential API key or private secret detected in staged commit!`
- **Root Cause:** Staged changes contain strings matching high-entropy secret patterns (e.g. OpenAI `sk-...` keys, GitHub tokens, or private SSH keys).
- **Resolution:**
  - Remove all hardcoded credentials from the files.
  - Store sensitive keys in local ignored environment files (`.env`).
  - Verify your `.gitignore` includes `*.env`, `*.key`, and `credentials.json`.
