# Execution Runbook — MISSION-005 (run ONLY after all gates pass)

A controlled, scientific procedure. **Do not start** until `GATE-STATUS.md` shows all
12 gates SATISFIED and `APPROVALS.md` is fully signed. If any step trips a stop
condition, **halt and return to the CEO — do not improvise around a gate.**

## Pre-flight (confirm, do not assume)
1. `GATE-STATUS.md`: all 12 SATISFIED. `APPROVALS.md`: CEO + legal + security signed.
2. Verified `cost_per_record_usd` from the written quote is recorded; billing model
   confirmed per-record (else re-derive cap — security finding A2).
3. Credential present in the secret manager (`DATA_AXLE_API_KEY`); secret scan clean.
4. Baseline frozen (`MEASUREMENT-BASELINE.md`); tests green (`python3 -m unittest discover -s tests`).
5. Live transport implemented **and re-reviewed** by AION-SECURITY; `parse_record`
   validated against a real response sample (finding A1).

## Enablement (encodes every cap)
Construct the provider with the ratified, technically-enforced limits:
```
DataAxleProvider(
    enabled=True,
    api_key_env="DATA_AXLE_API_KEY",   # value in secret manager only
    max_records=500,                    # volume cap
    spend_cap_usd=100.0,                # hard spend cap
    cost_per_record_usd=<verified quote>,   # arms the spend cap (gate 1)
    allowed_market_tokens=("denver","aurora","lakewood","co","colorado"),
    naics="238210",
    transport=<reviewed live transport>,
)
```

## Acquisition (bounded, logged)
6. Run one bounded pull for the approved market via the existing pipeline
   (`run(query, provider, out_dir=<controlled non-repo path>)`).
7. Log per-call count, latency, and errors (no secrets, no PII) for API-reliability
   metrics. Record the **real invoice** total.
8. Verify the acquired count ≤ 500 and spend ≤ $100. If either is breached →
   **STOP** (this should be impossible given the adapter, but verify).

## Intelligence (existing engine, unchanged)
9. The pipeline normalizes → enriches → qualifies with **config v1.0.0**. No scoring
   changes. Output the verified lead dataset + run summary to controlled storage.

## Measurement
10. Draw the random **n=100** human-label sample; apply the rubric
    (`MEASUREMENT-PLAN.md` §A). Keep MACHINE output and HUMAN labels separate.
11. Compute every metric in `MEASUREMENT-BASELINE.md`; mark each PASS/FAIL vs. the
    frozen thresholds. Headline: **cost per usable qualified opportunity**.
12. Write `AION-INTELLIGENCE-EVALUATION.md` (created at execution) with the metrics
    table, confusion matrix, real economics, API reliability, legal/security status,
    and a single recommendation.

## Stop conditions (any one → halt immediately, return to CEO)
Unexpected PII · legal ambiguity · provider restriction · cost anomaly · data-quality
failure · API instability · security issue · scope creep · cap breach.

## Decision
13. Route the evaluation to `DECISION-FRAMEWORK.md`: **APPROVE / ITERATE / REJECT**.
    Thresholds are frozen; only an explicitly-permitted ITERATE may re-measure.

## Post-run hygiene
14. Enforce retention (≤30 days or shorter per license); delete the dataset and
    derived files from controlled storage at end of retention; record the deletion in
    the mission `Log`. Revoke/rotate credentials if the pilot is complete.
15. Confirm no real prospect data or credential ever entered the git repository.

> APPROVE authorizes acquiring data for the verified-dataset workflow only. Outreach,
> CRM, and autonomous workflows remain separate missions with their own gates.
