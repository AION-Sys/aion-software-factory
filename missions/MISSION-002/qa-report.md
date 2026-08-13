# QA Report — MISSION-002 — Electrical Contractor Lead Intelligence (V1)

- **Reviewer:** AION-QA (independent of Builder)
- **Consumes:** `products/lead-intel/` branch + `prd.md` acceptance criteria
- **Verdict:** PASS (with non-blocking findings)
- **Date:** 2026-08-13

## 1. Acceptance criteria results
| AC # | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| AC-1 | CLI produces CSV + JSON lead list | PASS | `python3 cli.py --market "electrical contractors" --location "Austin, TX"` wrote `examples/austin-tx-sample.{csv,json,jsonl,run-summary.json}` |
| AC-2 | All required fields present; missing = explicit, never fabricated | PASS | `test_all_required_fields_present`; JSON shows `website: null`, `decision_makers: []` for Hill Country sample |
| AC-3 | Score 0–100 with per-signal breakdown | PASS | `test_breakdown_sums_to_score`, `test_score_is_bounded_0_100`; CSV `score_breakdown` column |
| AC-4 | Status ∈ {NEW,QUALIFIED,NEEDS_REVIEW,DISQUALIFIED} | PASS | `test_all_required_fields_present`; run shows QUALIFIED/NEEDS_REVIEW |
| AC-5 | Opportunity ∈ {LOW,MEDIUM,HIGH} (UNKNOWN when no signals) | PASS | `test_no_size_signals_gives_unknown_opportunity`; run shows HIGH/MEDIUM/LOW |
| AC-6 | Decision-maker only when legitimately available; absence marked | PASS | `test_decision_makers_only_when_present`, `test_decision_maker_without_name_is_dropped`, `test_missing_fields_are_none_not_fabricated` |
| AC-7 | Runs with zero credentials and zero network | PASS | Fixture run needs no env/keys; `test_live_provider_is_gated` confirms live path is disabled |
| AC-8 | Automated tests cover qualify/pipeline/output; all pass | PASS | 21 tests, all green |

## 2. Test execution
```
python3 -m unittest discover -s tests
Ran 21 tests in 0.010s
OK
```
- Suite result: **21 passed, 0 failed**.
- Coverage: qualify (7), enrich (4), pipeline (6), output (4).

## 3. Findings
| ID | Severity | Type | Description | Repro |
|----|----------|------|-------------|-------|
| Q1 | LOW | edge | Coarse relevance keyword: "Zilker Handyman & Home" (category "minor electrical") scores full service-relevance (25) and lands QUALIFIED (74). A handyman doing minor electrical is a weak prospect. | Run Austin, TX query; inspect row |
| Q2 | INFO | calibration | Thresholds/weights are tuned on synthetic data; average score (82.4) is optimistic for a curated sample. Recalibrate after first live run. | PRD §11 open question |

### Recommended follow-ups (not blocking V1)
- Q1: add negative keywords ("handyman", "home repair") or require an explicit
  electrical-contractor category to earn full relevance. Tunable in `qualify.py`.
- Q2: revisit `QUALIFY_THRESHOLD`/weights against real acquired data.

## 4. Edge cases probed
- No website / no phone / no email → fields null, notes explain, still scored. PASS.
- No size signals → opportunity UNKNOWN, 0 opportunity points. PASS.
- Out-of-market business (San Jose, CA) → filtered from an Austin, TX query. PASS.
- `--limit` → respected. PASS.
- Live provider without approval → refuses with clear message. PASS.

## 5. Regressions checked
- Deterministic scoring (`test_deterministic`) → identical output across runs. PASS.
- CSV renders missing values as empty, never the string "None". PASS.

## 6. Verdict & handoff
- **Verdict:** PASS — all acceptance criteria met; Q1/Q2 are non-blocking quality
  follow-ups, appropriate for calibration once a live provider is approved.
- **Handoff:** AION-SECURITY.
