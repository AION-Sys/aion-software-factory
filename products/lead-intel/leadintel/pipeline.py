"""Pipeline orchestration.

Data Provider -> Raw Data -> Normalizer -> Enrichment -> Qualification Engine
-> Lead Record -> Output.

The qualification engine is provider-independent: the pipeline hands it enriched
Lead records and a ScoringConfig, never provider-specific shapes.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import output
from .enrich import enrich
from .models import Lead, Query, Status
from .normalize import normalize
from .providers.base import ResearchProvider
from .providers.fixture import FixtureProvider
from .scoring.config import ScoringConfig, load_config
from .scoring.engine import qualify


@dataclass
class RunResult:
    """Observability summary for a pipeline run (see docs/operations/observability.md)."""
    query: dict
    provider: str
    is_synthetic: bool
    scoring_config_version: str
    total_leads: int
    by_status: dict
    by_category: dict
    average_score: float
    average_data_completeness: float
    provenance_complete_rate: float
    duration_ms: int
    files: dict = field(default_factory=dict)
    generated_at: str = ""

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        if self.is_synthetic:
            d["_disclaimer"] = ("SYNTHETIC run — results are from fixture data and are "
                                "NOT real-world evidence.")
        return d


def build_leads(
    query: Query,
    provider: ResearchProvider,
    config: ScoringConfig | None = None,
) -> list[Lead]:
    """Pure part: research -> normalize -> enrich -> qualify, sorted by score desc."""
    config = config or load_config()
    retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    is_synthetic = getattr(provider, "is_synthetic", False)

    leads: list[Lead] = []
    for raw in provider.search(query):
        nb = normalize(raw, provider.name, retrieved_at=retrieved_at, is_synthetic=is_synthetic)
        lead = enrich(nb)
        qualify(lead, query, config)
        leads.append(lead)
    leads.sort(key=lambda l: l.qualification_score, reverse=True)
    return leads


def run(
    query: Query,
    provider: ResearchProvider | None = None,
    out_dir: str | Path = "out",
    run_id: str | None = None,
    config: ScoringConfig | None = None,
) -> RunResult:
    """Full pipeline with file output. Returns a RunResult summary."""
    provider = provider or FixtureProvider()
    config = config or load_config()
    start = time.perf_counter()

    leads = build_leads(query, provider, config)

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
    by_category: dict = {}
    for lead in leads:
        by_category[lead.category_verdict.value] = by_category.get(lead.category_verdict.value, 0) + 1

    n = len(leads)
    avg_score = round(sum(l.qualification_score for l in leads) / n, 1) if n else 0.0
    avg_complete = round(sum(l.data_completeness for l in leads) / n, 3) if n else 0.0
    prov_rate = round(sum(1 for l in leads if l.provenance_complete) / n, 3) if n else 0.0

    result = RunResult(
        query={"market": query.market, "location": query.location, "limit": query.limit},
        provider=provider.name,
        is_synthetic=getattr(provider, "is_synthetic", False),
        scoring_config_version=config.version,
        total_leads=n,
        by_status=by_status,
        by_category=by_category,
        average_score=avg_score,
        average_data_completeness=avg_complete,
        provenance_complete_rate=prov_rate,
        duration_ms=int((time.perf_counter() - start) * 1000),
        files=files,
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    summary_path = base.parent / f"{run_id}.run-summary.json"
    Path(summary_path).write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
                                  encoding="utf-8")
    result.files["summary"] = str(summary_path)
    return result


def _default_run_id(query: Query) -> str:
    from .models import slugify
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{slugify(query.market)}_{slugify(query.location)}_{stamp}"
