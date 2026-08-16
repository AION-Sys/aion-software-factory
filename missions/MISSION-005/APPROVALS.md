# Required Approvals — MISSION-005 (before any execution)

The pilot does **not** start until every box below is checked. Boxes are unchecked by
design; the CEO and legal complete them. This operationalizes
`docs/operations/live-provider-activation-checklist.md` for the Data Axle pilot.

## A. CEO authorization (the five parameters — RATIFIED 2026-08-13)
The parameters below were **ratified by the CEO on 2026-08-13**. Sign-off here
confirms them; do not substitute the earlier proposed values.
- [ ] **Provider:** Data Axle confirmed for the pilot.
- [ ] **Spend cap:** hard, absolute not-to-exceed **$100 USD**.
- [ ] **Metro + volume:** one metro **Denver–Aurora–Lakewood, CO** and record cap **500**.
- [ ] **PII handling:** retention window **≤30 days** (or shorter per license; any
      longer requires CEO approval + legal/privacy review) + deletion/opt-out process.
- [ ] **Storage authorization:** approve storing real prospect data in the defined
      encrypted, access-controlled, non-repo location.

## B. Pre-registered thresholds
- [ ] CEO ratifies (or edits) the acceptance thresholds in `MEASUREMENT-PLAN.md` §C,
      especially the **cost-per-usable-opportunity** economic bar (#11).

## C. Legal sign-off (from `DATA-HANDLING-PLAN.md`)
- [ ] Storage for internal use permitted (retention terms confirmed).
- [ ] Redistribution boundary confirmed (internal use only; no resale/sharing).
- [ ] PII obligations + deletion/opt-out process acceptable.
- [ ] DPA in place where personal data is involved.
- [ ] Intended Provider→Intelligence→verified-dataset use is permitted.

## D. Technical pre-conditions
- [ ] Written Data Axle **quote** + rate-limit + retention terms obtained (no data pulled).
- [ ] Credentials provisioned via **secret manager / env only** (never committed).
- [ ] `DataAxleProvider` adapter implemented and **reviewed by AION-SECURITY** before it runs.
- [ ] Secret scan clean.

## Sign-off block (to be completed at authorization)
```
CEO approval:        __________________________   date: __________
Legal sign-off:      __________________________   date: __________
Security review:     __________________________   date: __________
Authorized spend cap: $__________   Metro: __________   Volume cap: __________
```

Until this page is complete, MISSION-005 remains **READY FOR CEO PILOT
AUTHORIZATION** and no data, credentials, or spend are involved.
