"""Pipeline orchestration: INPUT -> RESEARCH -> ENRICH -> QUALIFY -> ORGANIZE -> OUTPUT."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import output
from .enrich import enrich
from .models import Lead, Query, Status
from .providers.base import ResearchProvider
from .providers.fixture import FixtureProvider
from .qualify import qualify


@dataclass
class RunResult:
    """Observability summary for a pipeline run (see docs/operations/observability.md)."""
    query: dict
    provider: str
    total_leads: int
    by_status: dict
    average_score: float
    duration_ms: int
    files: dict = field(default_factory=dict)
    generated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "provider": self.provider,
            "total_leads": self.total_leads,
            "by_status": self.by_status,
            "average_score": self.average_score,
            "duration_ms": self.duration_ms,
            "files": self.files,
            "generated_at": self.generated_at,
        }


def build_leads(query: Query, provider: ResearchProvider) -> list[Lead]:
    """Pure part: research -> enrich -> qualify, sorted by score desc."""
    retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    raw_records = provider.search(query)
    leads: list[Lead] = []
    for raw in raw_records:
        lead = enrich(raw, query, retrieved_at=retrieved_at)
        if lead.source:
            lead.source.provider = provider.name
        qualify(lead, query)
        leads.append(lead)
    leads.sort(key=lambda l: l.qualification_score, reverse=True)
    return leads


def run(
    query: Query,
    provider: ResearchProvider | None = None,
    out_dir: str | Path = "out",
    run_id: str | None = None,
) -> RunResult:
    """Full pipeline with file output. Returns a RunResult summary."""
    provider = provider or FixtureProvider()
    start = time.perf_counter()

    leads = build_leads(query, provider)

    out_dir = Path(out_dir)
    run_id = run_id or _default_run_id(query)
    base = out_dir / run_id
    files = {
        "jsonl": str(output.write_jsonl(leads, base.with_suffix(".jsonl"))),
        "json": str(output.write_json(leads, base.with_suffix(".json"))),
        "csv": str(output.write_csv(leads, base.with_suffix(".csv"))),
    }

    by_status = {s.value: 0 for s in Status}
    for lead in leads:
        by_status[lead.status.value] += 1
    avg = round(sum(l.qualification_score for l in leads) / len(leads), 1) if leads else 0.0
    duration_ms = int((time.perf_counter() - start) * 1000)

    result = RunResult(
        query={"market": query.market, "location": query.location, "limit": query.limit},
        provider=provider.name,
        total_leads=len(leads),
        by_status=by_status,
        average_score=avg,
        duration_ms=duration_ms,
        files=files,
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    # Write run summary alongside outputs (observability).
    summary_path = base.parent / f"{run_id}.run-summary.json"
    output.Path(summary_path).write_text(_json(result.to_dict()), encoding="utf-8")
    result.files["summary"] = str(summary_path)
    return result


def _default_run_id(query: Query) -> str:
    from .models import slugify
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{slugify(query.market)}_{slugify(query.location)}_{stamp}"


def _json(obj: dict) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False, indent=2)
