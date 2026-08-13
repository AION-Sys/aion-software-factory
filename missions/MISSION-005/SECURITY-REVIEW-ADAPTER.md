# AION-SECURITY Review — DataAxleProvider Adapter (MISSION-005, gate 7)

- **Reviewer:** AION-SECURITY (independent of the builder)
- **Subject:** `products/lead-intel/leadintel/providers/dataaxle.py`
- **Date:** 2026-08-13
- **Verdict:** APPROVED FOR THE DISABLED/PREPARATION STATE — with conditions that must
  hold before it is ever enabled.

## Scope
Reviews the adapter as written for pilot **preparation**. The adapter is not, and must
not be, enabled or run against the live API until every gate in `GATE-STATUS.md` is
satisfied. This review re-runs when the live transport is implemented.

## Checklist
| Area | Result | Notes |
|------|--------|-------|
| Secrets handling | OK | Credential read from `os.environ[api_key_env]` only; never hardcoded, logged, or committed. `_build_request` carries the env-var **name**, never the value. |
| No accidental network call | OK | `enabled` defaults `False`; real `_live_transport` raises `NotImplementedError`; all tests inject a mock. No live call originates from the repo. |
| Spend cap enforcement (gate 9) | OK | Refuses without a verified `cost_per_record_usd`; clamps record count to `spend_cap_usd // cost_per_record`; refuses if cap < one record. |
| Volume cap enforcement (gate 10) | OK | Clamps request to `max_records` (default 500) and re-clamps the response. |
| Market guard | OK | Refuses any location outside the approved Denver–Aurora–Lakewood tokens (no market expansion). |
| Vertical guard | OK | NAICS fixed to 238210 in the request builder. |
| Synthetic labeling integrity | OK | `is_synthetic = False`; real output is never mislabeled synthetic. Conversely, mock test data is confined to tests and produces no committed artifact. |
| PII in logs | OK | Adapter does not log; `_build_request` excludes secrets/PII. Call-logging (for reliability metrics) is specified in the runbook to exclude PII. |
| Input handling | OK | Uses `.get` defensively; tolerant of missing fields (absence preserved downstream). |

## Findings
| ID | Severity | Description | Required action |
|----|----------|-------------|-----------------|
| A1 | INFO | Field mapping in `parse_record` is based on **documented** Data Axle fields, not a verified live response. | Validate the mapping against a real response sample during execution before trusting parsed fields. |
| A2 | MEDIUM (pre-enable) | Spend-cap enforcement is client-side (record-count × unit price). It cannot see provider-side charges (e.g., minimums, per-query fees). | Confirm the true billing model from the written quote; if billing is not per-record, re-derive the cap enforcement before enabling. |
| A3 | INFO | No rate-limit/backoff logic yet. | Add per the provider's documented limits when the live transport is implemented; re-review. |

No hardcoded secrets. No live call path reachable in the current state.

## Conditions before enabling (must all hold)
1. All `GATE-STATUS.md` gates SATISFIED (esp. quote, legal, credentials in secret manager).
2. `cost_per_record_usd` set from the **written quote**; billing model confirmed (A2).
3. Live transport implemented with rate-limit/backoff and **re-reviewed** by AION-SECURITY.
4. `parse_record` validated against a real response sample (A1).
5. Secret scan clean; credentials confirmed absent from the repo and logs.

## Verdict
**APPROVED for the disabled preparation state.** The adapter safely encodes the
ratified caps and cannot acquire data or leak secrets as written. Enabling it is
gated on the conditions above and a second security review of the live transport.
