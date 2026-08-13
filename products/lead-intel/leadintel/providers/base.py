"""Research provider interface and the raw record it returns.

A provider's only job is to *acquire* candidate businesses for a query. It does
not score or enrich. `RawBusiness` mirrors what a real source might legitimately
expose; every field is optional so absence flows through honestly (AC-6).
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Optional

from ..models import Query


@dataclass
class RawBusiness:
    """Loosely-typed business record as returned by a provider."""
    name: str
    website: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    categories: list[str] = field(default_factory=list)
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_form_url: Optional[str] = None
    socials: list[str] = field(default_factory=list)
    # Size signals (optional):
    employees: Optional[int] = None
    review_count: Optional[int] = None
    years_in_business: Optional[int] = None
    rating: Optional[float] = None
    # Decision-makers ONLY if the source legitimately provides them:
    decision_makers: list[dict] = field(default_factory=list)
    # Provenance:
    source_url: Optional[str] = None
    notes: str = ""


class ResearchProvider(abc.ABC):
    """Acquire candidate businesses for a query."""

    name: str = "abstract"
    # True for fixture/synthetic providers so downstream never treats their
    # output as real-world evidence (MISSION-003).
    is_synthetic: bool = False

    @abc.abstractmethod
    def search(self, query: Query) -> list[RawBusiness]:
        """Return raw candidate businesses for the query. No scoring/enrichment."""
        raise NotImplementedError
