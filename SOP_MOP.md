# EGE-2 Standard Operating Procedures (SOP) & Method of Procedure (MOP)

This document establishes formal **Standard Operating Procedures (SOP)** and **Methods of Procedure (MOP)** for operators, researchers, and engineers deploying and managing the **EGE-2 Quantum Epistemic System**.

---

## 📋 Standard Operating Procedures (SOP)

### SOP-01: Genesis Knowledge Ingestion Protocol
**Purpose:** Standardize the onboarding of verified scientific facts into the baseline Epistemic Q-Graph.

1. **Verify Evidence Tier:**
   - Must be supported by Tier 1 (Direct Telemetry) or Tier 2 (Controlled Scientific Experiment).
2. **Define Empirical Mechanism & Falsifiability:**
   - Every node must articulate the causal mechanism and explicit conditions under which the belief would be falsified.
3. **Generate Node & Seal Provenance:**
   ```python
   from ege2_quantum import EpistemicNode, EvidenceTier
   node = EpistemicNode(
       node_id="domain_constant_name",
       claim="Clear, unambiguous declarative statement of fact",
       domain="physics",
       evidence_tier=EvidenceTier.CONTROLLED_EXPERIMENT,
       confidence=0.999,
       mechanism="Empirical verification protocol (e.g. ISO/NIST standard)",
       falsifiability="Observable condition under which claim fails",
   )
   node.seal()
   graph.add_node(node)
   ```
4. **Run Unit Verification:** Execute `python3 -m unittest test_ege2_quantum.py`.

---

### SOP-02: User Model Drop-In & Calibration Workflow
**Purpose:** Safely connect, benchmark, and calibrate an external LLM or custom inference engine.

1. **Select Adapter:**
   - `OllamaAdapter`: Local edge models (Llama 3, Mistral, Phi-3).
   - `OpenAICompatibleAdapter`: vLLM, LMStudio, Groq, OpenRouter.
   - `CallableAdapter`: Custom Python functions or PyTorch neural models.
2. **Execute Benchmark Matrix:**
   ```bash
   python3 -c "from model_dropin import ModelBenchmarker, OllamaAdapter; b = ModelBenchmarker(OllamaAdapter('llama3')); b.run_benchmark()"
   ```
3. **Verify Epistemic Gate Performance:**
   - Ensure factual queries receive `ACCEPT` with high confidence.
   - Ensure adversarial urgency/manipulation prompts receive `REJECT` ($0.0\%$ confidence).
   - Ensure unverified assertions receive `CAUTION` with downgraded confidence.

---

### SOP-03: Quantum Superposition & Entanglement Management
**Purpose:** Manage superposed hypothesis lifecycles and consensus synchronization across distributed agents.

1. **Monitor Superposition Ratio:**
   - Inspect active superposed vs collapsed nodes:
     ```python
     stats = graph.stats()
     print(f"Superposed Nodes: {stats['superposed_nodes']} / {stats['active_nodes']}")
     ```
2. **Trigger Empirical Measurement:**
   - When new telemetry arrives, call `graph.measure_node(node_id)`.
   - Verify that entangled partner nodes collapse instantaneously to the corresponding eigenstate.

---

## 🛠️ Methods of Procedure (MOP)

### MOP-01: Full-Stack Containerized Production Deployment
**Purpose:** Step-by-step procedure for deploying the EGE-2 REST server and interactive web client in production.

#### Prerequisites:
- Docker $\ge 24.0$ & Docker Compose $\ge 2.20$ (or Python 3.9+)

#### Procedure:
1. **Clone and Verify Repository:**
   ```bash
   git clone https://github.com/fj906880l-web/ege2.git
   cd ege2
   ```
2. **Run Pre-Flight Security & Invariant Suite:**
   ```bash
   make test
   make security-audit
   ```
3. **Build and Launch Production Container:**
   ```bash
   make docker-build
   make docker-run
   ```
4. **Verify Health Endpoint:**
   ```bash
   curl -s http://localhost:8000/health | jq .
   ```
   *Expected Response:* `{"status": "healthy", "version": "2.0.0", "active_nodes": ...}`

---

### MOP-02: Cold-Start Disaster Recovery & Q-Graph State Restoration
**Purpose:** Recover persistent epistemic state following infrastructure failure or storage corruption.

#### Procedure:
1. **Locate Backup Snapshot:**
   - Identify latest verified state file: `epistemic_graph_backup.json`.
2. **Validate Cryptographic Provenance Chains:**
   ```python
   import json, hashlib
   with open("epistemic_graph_backup.json") as f:
       data = json.load(f)
   for nid, node in data["nodes"].items():
       # Recompute SHA-3 classical hash
       payload = json.dumps({
           "node_id": node["node_id"],
           "claim": node["claim"],
           "domain": node["domain"],
           "tier": node["evidence_tier"],
           "confidence": round(node["confidence"], 6),
           "version": node["version"],
           "mechanism": node.get("mechanism"),
           "created_at": node["created_at"]
       }, sort_keys=True)
       computed_hash = hashlib.sha3_256(payload.encode("utf-8")).hexdigest()
       assert computed_hash == node["immutable_hash"], f"Tamper detected in node {nid}!"
   print("✅ All cryptographic provenance chains verified 100% intact.")
   ```
3. **Re-initialize Epistemic Graph:**
   ```python
   from ege2_quantum import EpistemicGraph
   graph = EpistemicGraph(storage_path="epistemic_graph_backup.json")
   ```
4. **Verify Active Invariants:**
   - Execute test suite: `python3 -m unittest test_ege2_quantum.py`.
