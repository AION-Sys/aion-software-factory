# Measurement Baseline — FROZEN before acquisition (MISSION-005, gate 11)

**Frozen: 2026-08-13, before any real data is acquired.** This pins the metric
definitions, the scoring model version, the acceptance thresholds, and the current
synthetic reference numbers, so the pilot is measured against a fixed rule set. Do
not modify after seeing pilot results **unless** the `DECISION-FRAMEWORK.md`
explicitly permits an ITERATE decision (which requires a named, testable cause).

## Frozen model
- Scoring engine: MISSION-003, **config v1.0.0** (unchanged for the pilot).
- Category gate + weighted signals per `docs/decisions/0006-*`.

## Primary economic metric (precise definition)
**COST PER USABLE QUALIFIED OPPORTUNITY**
```
cost_per_usable_qualified_opportunity =
    total_invoiced_spend_usd  /  count(usable_qualified_opportunities)

usable_qualified_opportunity = a record that is ALL of:
  (a) engine status == QUALIFIED, AND
  (b) category_verdict == ELECTRICAL, AND
  (c) has >=1 usable contact channel (phone OR email OR contact_form_url), AND
  (d) confirmed a genuine electrical contractor by the HUMAN label (is_electrical_contractor = yes)
      for records in the labeled sample; outside the sample, (a)-(c) apply and the
      count is reported separately as "machine-usable-qualified" vs
      "human-verified-usable-qualified".
```
`total_invoiced_spend_usd` is the **real Data Axle invoice** (not an estimate).

## Full metric set (definitions)
Machine metrics run over the full acquired set; accuracy metrics use the
human-labeled sample (n=100). **Machine output and human ground truth are reported
separately.**

| Metric | Definition |
|--------|-----------|
| records acquired | count of records returned/paid for |
| valid records | records with a name + location + ≥1 category or NAICS |
| duplicates / duplicate rate | dup count ÷ acquired, deduped by (normalized name+address) and by domain |
| electrical category precision | of records the engine marks ELECTRICAL, fraction genuinely electrical (human) |
| qualification precision | of engine-QUALIFIED sampled records, fraction genuinely electrical contractors (human) |
| qualification recall | of genuine electrical contractors in the sample, fraction the engine QUALIFIED |
| false-positive rate | engine-QUALIFIED but not an electrical contractor ÷ engine-QUALIFIED (sample) |
| false-negative rate | genuine electrical contractors the engine did NOT QUALIFY ÷ genuine (sample) |
| data completeness | mean engine `data_completeness` |
| provenance completeness | fraction with provider + source id/url + retrieval timestamp |
| decision-maker availability | fraction with ≥1 legitimate primary-contact name+title |
| cost per raw record | invoice ÷ records acquired |
| cost per qualified contractor | invoice ÷ count(status==QUALIFIED) |
| cost per usable opportunity | **primary metric above** |
| API reliability | error rate, p50/p95 latency, throttling events (from call logs) |
| processing failures | records that failed normalize/enrich/qualify ÷ acquired |

## Frozen acceptance thresholds (pre-registered)
| Metric | Threshold | Hard gate? |
|--------|-----------|:----------:|
| Qualification precision | ≥ 0.85 | **yes** |
| False-positive rate | ≤ 0.15 | yes (complement) |
| Qualification recall | ≥ 0.70 | no (ITERATE-able) |
| Electrical category precision | ≥ 0.85 | yes |
| Decision-maker availability | ≥ 40% | no |
| Data completeness (avg) | ≥ 0.70 | no |
| Duplicate rate | ≤ 10% | no |
| Provenance completeness | = 100% | **yes** |
| Processing failures | ≤ 2% | no |
| API reliability | error rate < 2%, no blocking throttling | no |
| Cost per qualified contractor | ≤ $0.50 | no (informational) |
| **Cost per usable qualified opportunity** | **≤ $5.00 (CEO owns this bar)** | **yes** |
| Legal storability | must be "yes" | **yes** |

## Synthetic reference snapshot (context only — NOT a pilot result, NOT real-world evidence)
From `python3 evaluate.py` on the labeled synthetic dataset, config v1.0.0, 2026-08-13:
```
records 24 · TP=11 FP=0 FN=2 TN=11
precision 1.0 · recall 0.846 · FP rate 0.0 · FN rate 0.154
category accuracy 1.0 · data completeness 0.833 · provenance 1.0
```
This is the model's behavior on **synthetic** inputs. Real-data metrics will differ;
this snapshot exists only to detect model drift, not to predict pilot outcomes.
