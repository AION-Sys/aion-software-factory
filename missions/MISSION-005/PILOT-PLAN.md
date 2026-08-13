# Bounded Pilot Plan — MISSION-005

A small, bounded, one-shot test. Acquire → run through the existing engine →
measure → decide. Nothing here executes until the CEO authorizes the parameters
(`APPROVALS.md`) and legal signs off (`DATA-HANDLING-PLAN.md`).

## 1. Bounded parameters (proposed — CEO ratifies exact values)
| Parameter | Proposed value | Notes |
|-----------|----------------|-------|
| Provider | **Data Axle** (Business Data / Search API) | Selected in Mission 004 |
| Vertical filter | **NAICS 238210** (electrical contractors) | Pre-filter at the provider |
| Metro (one) | **Denver–Aurora–Lakewood, CO (MSA)** | Aligns with MISSION-003 calibration; CEO may substitute one metro |
| Record volume cap | **2,000 records** (or all available if fewer) | Fixed; not to be exceeded |
| **Hard spend cap** | **$250 USD, absolute not-to-exceed** | Includes any re-pulls; stop at cap regardless of records obtained |
| Human-label sample | **100 records random** (or all if fewer) | Ground truth for precision/recall/false-positive |
| Retention | **≤90 days**, then delete (or shorter per license) | See data-handling plan |
| Engine | **MISSION-003 engine, config v1.0.0, unchanged** | We test the provider against our *current* model |

Estimated cost at cap: 2,000 × ~$0.05–0.075/record ≈ **$100–$150** (ESTIMATED,
Mission 004; confirm with a written quote before purchase). The **$250 hard cap**
sits above that with margin and is the true limit.

## 2. Method (five steps, in order)
1. **Authorize & verify** — CEO ratifies parameters; legal clears the HIGH items;
   obtain a written Data Axle quote + rate-limit/retention terms (still no data pull).
2. **Build the adapter** — implement a thin `DataAxleProvider(ResearchProvider)`
   returning `RawBusiness` records. Credentials via secret manager/env only. Pass an
   AION-SECURITY review before it runs. **No other code changes.**
3. **Acquire (bounded)** — pull ≤2,000 NAICS 238210 records for the one metro, under
   the hard spend cap. Log every API call (count, latency, errors) for reliability metrics.
4. **Run the existing engine** — normalize → enrich → qualify (config v1.0.0). Produce
   the verified lead dataset + run summary. No new scoring logic.
5. **Measure & report** — compute all metrics in `MEASUREMENT-PLAN.md`, including the
   human-labeled sample, and produce the AION Intelligence Evaluation report.

## 3. Stop conditions (any one → halt immediately)
1. **Spend** reaches the $250 cap → stop acquisition.
2. **Volume** reaches 2,000 records → stop acquisition.
3. **Legal/ToS blocker** discovered (storage or use not permitted) → stop; do not proceed.
4. A **secret/credential** would have to be committed or exposed → stop; fix via secret manager.
5. **Sensitive/special-category PII** appears, or any compliance red flag → stop, quarantine, escalate.
6. **API instability** beyond a usable threshold (e.g., sustained errors/throttling that
   prevent a clean pull) → stop; report reliability as a finding.
7. **Legal review not complete** or CEO parameters not ratified → do not start.
8. **Scope creep** toward outreach/CRM/platform → stop (governance stop).

## 4. What "done" looks like
A single **AION Intelligence Evaluation** report containing the measured metrics
(headlined by cost-per-qualified-opportunity) and a recommendation, handed to the
CEO decision gate (`DECISION-FRAMEWORK.md`). The pilot dataset is retained per the
data-handling plan and deleted at end of retention.

## 5. Effort guardrail
This is a measurement pilot. If the work starts to look like building a platform,
that is a stop condition (see 3.8). The adapter should be a small, reviewable file;
the intelligence and output already exist.
