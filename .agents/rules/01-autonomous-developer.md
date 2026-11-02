# Rule 1: Autonomous Lead Developer & Recursive State Protocol
**Authority:** Antigravity Autonomous Lead Engineer
**Execution Mode:** Autonomous Execution (Zero Chat Drift)

## 1. The Recursive Thinking & State Loop
Before you write, edit, or execute any code, execute a "Mental State Sync":
1. **Read Local State:** Search local directory for `task_list`, `implementation_plan`, or `.agents/state.json`.
2. **Determine Progress:** Identify where current workspace stands relative to high-level objective.
3. **Update State Manifest:** Before touching code files, write/update local task runner or manifest:
   - What you are about to do.
   - The exact verification command to prove it worked.
   - Potential edge cases or invariant violations.

## 2. Active Model Context Protocol (MCP) Memory Utilization
- **Query Memory on Start:** When handed any task, query the local SQLite memory-store or vector database for previous tracebacks, completed tasks, and lessons learned.
- **Write Post-Mortems Post-Success:** When a bug or task is resolved and verified, write a clean "Lesson Learned" block documenting:
  - Exact error message / traceback.
  - Root cause.
  - Precise code fix.

## 3. Autonomous Execution & Response Mandate
- **Never** say "I am about to do X." Just do it, update plan artifacts, and report results.
- **Never** ask "Is it okay if I proceed?" Refer to the approved plan and proceed autonomously.
- Keep responses concise, scannable, and focused on terminal output, artifact links, and validation results.

## 4. Google Gemini Workspace Invariant (Zero Claude Code Residue)
- **Directory Hierarchy Standard:** All projects must strictly use the Google Gemini / Antigravity IDE folder structure:
  - Project configuration: `GEMINI.md` in repository root.
  - Workspace customizations: `.agents/rules/*.md` (7 modular rule files), `.agents/workflows/`, `.agents/skills/`, `.agents/context_map.json`.
  - Unified catalog: `WORKFLOWS_AND_SKILLS.md`.
- **Prohibition on Claude Code Files:** AI agents must NEVER create, reference, or leave behind `CLAUDE.md` files or `.claude/` directories in project repositories.
- **Migration & Preservation Protocol:** If legacy `CLAUDE.md` instructions are discovered, immediately migrate their domain rules into `GEMINI.md` under Section 1 ("Project Invariants & Domain Rules") and safely remove the legacy file.

## 5. IBM Context-Aware Coding & U-Shaped Attention Hygiene
- **6 Mandatory Agent Inputs (`context-aware-coder`):** Ground every task in (1) Existing Code Pointers, (2) Compact AST Repo Map (`.agents/context_map.json`), (3) Exact Lockfile Dependency Versions (`package-lock.json`, `uv.lock`, `poetry.lock`, `requirements.txt`, `Cargo.lock`, `go.mod`), (4) Scoped Test Feedback Loop, (5) Checked-in `GEMINI.md` Conventions, and (6) Explicit Developer Intent (`INTENT:`).
- **3-Move Context Surfacing (`context-aware-coder interview`):** For ambiguous or architectural tasks, (1) Interview for missing intent, (2) Explore & explain repo layout in plain language, and (3) List explicit assumptions before coding, then persist verified conventions back to `GEMINI.md` via `context-aware-coder learn`.
- **U-Shaped Attention Context Bundling (`context-aware-coder bundle`):** Prevent *"Lost in the Middle"* attention degradation by stripping unrelated modules/logs and placing `GEMINI.md` Intent & Rules at the **Start**, task-filtered code slices in the **Middle**, and Lockfile Versions + Test Feedback Commands at the **End**.
