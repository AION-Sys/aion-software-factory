# Factory Architecture

How the AION Software Factory itself is built. This describes the *platform*, not
any product the factory produces.

## Design goals (in priority order)
1. **Traceability** — any mission's full history reconstructable from files.
2. **Clarity** — one obvious place for each thing.
3. **Modularity** — no hard coupling to a single vendor.
4. **Security** — least privilege; no secrets in the repo.
5. **Human oversight** — explicit approval gates.
6. **Repeatability** — every mission runs the same pipeline.
7. **Future autonomy** — designed toward it, not assuming it.

## The three layers

```
┌──────────────────────────────────────────────────────────────┐
│  1. GOVERNANCE  (rules the whole factory obeys)                │
│     AION_ENGINEERING.md · AGENTS.md · docs/operations/*        │
├──────────────────────────────────────────────────────────────┤
│  2. AGENTS      (the workforce + their contracts)              │
│     agents/{pm,architect,builder,qa,security}/CONTRACT.md      │
├──────────────────────────────────────────────────────────────┤
│  3. WORK        (missions flowing through the pipeline)        │
│     missions/MISSION-XXX/* driven by templates/* + docs/workflows/* │
└──────────────────────────────────────────────────────────────┘
```

Supporting: `scripts/` (traceability + validation), `docs/decisions/` (ADRs).

## Data model (files, not a database)

Per ADR-0002 there is **no database**. State lives in version-controlled files:

- **Mission state** — the metadata block in `mission.md` (`status`, `stage`).
- **Artifacts** — PRD / architecture / tasks / QA / security reports per mission.
- **Decisions** — ADRs in `docs/decisions/`.
- **Observability data** — see `../operations/observability.md`; measured from
  git history, mission metadata, and report verdicts, not a live metrics store.

This keeps the foundation dependency-free and auditable. A database or metrics
store is introduced only when a concrete mission proves the need (with an ADR).

## Vendor neutrality

The factory references AION's ecosystem (GitHub, Claude Code, Cursor, AWS,
Supabase, Vercel, agent runtime, Notion, Airtable, Slack) but couples tightly to
none. The only hard dependencies are **git + Markdown + Python stdlib**. Any
agent runtime that can read files and run the pipeline can operate the factory.

## Extensibility

- **New agent** → add `agents/<role>/CONTRACT.md` (nine-section schema), register
  it in `agents/README.md`, and insert its stage in the workflow. Only when a
  proven recurring gap justifies it.
- **New artifact type** → add a template in `templates/` and reference it from
  the relevant contract and workflow.
- **New product repository** → the Builder can operate on a designated external
  repo; missions still live here as the control plane.

## What is intentionally NOT built yet
- An autonomous multi-agent runtime / orchestrator.
- A UI / dashboard (the scripts + Markdown suffice for the foundation).
- A metrics database or analytics service.
- Any automatic production deployment path.
