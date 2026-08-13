"""ENRICH — NormalizedBusiness -> Lead (the Lead Record).

In V1 (offline, no live provider) enrichment is derivation only: it computes data
completeness and provenance completeness, and writes honest research notes. It
never fabricates. Real external enrichment (e.g. firmographics) is a future,
approved capability that plugs in here.
"""
from __future__ import annotations

from .models import Lead, NormalizedBusiness

# Key fields used to measure how complete a lead's data is.
_COMPLETENESS_FIELDS = (
    "company", "website", "location_city", "category",
    "contact", "size_signal", "decision_maker",
)


def enrich(nb: NormalizedBusiness) -> Lead:
    notes = nb.provider_notes
    if not nb.decision_makers and "decision-maker" not in notes.lower():
        notes = _append(notes, "No decision-maker legitimately available at research time.")
    if not nb.website and "website" not in notes.lower():
        notes = _append(notes, "No website found.")

    lead = Lead(
        company=nb.company,
        location=nb.location,
        website=nb.website,
        service_type=list(nb.categories),
        contact_channels=nb.contact_channels,
        decision_makers=list(nb.decision_makers),
        size_signals=nb.size_signals,
        source=nb.source,
        research_notes=notes,
    )
    lead.data_completeness = _completeness(lead)
    lead.provenance_complete = _provenance_complete(lead)
    return lead


def _completeness(lead: Lead) -> float:
    present = {
        "company": bool(lead.company),
        "website": bool(lead.website),
        "location_city": bool(lead.location.city),
        "category": bool(lead.service_type),
        "contact": lead.contact_channels.has_any(),
        "size_signal": lead.size_signals.any_present(),
        "decision_maker": bool(lead.decision_makers),
    }
    return round(sum(1 for v in present.values() if v) / len(_COMPLETENESS_FIELDS), 3)


def _provenance_complete(lead: Lead) -> bool:
    s = lead.source
    return bool(s and s.provider and s.url and s.retrieved_at)


def _append(notes: str, extra: str) -> str:
    return f"{notes} {extra}".strip() if notes else extra
