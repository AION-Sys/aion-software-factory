"""FixtureProvider — deterministic, offline, SYNTHETIC data.

Loads sample businesses from a fixture JSON. The data is fabricated for testing
the intelligence layer only; it does NOT describe real companies or real people
(see ADR-0005). Every lead produced from this provider is flagged
``is_synthetic`` end-to-end so it is never mistaken for real-world evidence.

Filtering here is intentionally simple (location + loose market match): finding
real businesses is a live-provider concern. The qualification engine — not the
provider — decides relevance.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from ..models import Query
from .base import RawBusiness, ResearchProvider

_DEFAULT_FIXTURE = (
    Path(__file__).resolve().parents[2] / "data" / "fixtures" / "electrical_contractors.json"
)

# Loose market tokens used only for provider-side prefiltering (not scoring).
_MARKET_HINTS = (
    "electric", "electrical", "electrician", "contractor", "contractors",
    "wiring", "panel", "lighting", "solar", "generator", "hvac", "plumb",
    "handyman", "roofing", "service", "services",
)


class FixtureProvider(ResearchProvider):
    name = "fixture"
    is_synthetic = True

    def __init__(self, fixture_path: Optional[Path] = None):
        self.fixture_path = Path(fixture_path) if fixture_path else _DEFAULT_FIXTURE

    def _load(self) -> list[dict]:
        with open(self.fixture_path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        return payload.get("businesses", [])

    def search(self, query: Query) -> list[RawBusiness]:
        records = self._load()
        loc = query.location.lower()
        market = query.market.lower()
        market_tokens = [t for t in market.replace(",", " ").split() if len(t) > 2]
        results: list[RawBusiness] = []
        for r in records:
            hay_loc = " ".join(
                str(r.get(k, "")) for k in ("city", "region", "country")
            ).lower()
            hay_cat = " ".join(r.get("categories", [])).lower() + " " + r.get("name", "").lower()
            loc_ok = (not loc) or any(tok in hay_loc for tok in _tokens(loc))
            market_ok = (
                (not market)
                or any(tok in hay_cat for tok in market_tokens)
                or any(hint in hay_cat for hint in _MARKET_HINTS)
            )
            if loc_ok and market_ok:
                results.append(_to_raw(r))
        if query.limit is not None:
            results = results[: query.limit]
        return results


def _tokens(text: str) -> list[str]:
    return [t for t in text.replace(",", " ").split() if len(t) > 1]


def _to_raw(r: dict) -> RawBusiness:
    return RawBusiness(
        name=r.get("name", "").strip(),
        website=r.get("website"),
        city=r.get("city"),
        region=r.get("region"),
        country=r.get("country"),
        categories=list(r.get("categories", [])),
        phone=r.get("phone"),
        email=r.get("email"),
        contact_form_url=r.get("contact_form_url"),
        socials=list(r.get("socials", [])),
        employees=r.get("employees"),
        review_count=r.get("review_count"),
        years_in_business=r.get("years_in_business"),
        rating=r.get("rating"),
        decision_makers=list(r.get("decision_makers", [])),
        source_url=r.get("source_url"),
        notes=r.get("notes", ""),
    )
