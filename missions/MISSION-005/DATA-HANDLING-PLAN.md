# Data Handling Plan — MISSION-005

How real pilot data is stored, protected, retained, and deleted. Operationalizes
`docs/operations/live-provider-activation-checklist.md` (§B/§C) and the HIGH items
from `missions/MISSION-004/RISK-REVIEW.md`. Nothing here runs until legal signs off.

## Storage (controlled)
- Pilot data is stored in an **access-controlled, non-repo location** (private,
  encrypted at rest; e.g., a restricted object store or an encrypted local volume).
- **The git repository never contains real prospect data.** `.gitignore` already
  blocks `out/` and product run outputs; real datasets live outside the repo entirely.
- Access limited to the pilot operator (least privilege). No sharing, no export beyond
  the pilot's evaluation.

## Credentials
- Data Axle API credentials via **secret manager / environment variable only** — never
  committed, logged, printed, or placed in prompts. Separate dev credentials; no
  production scope.

## PII rules
- Capture only **legitimately-available business** information and **business-role**
  decision-maker contacts (name, title). No special-category/sensitive PII.
- Absence stays explicit (the engine never fabricates).
- **No outreach** to any individual during or after the pilot (separate future mission).
- Honor deletion/opt-out: maintain the ability to remove any record on request.

## Retention & deletion
- Retain pilot data **≤30 days** (ratified; or the shorter period the Data Axle
  license requires), solely to compute and verify metrics. Any longer retention
  requires CEO approval + documented legal/privacy review.
- **Deletion procedure:** at end of retention (or on request/opt-out), delete the
  dataset and any derived files from the controlled store; record the deletion in the
  mission `Log`. Verify the license's own deletion obligations are met.

## Security controls
- Encryption in transit (HTTPS) and at rest.
- Call logs capture counts/latency/errors only — **no secrets, no PII in logs**.
- AION-SECURITY reviews the `DataAxleProvider` adapter before it runs.
- Secret scan must be clean before any commit.

## Legal review required before execution (must be signed off)
From Mission 004's risk review, resolve for Data Axle specifically:
1. May we **store** acquired records for internal use in AION's workflow? (retention terms)
2. **Redistribution** boundary confirmed — internal use only; never resell/share lists.
3. **PII obligations** for executive contacts (CCPA/state) and a deletion/opt-out process.
4. A **Data Processing Agreement** where personal data is involved.
5. Confirmation that the intended Provider→Intelligence→verified-dataset use is permitted.

If any of these returns "no" or "unclear," the pilot does not start (stop condition).
