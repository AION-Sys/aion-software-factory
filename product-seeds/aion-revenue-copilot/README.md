# AION Revenue Conversion Copilot

AI-assisted sales workspace for home-service contractors and SMB sales teams — the first **Factory → Product → Revenue → Learning** validation build (Mission 002).

## Mission
[aion-software-factory: MISSION-002](https://github.com/Ceoloo/aion-software-factory/blob/main/missions/MISSION-002.md)

## Workflow (MVP)
1. **Before conversation** — lead intelligence, pains, offer, recommended questions
2. **During conversation** — guidance, checklist, objections, qualification, next-best action
3. **After conversation** — structured outcome, CRM event, learning event

## Repository Structure

```
aion-revenue-copilot/
├── app/                 # Next.js routes
├── components/          # UI
├── lib/
│   ├── ai/              # AION AI Gateway client
│   ├── intelligence/    # Pre-call / during-call logic
│   ├── sales/           # Domain types
│   ├── learning/        # Learning event pipeline
│   └── crm/             # Persistence + CRM events
├── tests/
│   ├── unit/
│   ├── integration/
│   └── critical-path/
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   └── VALIDATION.md
└── .github/workflows/ci.yml
```

## Stack
Next.js · TypeScript · Supabase · AION AI Gateway · AION event/learning infrastructure · Vercel

## Local Development

```bash
cp .env.example .env.local
# Fill Supabase and AION gateway values (never commit secrets)
npm install
npm run dev
```

## Quality Checks

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

## Agent Contract
Agents follow [aion-software-factory AGENTS.md](https://github.com/Ceoloo/aion-software-factory/blob/main/AGENTS.md). Work in small PRs against tasks in `docs/ARCHITECTURE.md`.

## Validation
Real-world evidence goes in [`docs/VALIDATION.md`](docs/VALIDATION.md). Mission 002 does not close until Revenue + Validation gates pass.
