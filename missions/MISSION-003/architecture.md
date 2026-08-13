# Architecture — MISSION-003 — Live Data Readiness + Intelligence Calibration

- **Author:** AION-ARCHITECT
- **Status:** APPROVED
- **Consumes:** `prd.md`

## 1. Overview
Preserve the MISSION-002 architecture; sharpen the stage boundaries and replace
the scorer with a config-driven, category-gated, explainable engine (ADR-0006).
The qualification engine is independent of any data provider.

## 2. Target abstraction (as requested)
```
Data Provider  →  Raw Data       providers/*.py -> RawBusiness
      ↓
Normalizer     →  Normalized     normalize.py   -> NormalizedBusiness  (clean, standardize)
      ↓
Enrichment     →  Lead Record    enrich.py      -> Lead  (+completeness, +provenance, notes)
      ↓
Qualification  →  scored Lead    scoring/engine.py (config-driven, provider-independent)
      ↓
Output         →  files          output.py      -> CSV / JSON / JSONL / run-summary
```
No provider-specific shape passes the Normalizer. The engine consumes only
`Lead` + `ScoringConfig`.

## 3. Scoring model (ADR-0006)
Two parts:
1. **Category validation (gate).** `classify_category()` → ELECTRICAL / ADJACENT /
   NON_ELECTRICAL / AMBIGUOUS from categories + name via config keyword sets. The
   verdict caps status: NON_ELECTRICAL can never QUALIFY; ADJACENT/AMBIGUOUS cap
   at NEEDS_REVIEW; only ELECTRICAL can QUALIFY.
2. **Weighted, explainable scoring.** Positive signals add, negative subtract;
   each non-zero signal emits a `ScoreContribution(signal, points, kind, reason)`.

### Signals (defaults; see `scoring/default_config.json`)
Positive: core_electrical_category (30), commercial_electrical (10),
established_website (10), service_area_match (10/6), contactable (10),
business_maturity (0–15), decision_maker_identified (10), relevant_indicators (5).
Negative: non_electrical_trade (−40), adjacent_only (−10),
insufficient_evidence (−15), ambiguous_no_evidence (−20).
Thresholds: QUALIFIED ≥ 60, NEEDS_REVIEW ≥ 40.

Rules are **data, not code** — configurable/auditable via JSON; the engine only
reads config. `ScoringConfig.validate()` rejects incoherent configs.

## 4. Data model additions
`Lead` gains: `category_verdict`, `category_reason`, `score_contributions`,
`data_completeness`, `provenance_complete`, `scoring_config_version`, and an
`is_synthetic` view (from `Source.is_synthetic`). New intermediate:
`NormalizedBusiness`.

## 5. Measurement
`metrics.py` runs the engine over the **labeled** dataset (`ground_truth`) and
computes precision / recall / FP rate / FN rate / category accuracy /
data completeness / provenance completeness. `evaluate.py` prints/writes it. All
outputs carry a SYNTHETIC disclaimer.

## 6. Synthetic labeling (non-negotiable)
`is_synthetic` flows Provider → Source → Lead → Output (CSV `synthetic` column,
JSON `_disclaimer`, run-summary `_disclaimer`, metrics `_disclaimer`). Real data
(future) will carry `is_synthetic=false`.

## 7. Provider seam & governance
`ResearchProvider` unchanged; `LiveProvider` remains disabled (env-key only).
Governance docs define requirements, evaluation, and the CEO activation gate.

## 8. Decisions
- ADR-0006 (this mission). Builds on ADR-0004 (Python/stdlib), ADR-0005 (fixture-first/gated).

## 9. Trade-offs
- Keyword category gating (not ML) — explainable and needs no real labeled data;
  recalibrate later. AMBIGUOUS routes uncertainty to human review rather than
  discarding it.

## Handoff
- Task list: `tasks.md`. Next: AION-BUILDER (done) → QA → Security → CEO gate.
- Approval gates triggered: none (all GREEN). Live acquisition remains future YELLOW.
