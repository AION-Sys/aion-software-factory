# PRD — MISSION-003 — Live Data Readiness + Intelligence Calibration

- **Author:** AION-PM
- **Status:** APPROVED
- **Source mission:** `mission.md`

## 1. Summary
Make the intelligence layer production-ready — governance, architecture, testing,
measurement — before any live data provider is connected. Fix the MISSION-002 Q1
false-positive, make scoring explicit/configurable/explainable, and establish
baseline accuracy metrics on labeled synthetic data.

## 2. Problem & Opportunity
The MISSION-002 scorer was coarse: a handyman advertising "minor electrical"
qualified (Q1). We cannot connect real, paid data to a scorer we can't trust or
measure. Getting governance and measurement right first de-risks every future
dollar spent on data.

## 3. Users
| User | Need |
|------|------|
| CEO | A clear, evidence-backed decision on whether/how to go live |
| Operator | Explainable, trustworthy qualification |
| Future agent | A clean provider seam + evaluation method to extend safely |

## 4. Goals & Success Metrics (SYNTHETIC — not real-world evidence)
| Goal | Metric | Target |
|------|--------|--------|
| Kill false positives | FP rate on labeled set | ≈0 |
| Precise qualification | precision | high (≥0.9) |
| Explainability | every lead has per-signal reasons | 100% |
| Measurability | baseline metrics reproducible | `evaluate.py` |

## 5. Scope / 6. Non-Goals
See `mission.md`. Notably **out**: choosing/connecting a provider, purchases,
credentials, real PII, deployment, outreach.

## 7. Requirements → Objectives mapping
- Fix Q1 → category validation + negative signals (obj 1,2).
- Explicit/configurable/explainable scoring (obj 3).
- Clean provider/normalizer/enrichment/qualification/output separation (obj 4).
- Live-provider requirements (obj 5).
- Provider evaluation framework + template (obj 6).
- Expanded labeled synthetic dataset (obj 7).
- Regression tests (obj 8).
- Baseline metrics: precision, FP, FN, data + provenance completeness (obj 9).
- CEO approval requirements + activation checklist (obj 10).

## 8. Acceptance Criteria
Mirrors `mission.md` § Acceptance Criteria (AC-1…AC-10).

## 9. Assumptions
- Synthetic data is sufficient to validate *logic and governance*, not real
  accuracy. All synthetic outputs are labeled and never treated as evidence.
- Scoring thresholds will be recalibrated against a labeled real sample after the
  CEO gate.

## 10. Open Questions (for the CEO gate)
- Which provider + budget? Which first market + volume? Retention/deletion policy
  for real PII? → answered at activation (see checklist).

## Handoff
- Next agent: **AION-ARCHITECT** (done) → **AION-BUILDER** (done) → QA → Security → CEO gate.
