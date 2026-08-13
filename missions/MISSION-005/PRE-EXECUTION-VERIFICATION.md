# Pre-Execution Verification Packet — MISSION-005 (gates 1–6, 8)

Prepares the gates that require a human (CEO / legal / procurement). AION cannot
close these — no signup, quote, credential, or legal opinion can be produced by the
agent. This packet makes each one a short, concrete action.

## Gate 1 — Written provider quote (procurement action)
Request from Data Axle, in writing, before any purchase:
- [ ] Unit price per record for the **API** at pilot scale (≤500 records).
- [ ] **Billing model**: per-record? per-query? monthly minimum? setup fee?
      (Determines whether our client-side spend cap is sufficient — see security
      finding A2.)
- [ ] Any minimum spend / contract term.
- [ ] Documented **rate limits** and throughput.
- [ ] **Retention** obligations (how long we may keep records; deletion duties).
- [ ] Confirmation the **API returns NAICS 238210** records for the Denver metro.
> Record the verified **cost per record** here for the runbook: `________`

## Gate 2 — Terms of Service review
- Mission 004 summary (via search; primary read still required): Google/Data Axle/PDL
  terms in `missions/MISSION-004/PROVIDER-COMPARISON.md` and `RISK-REVIEW.md`.
- [ ] Read the current Data Axle Terms directly (data-axle.com/terms-and-conditions).
- [ ] Confirm no clause prohibits our Provider→Intelligence→verified-dataset use.

## Gate 3 — Data licensing / commercial use
- Known (Mission 004): limited, non-exclusive, internal-use license; **redistribution/
  resale prohibited**; Data Axle owns the data.
- [ ] Legal confirms internal lead-intelligence + storage is within the license.
- [ ] Confirm we will **not** resell/share lists (already an OUT-OF-SCOPE constraint).

## Gate 4 — Storage / retention / deletion
- Our controls (`DATA-HANDLING-PLAN.md`): encrypted, access-controlled, **non-repo**
  storage; retention ≤30 days (or shorter per license); documented deletion.
- [ ] Reconcile our 30-day retention with the provider's contractual requirement.
- [ ] Confirm deletion procedure satisfies the license's own deletion duties.

## Gate 5 — PII handling
- Rules set (`DATA-HANDLING-PLAN.md`): business + business-role contacts only; no
  special-category PII; honor deletion/opt-out; **no outreach**.
- [ ] DPA in place if personal data (exec contacts) is involved.
- [ ] Confirm CCPA/state obligations for stored exec-contact PII are covered.

## Gate 6 — Legal review of HIGH-risk items (counsel sign-off)
Items for counsel (from `missions/MISSION-004/RISK-REVIEW.md`):
- [ ] Storage of licensed data for internal use — permitted?
- [ ] Redistribution boundary — internal use only, confirmed.
- [ ] PII obligations + deletion/opt-out process — acceptable.
- [ ] DPA where personal data involved.
- [ ] Intended use permitted end-to-end.
> Legal sign-off recorded in `APPROVALS.md`.

## Gate 8 — Credentials via approved secret manager
- The adapter reads the key from `DATA_AXLE_API_KEY` (env / secret manager) **only**.
- [ ] Provision the API credential in the approved secret manager (never in the repo,
      never in a commit, never in a prompt, never in logs).
- [ ] Confirm least-privilege scope; dev credential separate from any production scope.
- [ ] Secret scan clean after any config change.

## Reminder
None of the above authorizes acquisition. When all are complete, update
`GATE-STATUS.md`, complete `APPROVALS.md`, and only then follow `EXECUTION-RUNBOOK.md`.
