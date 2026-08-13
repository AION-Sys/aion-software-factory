# Measurement Plan — MISSION-005

Defines exactly how every metric is computed and what result is acceptable. The
thresholds below are **pre-registered**: they are set here, *before any data is
acquired*, so the pilot cannot move its own goalposts. The CEO ratifies them (or
edits them) as part of authorization.

> All accuracy metrics distinguish **machine output** (from the existing engine)
> from **ground truth** (from a human-labeled sample). Automated metrics run over
> the full dataset; precision/recall/false-positive run over the labeled sample.

## A. Labeling protocol (ground truth)
- Draw a **random sample of 100** acquired records (or all, if fewer).
- A human labeler applies a fixed rubric per record:
  - `is_electrical_contractor` (yes/no) — is this genuinely an electrical contractor?
  - `is_usable_opportunity` (yes/no) — electrical contractor **and** has a reachable
    decision-maker or a business contact channel usable for future outreach.
  - `notes` — evidence for the call.
- Record the rubric version and labeler. Optionally a second labeler on 25 records to
  report inter-rater agreement. Labels are stored with the dataset (access-controlled).

## B. Metric definitions
| # | Metric | Definition / formula | Source |
|---|--------|----------------------|--------|
| 1 | Electrical-contractor coverage | records returned for NAICS 238210 in the metro; compared to a public benchmark count if available | provider result count; benchmark = ESTIMATED |
| 2 | Data completeness | mean of engine `data_completeness` (fraction of key fields present) | engine (MISSION-003) |
| 3 | Decision-maker availability | % of records with ≥1 legitimate primary-contact name+title | engine `decision_makers` |
| 4 | Duplicate rate | duplicate records ÷ total, deduped by (normalized name + address) and by domain | computed on dataset |
| 5 | False-positive rate | of records the engine marks QUALIFIED, fraction that are NOT electrical contractors per human label | engine ∩ labeled sample |
| 6 | Qualification **precision** | TP ÷ (TP+FP): of engine-QUALIFIED sampled records, fraction genuinely electrical contractors | engine ∩ labels |
| 7 | Qualification **recall** | TP ÷ (TP+FN): of genuine electrical contractors in the sample, fraction the engine QUALIFIED | engine ∩ labels |
| 8 | Provenance quality | % records with source provider + URL/id + retrieval timestamp; note freshness if provided | engine `provenance_complete` |
| 9 | **Cost per raw record** | total invoice ÷ records acquired | invoice (real) |
| 10 | **Cost per qualified contractor** | total invoice ÷ count(status = QUALIFIED) | invoice + engine |
| 11 | **Cost per usable sales opportunity** | total invoice ÷ count(QUALIFIED **and** decision-maker/contact usable) | invoice + engine + label |
| 12 | API reliability | error rate, p50/p95 latency, throttling events observed during the pull | call logs |
| 13 | Rate limits (actual) | observed/enforced limits vs. documented | call logs + quote |
| 14 | Retention/storage requirements (actual) | what the license actually requires | Data Axle quote/terms |
| 15 | Legal storability & usability | may we store and use this data for AION's Provider→Intelligence→verified-dataset workflow? | legal review |

## C. Pre-registered acceptance thresholds (proposals — CEO ratifies)
| Metric | Proposed acceptable threshold | Rationale |
|--------|-------------------------------|-----------|
| Qualification precision (#6) | **≥ 0.85** | Few false positives entering the pipeline |
| False-positive rate (#5) | **≤ 0.15** | Complement of precision bar |
| Qualification recall (#7) | **≥ 0.70** | Don't miss most real contractors |
| Decision-maker availability (#3) | **≥ 40%** | Enough actionable leads to matter |
| Data completeness (#2) | **≥ 0.70** average | Records rich enough to act on |
| Duplicate rate (#4) | **≤ 10%** | Not paying repeatedly for the same business |
| Provenance quality (#8) | **= 100%** | Every stored record must be traceable |
| Cost per qualified contractor (#10) | **≤ $0.50** | Raw unit economics (ESTIMATED basis) |
| Cost per usable sales opportunity (#11) | **≤ $5.00** | The headline economic bar (CEO owns this number) |
| API reliability (#12) | error rate **< 2%**, no blocking throttling | Usable at pilot scale |
| Legal storability (#15) | **must be "yes"** | Hard gate — no acceptable "maybe" |

> The economic thresholds (#10, #11) are placeholders reflecting the Mission 004
> model; the **CEO sets the true bar** based on downstream unit economics. #11 is the
> metric that matters most — treat it as the decision driver.

## D. Reporting
Produce one **AION Intelligence Evaluation** report (in `missions/MISSION-005/` at
execution time) with: the metrics table vs. thresholds (PASS/FAIL each), the
confusion matrix, the economic figures with the real invoice, API reliability
observations, the legal determination, and a one-line recommendation feeding
`DECISION-FRAMEWORK.md`. Clearly separate **measured** figures from any remaining
**estimates**.
