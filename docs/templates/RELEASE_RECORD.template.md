# Release Record — {Release Name}

## References
- **Mission:** {link}
- **Commit:** {SHA}
- **Date:** {YYYY-MM-DD}
- **Release owner:** AION-RELEASE

## Environment
- **URL:** {production URL}
- **Provider:** {e.g., Vercel}
- **Database:** {Supabase project ref — no secrets}

## Pre-deploy checklist
- [ ] QA report approved
- [ ] Security review complete (if triggered)
- [ ] CEO production deploy approval recorded
- [ ] CI green on release commit

## Deploy steps
1. {Step}
2. {Step}

## Post-deploy smoke checks
- [ ] App loads
- [ ] Auth works (if applicable)
- [ ] Critical path: pre-call → call → post-call

## Rollback plan
{How to revert if smoke checks fail}

## Handoff
- [ ] Sales/users notified for real-world usage
- [ ] Validation tracking started (`docs/VALIDATION.md`)
