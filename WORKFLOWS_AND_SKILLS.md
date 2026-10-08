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

---

# Indexed Project & System Skills Catalog
**Registry:** Antigravity Skills Master Index

<skills>
- **agent-harness-v2**: Master runtime specification and operational skill for Agent Harness v2.0. Governs 4-Asset Memory Hub, ISTL continuous confidence scoring, Supervisor CEO layer, Security Gating (<80 block), and Mind Virus Inoculation.
  - Path: `/Users/malcolm/.gemini/config/skills/agent-harness-v2/SKILL.md`

- **shift-left-ai-security**: Enforce the IBM 5 Principles of Shift-Left Security for AI-generated code, agent workflows, and autonomous trading systems. Governs fail-safe execution, pre-commit secrets scanning, supply-chain dependency auditing, business intent validation (50% capital cap), and agentic boundary enclosure.
  - Path: `/Users/malcolm/.gemini/config/skills/shift-left-ai-security/SKILL.md`

- **ege2-quantum-epistemics**: Master operational skill for EGE-2 Quantum Epistemic System — 7 evidence tiers, dual-branch Phi/Psi/Sigma cognitive architecture, Anti-Sycophancy (Anti-Glazing) defense, Q-Graph with post-quantum provenance, quantum belief superposition, and QUBO arbitration.
  - Path: `/Users/malcolm/.gemini/config/skills/ege2-quantum-epistemics/SKILL.md`

- **delegation-diligence-loop**: Strategic execution and supervisory loop for AI agent delegation and continuous verification. Implements the Claude Academy Delegation-Diligence 4D framework combined with Fable Method, Agent Harness v2.0 supervision, and TypeSafe System One judgment verification.
  - Path: `/Users/malcolm/.gemini/config/skills/delegation-diligence-loop/SKILL.md`

- **harness-engineering**: Applies the principles of Agent Harness v2.0 and Harness Engineering to ensure high stability, automated supervision, security gating, and error correction.
  - Path: `/Users/malcolm/.gemini/config/plugins/elite-ai-skills-plugin/skills/harness-engineering/SKILL.md`

- **expert-testing-debugging**: Playbooks for writing test scripts, auditing accessibility, running headless audits, and diagnosing client/server-side errors.
  - Path: `/Users/malcolm/.gemini/config/plugins/elite-ai-skills-plugin/skills/expert-testing-debugging/SKILL.md`

- **ui-pro-max**: Guide for premium, dopamine-inducing UI design. Focuses on HSL color harmony, glassmorphism, micro-animations, typography, and responsive layouts.
  - Path: `/Users/malcolm/.gemini/config/plugins/elite-ai-skills-plugin/skills/ui-pro-max/SKILL.md`

- **subagent-orchestration**: Guidelines for defining, launching, communicating with, and managing background subagents to coordinate complex tasks.
  - Path: `/Users/malcolm/.gemini/config/plugins/elite-ai-skills-plugin/skills/subagent-orchestration/SKILL.md`

- **social-media-vision-board**: Social Media Vision Board & High-Engagement Content Playbook for Quant, Trading, Crypto, and Options content generation. Enforces dark mode styling, curiosity hooks, visual asset archetypes, weekly content calendars, and mandatory NFA/SEC legal disclaimers.
  - Path: `/Users/malcolm/.gemini/config/skills/social-media-vision-board/SKILL.md`

- **generative-media-studio**: Multi-modal generative media studio for AI agents. Generates full 60s/90s vertical short videos, high-CTR thumbnails, voiceovers, video clipping/shorts creation, and social syndication packages.
  - Path: `/Users/malcolm/.gemini/config/skills/generative-media-studio/SKILL.md`

- **web-scraping-mcp**: Practical web scraping workflows with no paid APIs and zero third-party Python dependencies. Exposes search_sources, scrape_page, extract_links, extract_json_ld, extract_table, and crawl_site tools.
  - Path: `/Users/malcolm/.gemini/config/skills/web-scraping-mcp/SKILL.md`

- **skillopt**: Self-evolving skill optimization framework for AI agents based on Microsoft SkillOpt and OKF (Observable Knowledge Framework) standards. Optimizes natural-language SKILL.md documents using trajectory reflection, patch aggregation, bounded editing, and validation gating without model fine-tuning.
  - Path: `/Users/malcolm/.gemini/config/skills/skillopt/SKILL.md`

- **robinhood-for-agents**: Complete Robinhood programmatic trading and portfolio management suite for stocks, options, and crypto with real-time Greeks, order placement, and scanner support.
  - Path: `/Users/malcolm/.gemini/config/skills/robinhood-for-agents/SKILL.md`

- **bigquery**: BigQuery query optimization (SQL), BigFrames Python code, BigQuery ML/AI functions (SQL & Python), and Graph Analytics (GQL & Property Graphs).
  - Path: `/Users/malcolm/.gemini/config/skills/bigquery/SKILL.md`

- **firestore-data**: NoSQL document operations, collection hierarchy exploration, CRUD tasks, and data retrieval.
  - Path: `/Users/malcolm/.gemini/config/skills/firestore-data/SKILL.md`
</skills>
