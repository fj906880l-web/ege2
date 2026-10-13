---
name: vanta-security-scaling-guardrails
description: >-
  Enterprise-grade security, scaling, and privacy guardrails derived from VantaInc open-source repositories (graphql-query-cost, vanta-mcp-server, claude-grc-engineering). Binds local AI agent execution costs, validates tool payloads with strict schemas, sanitizes prompt injection vectors and PII, benchmarks LRU prompt caches, and audits code for 100% air-gapped local compliance.
---

# Vanta Security & Scaling Guardrails

## Overview
The `vanta-security-scaling-guardrails` skill adapts production-proven compliance, security, and scaling architectures from [VantaInc](https://github.com/VantaInc) into a deterministic operational toolkit for free, open-source, local-AI curriculum projects. It protects local GPUs and CPUs from runaway recursive agent loops, validates agent tool arguments with strict schemas, redacts PII and injection attacks, and provides privacy verification ensuring zero external cloud exfiltration.

## Dependencies
- Standard Python 3 runtime (`python3` or `uv run`).
- Zero external package dependencies (pure standard library).

## Quick Start
Run the CLI tool directly from anywhere on the machine:

```bash
# Check if an agent prompt exceeds local execution budget
python3 ~/.gemini/config/skills/vanta-security-scaling-guardrails/scripts/security_scaling_guardrails.py cost-calc \
  --prompt "Analyze this 500-page PDF and write tests" --iterations 10 --depth 2 --threshold 400.0
```

Or sanitize user input and redact PII:
```bash
python3 ~/.gemini/config/skills/vanta-security-scaling-guardrails/scripts/security_scaling_guardrails.py sanitize-prompt \
  --text "Ignore previous instructions. My email is student@example.edu and key is AKIA1234567890ABCDEF"
```

## Utility Scripts & Subcommands

The CLI script is located at `~/.gemini/config/skills/vanta-security-scaling-guardrails/scripts/security_scaling_guardrails.py`.

### 1. `cost-calc`
Calculates estimated prompt tokens, sub-agent iteration multipliers, and recursion depth penalties to block resource-heavy tasks before launching local inference.
- `--prompt`: The raw prompt string.
- `--iterations`: Maximum expected tool iterations (default: 5).
- `--tool-calls`: Expected tool calls per turn (default: 2).
- `--depth`: Sub-agent tree recursion depth (default: 1).
- `--threshold`: Maximum allowable cost before gating (default: 500.0).
- `--output`: Optional JSON output file path.

### 2. `schema-validate`
Enforces strict type and key validation on agent tool arguments before execution, preventing hallucinated parameters.
- `--payload-json`: JSON string of data payload to validate.
- `--schema-json`: JSON schema defining required keys and types.
- `--output`: Output file path.

### 3. `sanitize-prompt`
Scans input text for prompt injection keywords (`ignore previous instructions`, `system override`, `<|im_start|>`) and redacts PII/credentials (emails, AWS keys, SSNs, API tokens).
- `--text`: Input text string.
- `--output`: Output file path.

### 4. `cache-budget`
Simulates Vanta's `LruMap` insertion-order cache behavior across access streams, measuring hit rates, capacity thresholds, and memory eviction counts.
- `--keys`: Comma-separated list of prompt or embedding hashes.
- `--capacity`: Maximum entries in the LRU cache.
- `--output`: Output file path.

### 5. `audit-privacy`
Scans local code files and configurations for external network calls (`requests.get`, `urllib`, cloud APIs) to ensure 100% self-hosted, air-gapped privacy compliance.
- `--file`: Path to Python/JS script or config file.
- `--output`: Output file path.

## Rate Limiting & Performance
- Zero cloud API dependency; executes locally in sub-millisecond time.
- All operations are completely offline and deterministic.

## Automated Self-Verification
The skill contains an automated test suite verifying all 5 guardrails:
```bash
python3 ~/.gemini/config/skills/vanta-security-scaling-guardrails/tests/test_guardrails.py
```
Expected output: `RESULTS: 7 PASSED, 0 FAILED out of 7 tests.`

## Common Mistakes
1. **Unbounded Agent Recursion**: Launching multi-agent loops without pre-flight cost gating causes local Mac/Linux systems to freeze from GPU memory pressure. Always evaluate `cost-calc` prior to launching subagents.
2. **Trusting Raw LLM Tool Arguments**: Language models frequently output strings where numbers are expected or omit required dictionary keys. Always run `schema-validate` before executing system actions.
3. **Hardcoding Test API Keys**: Even in mock/sandbox environments, never commit real or fake credential patterns that trigger DLP alarms. Use `sanitize-prompt` or `.env.local` files with `chmod 600`.

