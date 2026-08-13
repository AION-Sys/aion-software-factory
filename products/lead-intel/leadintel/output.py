"""OUTPUT / ORGANIZE — persist leads as JSONL, JSON, and CSV.

CSV flattens nested structures into operator-friendly columns. Missing values are
rendered as empty (CSV) / null (JSON), never invented. A `synthetic` column makes
fixture-sourced rows unmistakable so they are never read as real-world evidence.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Lead

# Column order for the operator-facing CSV (mirrors the required lead fields,
# now with category verdict, explainability, and data-quality signals).
CSV_COLUMNS = [
    "id",
    "company",
    "synthetic",
    "category_verdict",
    "status",
    "qualification_score",
    "estimated_opportunity",
    "website",
    "location",
    "service_type",
    "decision_makers",
    "phone",
    "email",
    "contact_form_url",
    "socials",
    "score_breakdown",
    "why",
    "category_reason",
    "estimated_opportunity_basis",
    "data_completeness",
    "provenance_complete",
    "research_notes",
    "source_provider",
    "source_url",
    "retrieved_at",
    "scoring_config_version",
]


def write_jsonl(leads: list[Lead], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for lead in leads:
            fh.write(json.dumps(lead.to_dict(), ensure_ascii=False) + "\n")
    return path


def write_json(leads: list[Lead], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_disclaimer": _disclaimer(leads),
        "count": len(leads),
        "leads": [lead.to_dict() for lead in leads],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return path


def write_csv(leads: list[Lead], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for lead in leads:
            writer.writerow(_row(lead))
    return path


def _disclaimer(leads: list[Lead]) -> str:
    if any(l.is_synthetic for l in leads):
        return ("Contains SYNTHETIC (fixture) leads — labeled per row via `synthetic`. "
                "Synthetic data is NOT real-world evidence.")
    return ""


def _row(lead: Lead) -> dict:
    dms = "; ".join(
        " ".join(p for p in (dm.name, f"({dm.title})" if dm.title else "") if p)
        for dm in lead.decision_makers
    )
    breakdown = ", ".join(f"{k}={v}" for k, v in lead.score_breakdown.items())
    why = " | ".join(
        f"{c.signal} {'+' if c.points >= 0 else ''}{c.points}: {c.reason}"
        for c in lead.score_contributions
    )
    return {
        "id": lead.id,
        "company": lead.company,
        "synthetic": "yes" if lead.is_synthetic else "no",
        "category_verdict": lead.category_verdict.value,
        "status": lead.status.value,
        "qualification_score": lead.qualification_score,
        "estimated_opportunity": lead.estimated_opportunity.value,
        "website": lead.website or "",
        "location": lead.location.as_text(),
        "service_type": "; ".join(lead.service_type),
        "decision_makers": dms,
        "phone": lead.contact_channels.phone or "",
        "email": lead.contact_channels.email or "",
        "contact_form_url": lead.contact_channels.contact_form_url or "",
        "socials": "; ".join(lead.contact_channels.socials),
        "score_breakdown": breakdown,
        "why": why,
        "category_reason": lead.category_reason,
        "estimated_opportunity_basis": lead.estimated_opportunity_basis,
        "data_completeness": lead.data_completeness,
        "provenance_complete": "yes" if lead.provenance_complete else "no",
        "research_notes": lead.research_notes,
        "source_provider": lead.source.provider if lead.source else "",
        "source_url": (lead.source.url if lead.source else "") or "",
        "retrieved_at": (lead.source.retrieved_at if lead.source else "") or "",
        "scoring_config_version": lead.scoring_config_version,
    }
