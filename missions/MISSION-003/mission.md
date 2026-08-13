<!-- AION-MISSION-METADATA
id: MISSION-003
title: Live Data Readiness + Intelligence Calibration
status: ACTIVE
stage: approval
owner: CEO
priority: P1
-->

# MISSION-003 — Live Data Readiness + Intelligence Calibration

> **Final status: READY FOR LIVE PROVIDER DECISION** (NOT live-provider approved).
> Machine-readable status is in the metadata block above.

## Business Objective
Make the lead-intelligence layer production-ready from a governance, architecture,
testing, and measurement perspective — **before** connecting any live data
provider. No APIs purchased, no credentials, no real data, no deployment.

## CEO Decision (input)
- MISSION-002 approved as a successful factory test.
- Intelligence layer approved for continued development.
- Live-data YELLOW gate **not** approved. No purchases / credentials / real PII / deploy.

## Problem
MISSION-002 shipped a working but coarse scorer: QA finding Q1 showed a handyman
advertising "minor electrical" incorrectly QUALIFIED. Before real data enters the
system we must fix relevance, make scoring explicit/configurable/explainable,
separate the pipeline stages cleanly, and be able to *measure* accuracy.

## Target User
- CEO (approval decision) and AION operators (trustworthy, explainable scores).
- Future AION agents extending the system with a live provider.

## Expected Outcome
AION can answer: *"If we connect a real data provider tomorrow, exactly what data
enters, how is it transformed, how is a lead qualified, what evidence supports it,
what does it cost, what legal/privacy risks exist, and how do we know it's
accurate?"*

## Success Metrics (on SYNTHETIC data — not real-world evidence)
- Q1 fixed: non-electrical trades never QUALIFY (regression-tested).
- Qualification precision high; false-positive rate low, on the labeled dataset.
- Every lead's score is explainable (per-signal reasons).
- Baseline metrics established and reproducible via `evaluate.py`.

## Scope
- Fix Q1; add category validation + negative signals.
- Explicit, configurable, explainable scoring model (JSON config).
- Clean stage separation: Provider → Normalizer → Enrichment → Qualification → Output.
- Provider interface + live-provider requirements + evaluation framework/template.
- Expanded, labeled synthetic dataset across all listed categories.
- Regression tests per category + qualification; baseline metrics harness.
- Governance: security/privacy checklist + live-provider activation checklist + CEO decision.

## Non-Goals
- Selecting or connecting a live provider (YELLOW — not approved).
- Purchasing APIs / adding credentials / collecting real PII / deploying.
- Automated outreach.

## Acceptance Criteria
- [x] AC-1 Non-electrical businesses (handyman/plumber/HVAC/GC-without-electrical) cannot QUALIFY.
- [x] AC-2 Scoring rules are explicit + configurable (JSON) + explainable (per-signal reasons).
- [x] AC-3 Pipeline stages are cleanly separated; qualification engine is provider-independent.
- [x] AC-4 Live-provider requirements documented (obj 5).
- [x] AC-5 Provider evaluation framework + template exist (obj 6).
- [x] AC-6 Labeled synthetic dataset covers all listed categories (obj 7).
- [x] AC-7 Regression tests per category + qualification pass (obj 8).
- [x] AC-8 Baseline metrics established: precision, FP rate, FN rate, data + provenance completeness (obj 9).
- [x] AC-9 CEO approval requirements + activation checklist documented (obj 10).
- [x] AC-10 Synthetic data is labeled end-to-end and never treated as real-world evidence.

## Technical Requirements
Python 3, stdlib only. Config-driven scoring (ADR-0006). See `architecture.md`.

## Security Requirements
No secrets, no credentials, no real data. Synthetic labeling end-to-end. Live
acquisition remains a disabled, human-gated seam.

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Synthetic metrics mistaken for real accuracy | Med | High | Disclaimers everywhere; metrics labeled SYNTHETIC; recalibrate on real data |
| Category gate too strict (false negatives) | Med | Med | AMBIGUOUS→review, not discard; 2 known FN documented; tunable config |
| Keyword classification misses edge cases | Med | Med | Regression dataset + tests; recalibrate against live sample |

## Dependencies
- MISSION-002 intelligence layer (`products/lead-intel/`).
- Future live provider requires CEO gate (see activation checklist).

## Milestones
1. Scoring engine + config (Architect/Builder). 2. Dataset + regression tests + metrics (Builder/QA).
3. Governance docs (PM/Security). 4. CEO gate: READY FOR LIVE PROVIDER DECISION.

## Approval Gates
- **YELLOW:** connecting any live/paid provider; storing real prospect data.
- **RED:** purchasing services; outreach to real people.

## Definition of Done
All acceptance criteria met; regression + metrics passing on synthetic data; QA
and Security reports recorded; final status **READY FOR LIVE PROVIDER DECISION**.

## Artifact Package
| Artifact | Path |
|----------|------|
| PRD | `prd.md` |
| Architecture | `architecture.md` |
| Tasks | `tasks.md` |
| QA Report | `qa-report.md` |
| Security Report | `security-report.md` |
| CEO Mission Report | `report.md` |
| Baseline Metrics (data) | `baseline-metrics.json` |
| Implementation | `../../products/lead-intel/` |
| Provider eval framework | `../../docs/operations/provider-evaluation-framework.md` |
| Provider eval template | `../../templates/provider-evaluation-template.md` |
| Live-provider requirements | `../../docs/operations/live-provider-requirements.md` |
| Activation checklist (CEO gate) | `../../docs/operations/live-provider-activation-checklist.md` |

## Log
- 2026-08-13 — Mission created from CEO decision on MISSION-002.
- 2026-08-13 — Scoring engine refactored (ADR-0006); dataset + tests + metrics added; governance docs written.
- 2026-08-13 — QA and Security reviews complete. Status: READY FOR LIVE PROVIDER DECISION. Awaiting CEO.
