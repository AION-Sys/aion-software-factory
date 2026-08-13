# MISSION-003 — CEO Mission Report

**Final status: `READY FOR LIVE PROVIDER DECISION`** — NOT live-provider approved.

Mission 003 made the lead-intelligence layer production-ready for governance,
architecture, testing, and measurement — with **no** APIs purchased, **no**
credentials, **no** real data, and **no** deployment, exactly as directed.

---

## 1. The question this mission had to answer
> "If we connect a real data provider tomorrow, exactly what data enters our
> system, how is it transformed, how is a lead qualified, what evidence supports
> the qualification, what does it cost, what legal/privacy risks exist, and how do
> we know whether the system is accurate?"

Answers below, each backed by an artifact.

| Question | Answer | Where |
|----------|--------|-------|
| What data enters? | A provider returns `RawBusiness` records (name, website, location, categories, contacts, size signals, optional decision-makers, provenance). | `providers/base.py`, `live-provider-requirements.md` |
| How is it transformed? | Provider → **Normalizer** (clean/standardize) → **Enrichment** (completeness + provenance) → **Qualification Engine** → **Output**. | `architecture.md` |
| How is a lead qualified? | Category gate (ELECTRICAL/ADJACENT/NON_ELECTRICAL/AMBIGUOUS) + weighted signals; only ELECTRICAL can QUALIFY. | `scoring/engine.py`, ADR-0006 |
| What evidence supports it? | Every lead carries a per-signal `why` (points + reason) and a `category_reason`. | CSV `why`, JSON `score_contributions` |
| What does it cost? | Cost-per-qualified-lead is estimated from the provider's price × our qualification rate. | evaluation framework + template |
| What legal/privacy risks? | ToS/licensing/PII/retention/deletion requirements enumerated and gated. | `live-provider-requirements.md`, activation checklist |
| How do we know it's accurate? | Baseline metrics on a labeled dataset: precision, recall, FP/FN rates, completeness. | `metrics.py`, `baseline-metrics.json` |

## 2. What changed since MISSION-002
- **Q1 fixed.** The handyman-with-"minor electrical" case now classifies as
  `NON_ELECTRICAL` → `DISQUALIFIED` (was `QUALIFIED 74`). Regression-tested.
- **Scoring is now explicit, configurable, explainable** (JSON config; per-signal
  reasons; category gate + negative signals). ADR-0006.
- **Clean stage separation**; the qualification engine is provider-independent.
- **Labeled synthetic dataset** (24 records) across every category listed.
- **Regression + metrics harness**; test suite grew 21 → **50 tests**.
- **Governance package**: provider requirements, evaluation framework + template,
  security/privacy checklist, and the CEO activation checklist.

## 3. Baseline metrics — SYNTHETIC DATA (NOT real-world evidence)
```
records 24   confusion: TP=11  FP=0  FN=2  TN=11
qualification precision   1.0
recall                    0.846
false-positive rate       0.0
false-negative rate       0.154
category accuracy         1.0
data completeness (avg)   0.833
provenance completeness   1.0
```
Reproduce: `cd products/lead-intel && python3 evaluate.py`.

**Read this honestly:** precision 1.0 / FP 0.0 reflect the *category gate working
on synthetic data* — it does **not** predict real-world precision. The 2 false
negatives are real electrical contractors with missing website/contact that
correctly route to `NEEDS_REVIEW` rather than being dropped. Real numbers require
recalibration against a labeled real sample (activation checklist §D).

## 4. Deliverables (CEO gate checklist)
1. Mission report — this file.
2. Updated scoring model — `scoring/` + `default_config.json` (ADR-0006).
3. Provider interface — `providers/base.py` (+ disabled `live.py`).
4. Provider evaluation framework — `docs/operations/provider-evaluation-framework.md` + `templates/provider-evaluation-template.md`.
5. Expanded synthetic dataset — `data/fixtures/synthetic_leads.json`.
6. Regression test results — 50/50 passing.
7. Baseline metrics — `baseline-metrics.json`.
8. Security/privacy checklist — activation checklist §C + `security-report.md`.
9. Live-provider activation checklist — `docs/operations/live-provider-activation-checklist.md`.
10. Exact CEO decision required — below.

## 5. Exact decision required from the CEO
No action is required to keep operating on synthetic data. To go live, the CEO
must approve **in writing** (recorded in this mission's `Log`) all of:
1. **Provider** — chosen from a completed evaluation comparison.
2. **Budget** — a spending cap (paid service = YELLOW; the purchase is a human RED action).
3. **First market + volume** for a bounded pilot.
4. **PII handling** — retention window + deletion process.
5. **Authorization to store real prospect data** in a defined, access-controlled, non-repo location.

Until all five are given, status remains **READY FOR LIVE PROVIDER DECISION**.

## 6. Recommendation
Approve a **provider-evaluation sub-mission** (still GREEN: desk research only, no
signups/credentials) to complete the evaluation template for 2–3 candidates and
return a comparison + recommendation. That produces the evidence for decision #1
above without spending anything or touching real data.
