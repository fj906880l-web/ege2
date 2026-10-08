# Available Slash Command Workflows
**Protocol:** Antigravity Workflows & Operational Slash Commands

<workflows>
- **/goal <task>**: Autonomous goal-directed execution loop. Designed for long-running or overnight tasks; executes continuously with auto-recovery and diligence verification until the goal is fully achieved.
  - Path: `builtin/commands/goal`
  - Trigger: `/goal`
  - Usage: `/goal execute complete end-to-end integration and verified test suite`

- **/schedule <cron_or_seconds> <prompt>**: Schedules a one-shot timer or recurring background cron trigger.
  - Path: `builtin/commands/schedule`
  - Trigger: `/schedule`
  - Usage: `/schedule cron="0 * * * *" prompt="Run hourly system health check"`

- **/plan <task>**: Complex task decomposition and formal implementation planning. Generates structured architecture, risk assessment, and verification steps before execution.
  - Path: `builtin/commands/plan`
  - Trigger: `/plan`
  - Usage: `/plan design new multi-broker order router`

- **/grill-me <topic>**: Interactive interview mode where the agent asks pointed, high-value questions to resolve design ambiguities, clarify trade-offs, and align on architecture.
  - Path: `builtin/commands/grill-me`
  - Trigger: `/grill-me`
  - Usage: `/grill-me review trade allocation risk model`

- **/learn <lesson>**: Captures and persists operational lessons, bug post-mortems, and corrected developer behaviors into permanent MCP local memory.
  - Path: `builtin/commands/learn`
  - Trigger: `/learn`
  - Usage: `/learn always verify Oanda v20 datetime ISO8601 formatting`

- **/fable-method <task>**: Full 7-stage evidence-based engineering loop (Step 0 Classify, Step 1 Define Done, Step 2 Gather Evidence, Step 3 Decide, Step 4 Act, Step 5 Verify, Step 6 Report).
  - Path: `~/.gemini/config/skills/fable-method/SKILL.md`
  - Trigger: `/fable-method`
  - Subcommands:
    - `/fable-method plan <task>`: Steps 0-3 only (classify, define done, gather evidence, deliver plan, stop).
    - `/fable-method audit`: Grades work already completed in session against the loop.
    - `/fable-method report`: Rewrites pending response into Step 6 outcome-first executive format.
</workflows>
