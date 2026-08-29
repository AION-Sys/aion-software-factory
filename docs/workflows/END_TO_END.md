# End-to-End Delivery Workflow

This is the standard path from CEO objective to reviewable, mergeable software. Every product mission follows these phases unless the mission explicitly scopes down.

## Flow

```
CEO Objective
     │
     ▼
┌─────────┐    ┌─────────────┐    ┌──────────┐    ┌─────┐    ┌──────────┐    ┌──────────────┐
│ AION-PM │───▶│AION-ARCHITECT│───▶│AION-BUILDER│───▶│ QA  │───▶│ SECURITY │───▶│ Human Approval│
└─────────┘    └─────────────┘    └──────────┘    └─────┘    └──────────┘    └──────────────┘
  Mission         Architecture        PR(s)         Report      (if needed)      Merge / Deploy
  + PRD           + Tasks
```

## Phase 1 — PM (Mission + PRD)

**Input:** CEO objective or approved product problem.

**Actions:**
1. Create or update a mission file in `missions/` using `docs/templates/MISSION.template.md`.
2. Write acceptance criteria that are testable and unambiguous.
3. Define scope, out-of-scope, success metrics, and CEO approval gates.
4. Produce a PRD in the product repo from `docs/templates/PRD.template.md`.

**Output:** Approved mission (status `ACTIVE`) + PRD linked from mission.

**Gate:** CEO approves mission scope before Architect begins material design work.

## Phase 2 — Architect (Design + Tasks)

**Input:** Active mission + PRD.

**Actions:**
1. Read `AION_ENGINEERING.md`, mission acceptance criteria, and PRD.
2. Write `docs/ARCHITECTURE.md` in the product repo from template.
3. Break work into ordered, small tasks (each completable in one PR where possible).
4. Flag security-sensitive areas for mandatory Security review.
5. Document stack deviations if any.

**Output:** Architecture doc + task list (issues or task files).

**Gate:** Human approval for material architecture changes or new paid services.

## Phase 3 — Builder (Implementation)

**Input:** Approved architecture + tasks within mission scope.

**Actions:**
1. Implement on a feature branch; one focused change set per PR.
2. Add or update tests appropriate to risk (`docs/standards/TESTING.md`).
3. Update docs when behavior or architecture changes.
4. Fill PR description using product repo PR template; reference mission and task.
5. Run local/CI checks before requesting review.

**Output:** Pull request(s) ready for QA.

**Gate:** No production deploy or credential changes without explicit approval.

## Phase 4 — QA (Verification)

**Input:** PR + mission acceptance criteria + PRD.

**Actions:**
1. Verify each acceptance criterion; record pass/fail with evidence.
2. Run automated test suite; perform exploratory testing on changed surfaces.
3. File defects as PR comments or follow-up tasks; do not silently accept gaps.
4. Complete `docs/templates/QA_REPORT.template.md`.

**Output:** QA report attached to PR or stored in product repo `docs/`.

**Gate:** All acceptance criteria must pass or be explicitly deferred with CEO approval.

## Phase 5 — Security (Conditional)

**Trigger when changes touch:**
- Authentication, authorization, or session handling
- Secrets, credentials, or encryption
- User data collection, storage, or export
- External integrations or webhooks
- Infrastructure, IAM, or network boundaries
- Dependencies with known CVE relevance

**Actions:**
1. Complete `docs/templates/SECURITY_REVIEW.template.md`.
2. Classify findings: block / mitigate / accept with documented rationale.

**Output:** Security review linked to PR.

**Gate:** Blockers must be resolved before merge unless CEO accepts documented risk.

## Phase 6 — Human Approval

**Input:** PR + QA report (+ security review if applicable).

**Actions:**
1. Human reviewer confirms scope, quality, and gate compliance.
2. Approve merge or request changes.
3. For production deploy: separate explicit approval per mission gate.

**Output:** Merged PR; mission acceptance criteria checked off; deploy when authorized.

## Handoff Checklist (All Agents)

Every handoff must include:
- [ ] What was requested
- [ ] What was completed
- [ ] Files/artifacts changed
- [ ] Tests/checks performed
- [ ] Known limitations
- [ ] Risks
- [ ] Next recommended action
- [ ] Whether human approval is required

## Mission Lifecycle States

| Status | Meaning |
|--------|---------|
| `DRAFT` | PM writing; not yet approved for execution |
| `ACTIVE` | Approved; agents may execute within scope |
| `BLOCKED` | Waiting on human decision or external dependency |
| `COMPLETE` | Acceptance criteria satisfied; artifacts archived |
| `CANCELLED` | Scope abandoned; document reason |

## Speed Without Sacrificing Quality

- **Parallelize safely:** Architect can draft tasks while PM finalizes edge cases only if mission is `ACTIVE` and scope is frozen.
- **Don't skip phases:** Shortcuts create rework; QA and Security are cheaper before production.
- **Default to templates:** Copy from `docs/templates/`; do not rewrite structure per mission.
