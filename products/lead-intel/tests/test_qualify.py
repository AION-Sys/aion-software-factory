import unittest

from leadintel.enrich import enrich
from leadintel.models import Opportunity, Query, Status
from leadintel.providers.base import RawBusiness
from leadintel.qualify import QUALIFY_THRESHOLD, REVIEW_THRESHOLD, qualify

QUERY = Query(market="electrical contractors", location="Austin, TX")


def _lead(**kw):
    raw = RawBusiness(name=kw.pop("name", "Test Electric"), **kw)
    return enrich(raw, QUERY)


class TestQualify(unittest.TestCase):
    def test_strong_lead_is_qualified(self):
        lead = _lead(
            name="Austin Electric Co",
            website="https://example.com/x",
            city="Austin", region="TX", country="USA",
            categories=["electrical contractor", "commercial electrical"],
            phone="+1-512-555-0000",
            employees=60, review_count=200, years_in_business=20,
            decision_makers=[{"name": "Sample Owner", "title": "Owner"}],
        )
        qualify(lead, QUERY)
        self.assertGreaterEqual(lead.qualification_score, QUALIFY_THRESHOLD)
        self.assertEqual(lead.status, Status.QUALIFIED)
        self.assertEqual(lead.estimated_opportunity, Opportunity.HIGH)

    def test_sparse_lead_is_disqualified(self):
        lead = _lead(
            name="Generic Handyman",
            website=None,
            city="Dallas", region="TX",
            categories=["handyman"],
        )
        qualify(lead, QUERY)
        self.assertLess(lead.qualification_score, REVIEW_THRESHOLD)
        self.assertEqual(lead.status, Status.DISQUALIFIED)

    def test_breakdown_sums_to_score(self):
        lead = _lead(
            name="Mid Electric",
            website="https://example.com/m",
            city="Austin", region="TX",
            categories=["electrician"],
            phone="+1-512-555-0001",
            employees=10, review_count=30, years_in_business=6,
        )
        qualify(lead, QUERY)
        self.assertEqual(sum(lead.score_breakdown.values()), lead.qualification_score)

    def test_score_is_bounded_0_100(self):
        lead = _lead(
            name="Max Electric Electrical Electrician Wiring Panel",
            website="https://example.com/z",
            city="Austin", region="TX", country="USA",
            categories=["electrical contractor"],
            phone="+1", email="a@example.com", contact_form_url="https://x",
            socials=["https://s"],
            employees=999, review_count=9999, years_in_business=99,
            decision_makers=[{"name": "A"}, {"name": "B"}],
        )
        qualify(lead, QUERY)
        self.assertGreaterEqual(lead.qualification_score, 0)
        self.assertLessEqual(lead.qualification_score, 100)

    def test_adjacent_service_scores_partial_relevance(self):
        core = _lead(name="Wiring Pros", city="Austin", region="TX",
                     categories=["electrical contractor"])
        adjacent = _lead(name="Solar Only Co", city="Austin", region="TX",
                         categories=["solar"])
        qualify(core, QUERY)
        qualify(adjacent, QUERY)
        self.assertGreater(core.score_breakdown["service_relevance"],
                           adjacent.score_breakdown["service_relevance"])
        self.assertGreater(adjacent.score_breakdown["service_relevance"], 0)

    def test_no_size_signals_gives_unknown_opportunity(self):
        lead = _lead(name="Austin Electric", city="Austin", region="TX",
                     categories=["electrical contractor"])
        qualify(lead, QUERY)
        self.assertEqual(lead.estimated_opportunity, Opportunity.UNKNOWN)
        self.assertEqual(lead.score_breakdown["opportunity_signal"], 0)

    def test_deterministic(self):
        a = _lead(name="Austin Electric", city="Austin", region="TX",
                  categories=["electrical contractor"], employees=40, review_count=100,
                  years_in_business=12, phone="+1", website="https://x")
        b = _lead(name="Austin Electric", city="Austin", region="TX",
                  categories=["electrical contractor"], employees=40, review_count=100,
                  years_in_business=12, phone="+1", website="https://x")
        qualify(a, QUERY)
        qualify(b, QUERY)
        self.assertEqual(a.qualification_score, b.qualification_score)
        self.assertEqual(a.score_breakdown, b.score_breakdown)


if __name__ == "__main__":
    unittest.main()
