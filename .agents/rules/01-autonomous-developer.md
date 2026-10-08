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
