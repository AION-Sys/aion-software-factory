# Engineering Tasks — MISSION-003

- **Author:** AION-ARCHITECT · **Implemented by:** AION-BUILDER · **Consumes:** `architecture.md`

| # | Task | Objective / AC | Status |
|---|------|----------------|--------|
| 1 | Add CategoryVerdict, ScoreContribution, NormalizedBusiness; extend Lead | obj 3 / AC-2,3 | DONE |
| 2 | `scoring/config.py` + `default_config.json` (explicit, configurable) | obj 3 / AC-2 | DONE |
| 3 | `scoring/engine.py`: category validation + weighted, explainable scoring | obj 1,2,3 / AC-1,2 | DONE |
| 4 | `normalize.py` stage (clean/standardize, provider-independent) | obj 4 / AC-3 | DONE |
| 5 | `enrich.py` → completeness + provenance; consumes NormalizedBusiness | obj 4 / AC-3 | DONE |
| 6 | Pipeline rewire + synthetic flag + data-quality summary | obj 4 / AC-3,10 | DONE |
| 7 | Output: category, `why`, `synthetic` column, JSON disclaimer | AC-2,10 | DONE |
| 8 | Expanded labeled synthetic dataset (all categories) | obj 7 / AC-6 | DONE |
| 9 | `metrics.py` + `evaluate.py` (precision/FP/FN/completeness) | obj 9 / AC-8 | DONE |
| 10 | Regression tests: category, qualification, config, metrics, normalize | obj 8 / AC-7 | DONE |
| 11 | Governance docs: requirements, eval framework+template, activation checklist | obj 5,6,10 / AC-4,5,9 | DONE |
| 12 | ADR-0006; update product README; regenerate examples | AC-2,3 | DONE |

## Key done-when conditions
- Task 3: handyman with "minor electrical" → NON_ELECTRICAL → DISQUALIFIED (Q1 fix).
- Task 8: dataset has obvious/commercial/residential/subcontractor electricians,
  solar+electrical, general contractors, handymen, HVAC, plumbers, ambiguous names,
  incomplete websites, and missing-contact cases — each with `ground_truth`.
- Task 9: FP rate ≈ 0 on the labeled set; metrics reproducible and labeled SYNTHETIC.

## Sequencing
1→2→3 (core), 4→5→6 (stages), 7 (output), 8→9→10 (data/measure/test), 11→12 (governance/docs).
