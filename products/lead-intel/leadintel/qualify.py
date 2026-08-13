"""QUALIFY — deterministic, explainable scoring.

Produces a 0-100 score with a per-signal breakdown (AC-3), a status (AC-4), and
an estimated opportunity tier (AC-5). All weights and thresholds are constants so
the model is transparent and tunable. Pure function: same input -> same output.
"""
from __future__ import annotations

from .models import Lead, Opportunity, Query, Status

# --- Scoring weights (sum of maxima = 100) ------------------------------------
W_SERVICE_RELEVANCE = 25
W_LOCATION_MATCH = 15
W_HAS_WEBSITE = 15
W_HAS_CONTACT = 15
W_OPPORTUNITY = 20   # scaled from size signals
W_DECISION_MAKER = 10

# --- Status thresholds --------------------------------------------------------
QUALIFY_THRESHOLD = 60
REVIEW_THRESHOLD = 40


def qualify(lead: Lead, query: Query) -> Lead:
    """Score the lead in place and return it (also returns for convenience)."""
    breakdown: dict[str, int] = {}

    breakdown["service_relevance"] = _service_relevance(lead, query)
    breakdown["location_match"] = _location_match(lead, query)
    breakdown["has_website"] = W_HAS_WEBSITE if lead.website else 0
    breakdown["has_contact"] = W_HAS_CONTACT if lead.contact_channels.has_any() else 0
    opp_points, tier, basis = _opportunity(lead)
    breakdown["opportunity_signal"] = opp_points
    breakdown["decision_maker"] = W_DECISION_MAKER if lead.decision_makers else 0

    score = sum(breakdown.values())
    score = max(0, min(100, score))

    lead.score_breakdown = breakdown
    lead.qualification_score = score
    lead.estimated_opportunity = tier
    lead.estimated_opportunity_basis = basis
    lead.status = _status_for(score)
    return lead


def _service_relevance(lead: Lead, query: Query) -> int:
    haystack = " ".join(lead.service_type + [lead.company]).lower()
    hits = [kw for kw in query.service_keywords if kw in haystack]
    if not hits:
        return 0
    # Full points if a core electrical term is present; partial for weak/adjacent match.
    core = {"electric", "electrical", "electrician", "wiring", "panel"}
    if any(h in core for h in hits):
        return W_SERVICE_RELEVANCE
    return int(W_SERVICE_RELEVANCE * 0.5)  # adjacent (solar/lighting/ev/generator only)


def _location_match(lead: Lead, query: Query) -> int:
    target = query.location.lower()
    tokens = [t for t in target.replace(",", " ").split() if len(t) > 1]
    hay = " ".join(
        v for v in (lead.location.city, lead.location.region, lead.location.country) if v
    ).lower()
    if not tokens or not hay:
        return 0
    matched = [t for t in tokens if t in hay]
    if not matched:
        return 0
    # Full points when every target token matches (e.g. city + state); partial otherwise.
    return W_LOCATION_MATCH if len(matched) == len(tokens) else int(W_LOCATION_MATCH * 0.6)


def _opportunity(lead: Lead) -> tuple[int, Opportunity, str]:
    """Estimate opportunity tier from available size signals -> (points, tier, basis)."""
    s = lead.size_signals
    signals = []
    strength = 0.0
    count = 0

    if s.employees is not None:
        count += 1
        if s.employees >= 50:
            strength += 1.0; signals.append(f"{s.employees} employees")
        elif s.employees >= 15:
            strength += 0.6; signals.append(f"{s.employees} employees")
        else:
            strength += 0.2; signals.append(f"{s.employees} employees")
    if s.review_count is not None:
        count += 1
        if s.review_count >= 150:
            strength += 1.0; signals.append(f"{s.review_count} reviews")
        elif s.review_count >= 40:
            strength += 0.6; signals.append(f"{s.review_count} reviews")
        else:
            strength += 0.2; signals.append(f"{s.review_count} reviews")
    if s.years_in_business is not None:
        count += 1
        if s.years_in_business >= 15:
            strength += 1.0; signals.append(f"{s.years_in_business}y in business")
        elif s.years_in_business >= 5:
            strength += 0.6; signals.append(f"{s.years_in_business}y in business")
        else:
            strength += 0.2; signals.append(f"{s.years_in_business}y in business")

    if count == 0:
        return 0, Opportunity.UNKNOWN, "No size signals available."

    normalized = strength / count  # 0..1
    points = round(W_OPPORTUNITY * normalized)
    if normalized >= 0.75:
        tier = Opportunity.HIGH
    elif normalized >= 0.45:
        tier = Opportunity.MEDIUM
    else:
        tier = Opportunity.LOW
    basis = f"{tier.value} from " + ", ".join(signals)
    return points, tier, basis


def _status_for(score: int) -> Status:
    if score >= QUALIFY_THRESHOLD:
        return Status.QUALIFIED
    if score >= REVIEW_THRESHOLD:
        return Status.NEEDS_REVIEW
    return Status.DISQUALIFIED
