<!-- AION-MISSION-METADATA
id: MISSION-002
title: Electrical Contractor Lead Intelligence (V1)
status: ACTIVE
stage: approval
owner: CEO
priority: P1
-->

# MISSION-002 — Electrical Contractor Lead Intelligence (V1)

> First real end-to-end factory test. Machine-readable status is in the metadata
> block above. Artifact package is listed at the bottom.

## Business Objective
Build the smallest usable system that identifies electrical contractor prospects
and organizes decision-maker intelligence into a structured lead pipeline. Prove
the **intelligence layer** before any outreach automation.

## Problem
Finding and qualifying electrical-contractor prospects is manual, slow, and
inconsistent. There is no repeatable way to turn a target market into a
structured, scored lead list an operator can act on.

## Target User
An AION operator (sales/BD) who provides a target market + location and needs a
usable, qualified lead list without doing the research by hand.

## Expected Outcome
Given a market + location, the system produces a structured lead list where each
lead carries: company, website, location, service type, estimated opportunity,
decision-maker info (only when legitimately available), contact channels,
qualification score, research notes, source, and status.

## Success Metrics
- From one `(market, location)` input, the system produces a lead list with **all
  required fields populated or explicitly marked "not available."**
- Qualification scores are **deterministic and explainable** (score breakdown per lead).
- Output is usable immediately: valid **CSV + JSON** an operator can open.
- End-to-end run requires **zero credentials and zero network** in V1 (fixture provider).

## Scope (V1)
- Pipeline: INPUT → RESEARCH → ENRICH → QUALIFY → ORGANIZE → OUTPUT.
- Deterministic **fixture research provider** (sample electrical contractors).
- Enrichment (normalize business data), qualification scoring, structured storage.
- CSV + JSON output; CLI entry point.
- A documented **live-provider seam** for real data acquisition (not enabled).

## Non-Goals
- No automated cold outreach / email / calling (explicitly deferred).
- No live paid data-provider integration enabled in V1 (YELLOW gate).
- No web UI / dashboard.
- No CRM sync, no database.
- No scraping of personal data beyond legitimately-available business contact info.

## Requirements
- R1. Accept a target market/service type and a location as input.
- R2. Produce leads from a pluggable research provider.
- R3. Enrich each lead into the canonical schema (below).
- R4. Score each lead 0–100 with an explainable breakdown and assign a status.
- R5. Estimate opportunity tier (LOW/MEDIUM/HIGH) from available size signals.
- R6. Capture decision-maker info **only when legitimately available**; otherwise mark unavailable.
- R7. Persist leads as JSONL and export CSV.
- R8. Run end-to-end via CLI with no credentials/network in V1.

## Acceptance Criteria
- [x] AC-1 Running the CLI with `(market, location)` produces a lead list file (CSV + JSON).
- [x] AC-2 Every lead includes all required fields; missing data is explicitly `null`/"not available", never fabricated.
- [x] AC-3 Qualification score is 0–100 and accompanied by a per-signal breakdown.
- [x] AC-4 Each lead has a status in {NEW, QUALIFIED, NEEDS_REVIEW, DISQUALIFIED}.
- [x] AC-5 Estimated opportunity is one of {LOW, MEDIUM, HIGH}.
- [x] AC-6 Decision-maker info appears only when present in source; absence is marked, not invented.
- [x] AC-7 The system runs with zero credentials and zero network access.
- [x] AC-8 Automated tests cover qualification, pipeline, and output; all pass.

## Technical Requirements
- Python 3, standard library only (no external dependencies).
- Pluggable `ResearchProvider` interface; `FixtureProvider` for V1.
- Pure, testable enrichment + qualification functions.
- File-based storage (JSONL + CSV); no database.
- See `architecture.md` for detail.

## Security Requirements
- No secrets committed; live provider reads API keys from env only.
- Capture only legitimately-available **business** information; do not fabricate
  decision-maker PII. Absence must be represented explicitly.
- Respect provider Terms of Service and robots directives for any future live provider.
- Live data acquisition and any paid provider is a **YELLOW gate** requiring human approval.
- Outreach is a separate, later mission and is out of scope.

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Fabricated / stale prospect data misleads operators | Med | High | Fixture data clearly labeled synthetic; live provider gated; no invented PII |
| Compliance exposure from scraping personal data | Med | High | V1 has no scraping; schema marks PII optional; security review required before live |
| Over-fitting scoring to sample data | Med | Med | Transparent weighted heuristic, documented + unit-tested; tunable |
| Scope creep into outreach/CRM | Med | Med | Non-goals explicit; outreach deferred to a future mission |

## Dependencies
- Foundation (MISSION-001) agent contracts, templates, and workflow.
- Future live provider requires CEO-approved API credentials (YELLOW).

## Milestones
1. Mission + PRD approved (PM).
2. Architecture + tasks (Architect).
3. Intelligence layer implemented + tested (Builder).
4. QA verification against acceptance criteria.
5. Security review (PII/compliance/secrets).
6. Human approval gate → (future) live provider mission.

## Approval Gates
- **YELLOW (needs human approval):** enabling any live/paid data provider;
  performing real data acquisition; storing real prospect PII.
- **RED (human-only):** any outreach to real people; purchasing data/services;
  exporting prospect PII to external systems.

## Definition of Done
See `AION_ENGINEERING.md` § Definition of Done. This mission additionally requires:
- The intelligence layer runs end-to-end on fixture data with all fields populated.
- QA and Security reports recorded; no HIGH/CRITICAL security findings open.
- No outreach and no live paid provider enabled.

## Artifact Package
| Artifact | Path | Produced by |
|----------|------|-------------|
| PRD | `prd.md` | AION-PM |
| Architecture | `architecture.md` | AION-ARCHITECT |
| Tasks | `tasks.md` | AION-ARCHITECT |
| QA Report | `qa-report.md` | AION-QA |
| Security Report | `security-report.md` | AION-SECURITY |
| Implementation | `../../products/lead-intel/` | AION-BUILDER |

## Log
- 2026-08-13 — Mission created from CEO objective (factory test).
- 2026-08-13 — PRD, architecture, and tasks produced; intelligence layer built and tested.
- 2026-08-13 — QA and Security reviews completed. Awaiting human approval gate.
