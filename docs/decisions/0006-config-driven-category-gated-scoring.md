# ADR-0006 — Config-driven, category-gated, explainable scoring

- **Status:** Accepted
- **Date:** 2026-08-13
- **Deciders:** AION-ARCHITECT (MISSION-003)
- **Mission:** MISSION-003

## Context
MISSION-002 QA found Q1: a general handyman advertising "minor electrical" scored
full service-relevance and QUALIFIED. The root cause was a coarse substring
keyword match and no notion of *disqualifying* categories. Before connecting a
live provider we need scoring that is explicit, configurable, explainable, and
resistant to false positives.

## Decision
Replace the single-function scorer with a two-part, config-driven engine
(`leadintel/scoring/`):

1. **Category validation (gate).** Classify each business as `ELECTRICAL`,
   `ADJACENT`, `NON_ELECTRICAL`, or `AMBIGUOUS` from its categories + name using
   keyword sets in config. The verdict **caps the achievable status**:
   `NON_ELECTRICAL` can never be `QUALIFIED`; `ADJACENT`/`AMBIGUOUS` cap at
   `NEEDS_REVIEW`; only `ELECTRICAL` can be `QUALIFIED`.
2. **Weighted, explainable scoring.** Positive signals add, negative signals
   subtract. Every non-zero signal produces a `ScoreContribution`
   (signal, points, kind, human reason), so each lead explains *why* it scored
   as it did.

Rules live in `scoring/default_config.json` (weights, thresholds, keyword lists)
— configurable and auditable without code changes. The engine is
**provider-independent**: it consumes an enriched `Lead` + `ScoringConfig`, never
provider-specific shapes.

## Consequences
### Positive
- Non-electrical trades (handyman/plumber/HVAC/GC-without-electrical) are gated
  out — Q1 fixed and regression-tested.
- Scores are explainable and tunable; thresholds calibratable per config.
- Enables baseline metrics (precision/FP/FN) against a labeled dataset.
### Negative / trade-offs
- Category gating is keyword-based; genuinely mislabeled sources could be
  misclassified. Mitigated by the `AMBIGUOUS` verdict + human review, and to be
  recalibrated against real data.

## Alternatives considered
- **Tune weights only** — rejected: doesn't address the missing category gate;
  would be "tuning to make the sample look good," which the mission forbids.
- **ML classifier** — rejected for V1: needs real labeled data we don't yet have;
  not explainable enough for a governance baseline.
