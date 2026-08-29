# Testing Standards

Testing depth must match **risk**, not vanity metrics. These standards apply to all product repositories under AION.

## Principles

1. **Acceptance criteria drive tests** — Every mission criterion should map to at least one verification method (automated or documented manual).
2. **Test behavior, not implementation** — Prefer tests that survive refactors.
3. **Fail in CI, not production** — PRs must not merge with failing required checks.
4. **No untested critical paths** — Auth, payments, data mutations, and permission checks require automated coverage.

## Test Pyramid (Default)

| Layer | Scope | When required |
|-------|-------|---------------|
| Unit | Pure logic, utilities, validators | Always for non-trivial logic |
| Integration | DB, API routes, service boundaries | Data access and API changes |
| E2E | Critical user journeys | Auth, checkout, core workflow changes |

UI-only changes may rely on manual QA plus lint/build checks if no logic changed.

## Minimum CI Checks (Product Repos)

Every product repo should run on pull request:

- [ ] Lint / format
- [ ] Type check (TypeScript projects)
- [ ] Unit + integration tests
- [ ] Build succeeds

E2E may run on main or nightly if too slow for every PR; document the choice in product `ARCHITECTURE.md`.

## Definition of Test-Complete (Builder)

Before handoff to QA:

- [ ] New/changed logic has tests or documented manual test steps in PR
- [ ] All existing tests pass locally and in CI
- [ ] Flaky tests are fixed or quarantined with tracked follow-up (not ignored)

## QA Verification

QA confirms:

- [ ] Each acceptance criterion has pass/fail evidence
- [ ] Regression spot-checks on adjacent features
- [ ] Edge cases called out in PRD are exercised

## Anti-Patterns

- Merging with "will add tests later" on critical paths
- Tests that assert implementation details and break every refactor
- 100% coverage targets on UI boilerplate with zero integration tests
- Skipping CI because "it's a small change"

## Agent Responsibility

- **Builder:** Writes and maintains tests for changed code.
- **QA:** Validates criteria coverage; does not substitute for missing automated tests on critical paths.
- **Architect:** Specifies which layers are required per task.
