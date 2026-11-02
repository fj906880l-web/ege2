---
name: context-aware-coding
description: IBM Technology Context-Aware Coding Framework meshed into Google Gemini & Antigravity IDE. Governs the 6 Agent Inputs (Code, Compact Repo Map, Lockfile Dependency Versions, Scoped Test Feedback Loop, GEMINI.md Docs, Developer Intent), the 3-Move Context Surfacing Loop (Interview, Explore & Explain, Plan & Explicit Assumptions), and U-Shaped Attention Context Hygiene to prevent Lost-in-the-Middle degradation.
version: 2.0.0
---

# Context-Aware Coding Skill (IBM Technology x Google Gemini / Antigravity)

## Overview
A single-sentence prompt cannot communicate years of architectural decisions, framework idioms, exact library versions, and testing conventions across a multi-file repository. This skill operationalizes **IBM Technology's Context-Aware Coding Framework** (*Legare Kerrison, "Context-Aware Coding: Give AI Agents the Right Context"*, `https://youtu.be/EkdIZXDnRK8`) directly inside the **Google Gemini / Antigravity IDE** ecosystem.

## CLI Tool & Engine
- **Script**: `/Users/malcolm/.gemini/config/scripts/context_aware_coder.py`
- **Binary Alias**: `context-aware-coder`
- **Project Manifest**: `.agents/context_map.json` (mirrored to `.agent/context_map.json`)

---

## 1. The 6 Mandatory Agent Context Inputs

Before modifying any project, ensure the agent is grounded in all 6 inputs:

1. **Relevant Existing Code (`repo-map --query`)**:
   - Point directly to existing reference patterns (e.g., *"Follow the pattern in `auth/login.py`"*).
2. **Compact Repository Map (`repo-map`)**:
   - Use AST-level file, class, function, and test-location maps (`.agents/context_map.json`) so the model sees the shape of the project without reading every line.
3. **Exact Lockfile Dependency Versions (`deps`)**:
   - Ground API usage in resolved lockfile versions (`package-lock.json`, `uv.lock`, `poetry.lock`, `requirements.txt`, `Cargo.lock`, `go.mod`). Many "hallucinated" functions are actually version mismatches (e.g. Pydantic v1 vs v2, React 18 vs 19).
4. **Executable Test Feedback Loop (`tests`)**:
   - Provide the exact scoped test command (`pytest tests/test_<module>.py -v`) so the agent operates in a closed **Write → Run → Fix** verification loop.
5. **Checked-In Instructions (`GEMINI.md` & `.agents/rules/*.md`)**:
   - Store repository conventions, build commands, and "do-not-touch" directory boundaries in `GEMINI.md` (strictly enforcing the **Google Gemini Workspace Invariant — Zero Claude Code Residue**).
6. **Developer Intent (`INTENT:` Gate)**:
   - Explicitly state what "done" looks like, hard constraints, and what the code must *not* do (`INTENT: code does <X>; task expects <Y>; GEMINI.md spec says <Z>`).

---

## 2. The 3-Move Context Surfacing Loop

When tackling a complex, ambiguous, or unfamiliar repository task (aligned with `/planning-vs-fast`):

```bash
python3 /Users/malcolm/.gemini/config/scripts/context_aware_coder.py interview --dir <project_path> --task "<task_description>"
```

1. **Move 1 — Interview (`Ask Missing Context`)**: Surface 1–3 pointed questions about edge cases, error formats, or boundary constraints before writing code.
2. **Move 2 — Explore & Explain (`Plain-Language Repo Map`)**: Summarize how the repository is put together in plain language so human and agent share a verified mental model.
3. **Move 3 — Plan & List Explicit Assumptions (`Assumptions Ledger`)**: List every load-bearing assumption before editing files, then write verified discoveries back into `GEMINI.md` upon completion:
   ```bash
   python3 /Users/malcolm/.gemini/config/scripts/context_aware_coder.py learn --dir <project_path> --lesson "<verified_convention>"
   ```

---

## 3. U-Shaped Attention Context Hygiene ("Lost in the Middle" Defense)

LLMs do not pay equal attention to all parts of a long context window—they attend strongest to the **Beginning** and **End**, and weakest to information buried in the **Middle** (*Liu et al., TACL*). Every irrelevant file (e.g., billing services or 3-week-old build logs when editing auth) competes with relevant tokens.

Use the `bundle` subcommand to assemble a task-filtered U-Shaped Context Bundle:

```bash
python3 /Users/malcolm/.gemini/config/scripts/context_aware_coder.py bundle --dir <project_path> --task "<task_description>" --raw
```

- **START OF CONTEXT (High Attention Anchor #1)**: Developer Intent (`INTENT:`), `GEMINI.md` Domain Invariants, and Explicit Load-Bearing Assumptions.
- **MIDDLE OF CONTEXT (Filtered Working Set)**: Task-filtered Compact Repo Map and relevant module symbols (all logs, build artifacts, and unrelated domains stripped).
- **END OF CONTEXT (High Attention Anchor #2)**: Exact Lockfile Dependency Versions + Scoped Executable Test Feedback Command.
