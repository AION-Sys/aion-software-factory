# Decision Framework — MISSION-005

How the CEO decides **after** the pilot runs and the AION Intelligence Evaluation is
produced. Defined **before** the pilot so the decision is rule-based, not vibes.

## Inputs to the decision
- The metrics table vs. the pre-registered thresholds (`MEASUREMENT-PLAN.md` §C),
  each marked PASS/FAIL.
- The headline number: **cost per usable sales opportunity** (#11).
- The legal storability determination (#15) — a hard gate.
- API reliability observations and any stop conditions hit.

## Decision rule
```
                         ┌─────────────────────────────────────────────┐
                         │ Legal storability (#15) = "yes"?             │
                         └─────────────────────────────────────────────┘
                              │ no                        │ yes
                              ▼                           ▼
                          REJECT              ┌───────────────────────────┐
                       (cannot use)           │ All HARD gates pass?       │
                                              │ - precision ≥ 0.85         │
                                              │ - provenance = 100%        │
                                              │ - cost/usable ≤ CEO bar    │
                                              └───────────────────────────┘
                                                │ no              │ yes
                                                ▼                 ▼
                                        ITERATE or REJECT     APPROVE provider
                                    (see disposition rules)  (authorize next layer)
```

## Dispositions
- **APPROVE provider** — legal = yes, and all hard gates (precision, provenance,
  cost-per-usable-opportunity ≤ the CEO's economic bar) pass, and no unresolved stop
  condition. → Authorize the **next layer** (enrichment / outreach / CRM) as a
  *separate* future mission with its own gates. Do **not** auto-start it.
- **ITERATE** — legal = yes, economics are promising, but one or more accuracy gates
  fail for a **fixable** reason (e.g., recall low → tune the scoring config;
  duplicates high → improve dedup). Re-run the *measurement* on the existing pilot
  dataset (no new spend) after the fix, or run one more bounded pull if justified —
  under a fresh cap. Cause of failure must be identified before iterating.
- **REJECT provider** — legal = no, OR economics fail the CEO's bar and no plausible
  fix closes the gap, OR data quality is structurally poor. → Return to Mission 004
  alternatives (e.g., Google Places as verification-only, or re-scope), or shelve
  live data.

## Anti-goodhart guardrails
- Thresholds are pre-registered; if the CEO changes the economic bar after seeing the
  data, record that explicitly as a decision input (not a silent edit).
- "ITERATE" requires a **named, testable cause** — not "try again and hope."
- A single passing metric never overrides a failed hard gate.

## What APPROVE does NOT authorize
Approving the provider authorizes acquiring data at scale for the verified-dataset
workflow. It does **not** authorize outreach, CRM, or autonomous revenue workflows —
each remains a distinct mission and gate.
