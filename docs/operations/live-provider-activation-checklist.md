# Live Provider Activation Checklist (CEO Gate)

The exact, ordered steps required to move from the current **synthetic-only**
system to a **live data provider**. This is a **YELLOW gate** (ADR-0005): nothing
here may be executed until the CEO explicitly approves in writing.

> Current state: **READY FOR LIVE PROVIDER DECISION** — not approved. Every box
> below is unchecked by design.

## A. Exact decision required from the CEO
The CEO must approve, in writing (recorded in the mission `Log`), all of:
1. **Which provider** (from a completed provider-evaluation comparison).
2. **Budget** — a spending cap for the provider (a paid service = YELLOW; the
   purchase itself is a human-only RED action performed by a human).
3. **Target market + volume** for the first live run.
4. **Data-handling terms**: retention window and deletion process for any PII.
5. **Authorization to store real prospect data** in a defined, access-controlled
   location (not this git repo).

Absent any one of these, activation does not proceed.

## B. Pre-activation checklist (before any live call)
- [ ] Provider passed the evaluation framework (mandatory ⚑ dimensions ≥ 3).
- [ ] ToS / licensing / permitted-use confirmed and archived.
- [ ] DPA / privacy terms in place where personal data is involved.
- [ ] Credentials provisioned via **secret manager / env var only** — never in
      the repo, logs, or prompts.
- [ ] Least-privilege API scope; separate dev vs. production credentials.
- [ ] Real-data storage location defined, access-controlled, and git-ignored.
- [ ] Retention + deletion procedure documented and testable.

## C. Security & privacy checklist (must all hold)
- [ ] No secret is committed, logged, or printed (secret scan clean).
- [ ] Personal data limited to legitimately-available business-role contacts.
- [ ] PII fields remain optional and explicit; nothing fabricated.
- [ ] Provenance captured per record (source URL + retrieval timestamp).
- [ ] Rate limiting / backoff respects the provider's limits and ToS.
- [ ] Deletion request path verified (we can remove a record on request).
- [ ] AION-SECURITY has reviewed the live `LiveProvider` implementation.

## D. Implementation & validation
- [ ] Implement `LiveProvider.search` (in `leadintel/providers/live.py`) against
      the approved provider; keep normalizer/enrichment/qualification unchanged.
- [ ] Set `is_synthetic=false` for live output; confirm the synthetic label never
      appears on real leads.
- [ ] Run a **small** bounded pilot within budget.
- [ ] Recompute metrics on a human-labeled real sample; compare to the synthetic
      baseline. Recalibrate scoring config if precision/FP rate warrant it.
- [ ] Record results and residual risk; obtain CEO sign-off before scaling.

## E. Explicitly still out of scope at activation
- Automated outreach to real people (separate future mission; RED for now).
- Production deployment of any service.
- Any purchase or commitment beyond the CEO-approved budget.

## Rollback
Disable the live provider (set `enabled=false`), revoke credentials, and stop
storing real data. Synthetic operation continues unaffected.
