# Observability

We define **what** the factory must eventually measure and **where the data comes
from** — without building an analytics system yet. Per ADR-0002 there is no
metrics database; early metrics are derived from version-controlled artifacts.

## Metrics catalogue

| Metric | Definition | Source (today) |
|--------|-----------|----------------|
| Mission completion rate | missions reaching `deployed` ÷ missions started | mission `stage` values |
| Agent success rate | stages passing on first handoff ÷ total stage runs | handoff blocks in `Log` |
| Agent failure rate | stages sent backward ÷ total stage runs | backward transitions in `Log` |
| QA pass rate | QA reports PASS ÷ total QA reports | `qa-report.md` verdicts |
| Security pass rate | security PASS ÷ total security reports | `security-report.md` verdicts |
| Human intervention rate | YELLOW/RED approvals ÷ missions | `Log` approval entries |
| Time saved / hours augmented | est. manual hours − actual elapsed | mission `Log` timestamps (est.) |
| Cost per mission | tokens/compute + paid services per mission | runtime logs (when available) |
| Tokens / compute | agent runtime usage per stage | agent runtime (when instrumented) |
| Post-deployment bugs | defects filed after `deployed` | linked issues (future) |
| Deployment success rate | successful deploys ÷ deploy attempts | deployment records (future) |

## Data model (files first)
Everything above is derivable from:
- **mission metadata** (`status`, `stage`) — pipeline position and completion;
- **handoff blocks** in each mission `Log` — per-stage outcomes and timing;
- **report verdicts** (`qa-report.md`, `security-report.md`) — quality gates;
- **git history** — who/what/when for changes.

## Instrumentation the Architect must add per feature
Each product feature's `architecture.md` § Observability must state what events,
logs, or counters it emits so these metrics remain measurable as the factory
grows.

## Deliberately deferred
No metrics store, dashboard, or analytics pipeline is built in the foundation.
When measurement needs exceed what scripts over files can provide, introduce a
store via an ADR — not before. `scripts/mission_status.py` is the first, minimal
observability surface.
