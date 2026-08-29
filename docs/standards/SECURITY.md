# Security Standards

Security is a gate, not an afterthought. These baselines apply to all AION product work.

## Non-Negotiables

1. **No secrets in source** — API keys, tokens, passwords, and private keys never belong in git, logs, issues, or agent prompts.
2. **Least privilege** — Production access is scoped, time-bound, and human-approved.
3. **Dependencies** — Known high/critical CVEs in direct dependencies must be addressed or explicitly accepted with documented rationale.
4. **User data** — Collect minimum necessary; encrypt in transit; document retention and deletion.
5. **Auth** — Use established libraries/patterns; never roll custom crypto or session schemes without Security review.

## When Security Review Is Mandatory

See `docs/workflows/END_TO_END.md` Phase 5 triggers. When in doubt, request review.

## Builder Checklist (Security-Relevant PRs)

- [ ] No secrets or credentials in diff
- [ ] Input validated at trust boundaries
- [ ] Authorization checked on every protected action (not just UI hiding)
- [ ] Errors do not leak internal paths, stack traces, or secrets to clients
- [ ] New dependencies justified and scanned
- [ ] SQL/NoSQL queries parameterized (no string concatenation)

## Security Review Severity

| Level | Action |
|-------|--------|
| **Blocker** | Must fix before merge |
| **High** | Fix before production deploy |
| **Medium** | Fix or accept with mitigation plan |
| **Low / Info** | Track; fix when convenient |

## Production and Infrastructure

Requires **human approval** per `AION_ENGINEERING.md`:

- Production deployment
- Production data migrations
- IAM / permission changes
- New third-party services processing user data
- Changes to encryption, backup, or disaster recovery

## Incident Response (Product Repos)

Product repos must document in `ARCHITECTURE.md`:

- Who is notified for security issues
- How to rotate credentials
- Where audit logs live (if applicable)

Factory repo does not hold production credentials or run incident response for live products.

## Agent Responsibility

- **Builder:** Follow checklist; escalate uncertainty.
- **Security:** Complete review template; classify findings clearly.
- **CEO / Human:** Accepts residual risk when documented.
