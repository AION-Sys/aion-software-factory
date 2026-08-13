# QA Report — MISSION-003

- **Reviewer:** AION-QA (independent of Builder)
- **Consumes:** `products/lead-intel/` + `prd.md` acceptance criteria + labeled dataset
- **Verdict:** PASS
- **Date:** 2026-08-13

## 1. Acceptance criteria results
| AC # | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| AC-1 | Non-electrical trades cannot QUALIFY | PASS | `test_qualify` (handyman/plumber/HVAC/GC); `test_category.test_no_non_electrical_is_ever_qualified`; original Q1 case (Zilker Handyman) now NON_ELECTRICAL/DISQUALIFIED in `examples/austin-tx-sample.csv` |
| AC-2 | Scoring explicit + configurable + explainable | PASS | `scoring/default_config.json`; `test_scoring_config` (thresholds change outcome, invalid rejected); `why`/`score_contributions` per lead |
| AC-3 | Clean stage separation; engine provider-independent | PASS | `normalize.py`/`enrich.py`/`scoring/engine.py`; `test_pipeline.test_engine_is_provider_independent`, `test_normalize` |
| AC-4 | Live-provider requirements documented | PASS | `docs/operations/live-provider-requirements.md` |
| AC-5 | Provider evaluation framework + template | PASS | `docs/operations/provider-evaluation-framework.md`, `templates/provider-evaluation-template.md` |
| AC-6 | Labeled dataset covers all categories | PASS | `data/fixtures/synthetic_leads.json` (24 records, all listed categories, `ground_truth`) |
| AC-7 | Regression tests per category + qualification | PASS | `test_category` (data-driven per record), full suite |
| AC-8 | Baseline metrics established | PASS | `evaluate.py` / `metrics.py`; `baseline-metrics.json` |
| AC-9 | CEO approval requirements + activation checklist | PASS | `docs/operations/live-provider-activation-checklist.md` |
| AC-10 | Synthetic labeled end-to-end, never treated as real | PASS | `is_synthetic` flag; CSV `synthetic` column; JSON/summary/metrics `_disclaimer`; `test_category.test_all_synthetic_flagged` |

## 2. Test execution
```
python3 -m unittest discover -s tests
Ran 50 tests in 0.045s
OK
```
- **50 passed, 0 failed** (was 21 in MISSION-002). New: category regression,
  scoring-config, metrics, normalize, plus updated qualify/enrich/pipeline/output.

## 3. Baseline metrics (SYNTHETIC — not real-world evidence)
```
records: 24    confusion: TP=11 FP=0 FN=2 TN=11
precision 1.0 · recall 0.846 · FP rate 0.0 · FN rate 0.154
category accuracy 1.0 · expected-behavior accuracy 1.0
avg data completeness 0.833 · provenance completeness 1.0
```

## 4. Findings
| ID | Severity | Description | Disposition |
|----|----------|-------------|-------------|
| Q3 | INFO | 2 false negatives are electrical contractors with missing website / missing contact → land in NEEDS_REVIEW, not lost. | Accepted: correct behavior (route to human review); documented in dataset (`expected_qualified=false`). |
| Q4 | INFO | Metrics are on synthetic data; precision 1.0 will not hold on real data. | Recalibrate against a labeled real sample at the CEO gate (activation checklist §D). |
| Q5 | LOW | Category classification is keyword-based; unusual phrasings could misclassify. | Mitigated by AMBIGUOUS→review + regression dataset; revisit on real data. |

## 5. Verification of the MISSION-002 Q1 fix
Re-ran the original Austin dataset: **Zilker Handyman & Home** → `NON_ELECTRICAL`
/ `DISQUALIFIED` (was `QUALIFIED 74`). Confirmed. Q1 closed.

## 6. Verdict & handoff
- **Verdict:** PASS — all 10 acceptance criteria met; findings are INFO/LOW and
  point to real-data recalibration, which is correctly deferred to the CEO gate.
- **Handoff:** AION-SECURITY.
