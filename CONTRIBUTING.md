# Contributing to EGE-2 Quantum Epistemic System

Thank you for your interest in contributing to the **EGE-2 Quantum Epistemic System**! To maintain absolute epistemic integrity, prevent regression of core invariants, and protect user security and privacy, all contributors must adhere to the following protocols.

---

## 🌿 Strict Branching Policy

To protect the codebase and maintain verifiable release provenance:

1. **Never commit directly to `main`:**
   - The `main` branch is protected and reserved strictly for audited, tested releases.
   - All contributions, bug fixes, experiments, and audits must be developed on a **separate isolated branch**.
2. **Branch Naming Conventions:**
   - `feature/<feature-name>`: New capabilities, adapters, or dataset expansions.
   - `fix/<issue-name>`: Bug fixes or resolution of failing tests.
   - `security/<audit-name>`: Cryptographic upgrades, vulnerability fixes, or hardening.
   - `research/<experiment-name>`: Epistemic theory, quantum simulation, or math optimizations.
   - `chore/<task-name>`: Documentation, formatting, or repository maintenance.

### Quick Workflow:

```bash
# 1. Ensure your local main is up to date
git checkout main
git pull origin main

# 2. Create and switch to your separate feature branch
git checkout -b feature/my-new-adapter

# 3. Make your edits and verify all tests pass
python3 -m unittest test_ege2_quantum.py -v
python3 model_dropin.py

# 4. Commit with descriptive semantic messages
git commit -m "feat(adapter): add support for custom ONNX runtime"

# 5. Push to your branch and open a Pull Request
git push origin feature/my-new-adapter
```

---

## 🔒 Security & Privacy Rules ("Security on 10")

1. **Zero Secret Policy:**
   - Never commit API keys, personal access tokens, private keys (`.pem`, `.key`), `.env` files, or production credentials.
   - All automated CI jobs will fail if secret patterns are detected.
2. **Zero Telemetry & Absolute Privacy:**
   - EGE-2 is designed for 100% offline, local, edge, or air-gapped deployment.
   - Do not introduce remote telemetry, tracking beacons, analytics endpoints, or unconsented network calls.
3. **Anti-Malicious Gating:**
   - EGE-2's $\Psi$-Engine and $\Sigma$-Cortex are specifically architected to detect and resist manipulation, propaganda, and adversarial attacks. Contributions that weaken manipulation detection or bypass evidence tier gating will be rejected.

---

## 🧪 Testing & Verification Mandate

Every Pull Request must pass the full verification matrix:

```bash
# Run unit and integration tests
python3 -m unittest test_ege2_quantum.py -v

# Run model drop-in benchmark suite
python3 -c "from model_dropin import ModelBenchmarker, MockLLM; res = ModelBenchmarker(MockLLM()).run_benchmark(False); assert res['accuracy_pct'] == 100.0"

# Verify standalone execution
python3 ege2_quantum.py
```

---

## ⚠️ Disclaimers & Licensing

All contributions are subject to the [MIT License](LICENSE) and must adhere to the legal and operational guardrails set forth in [`DISCLAIMER.md`](DISCLAIMER.md) and [`ACCEPTABLE_USE.md`](ACCEPTABLE_USE.md).
