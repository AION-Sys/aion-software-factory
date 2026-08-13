"""Shared test helpers."""
from __future__ import annotations

from leadintel.enrich import enrich
from leadintel.models import Query
from leadintel.normalize import normalize
from leadintel.providers.base import RawBusiness
from leadintel.scoring.config import load_config
from leadintel.scoring.engine import qualify

DEFAULT_QUERY = Query(market="electrical contractors", location="Denver, CO")
CONFIG = load_config()


def make_lead(query: Query = DEFAULT_QUERY, qualify_it: bool = True, **raw_kwargs):
    """Build a Lead from RawBusiness kwargs through normalize -> enrich -> qualify."""
    raw = RawBusiness(name=raw_kwargs.pop("name", "Test Electric"), **raw_kwargs)
    nb = normalize(raw, "fixture", is_synthetic=True)
    lead = enrich(nb)
    if qualify_it:
        qualify(lead, query, CONFIG)
    return lead
