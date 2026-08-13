import unittest

from leadintel.models import CategoryVerdict, Opportunity, Status
from leadintel.qualify import QUALIFY_THRESHOLD, REVIEW_THRESHOLD
from tests.helpers import CONFIG, DEFAULT_QUERY, make_lead


class TestQualify(unittest.TestCase):
    def test_strong_electrical_lead_is_qualified(self):
        lead = make_lead(
            name="Denver Electric Contractors",
            website="https://example.com/x", city="Denver", region="CO", country="USA",
            categories=["electrical contractor", "commercial electrical"],
            phone="+1-303-555-0000", employees=60, review_count=200, years_in_business=20,
            decision_makers=[{"name": "Sample Owner", "title": "Owner"}],
        )
        self.assertEqual(lead.category_verdict, CategoryVerdict.ELECTRICAL)
        self.assertGreaterEqual(lead.qualification_score, QUALIFY_THRESHOLD)
        self.assertEqual(lead.status, Status.QUALIFIED)
        self.assertEqual(lead.estimated_opportunity, Opportunity.HIGH)

    # --- Q1 FIX: non-electrical trades must never qualify ------------------------
    def test_handyman_with_minor_electrical_is_disqualified(self):
        """Regression for MISSION-002 Q1: a handyman advertising 'minor electrical'."""
        lead = make_lead(
            name="Denver Handyman & Minor Electrical",
            website="https://example.com/h", city="Denver", region="CO",
            categories=["handyman", "home repair", "minor electrical work"],
            phone="+1-303-555-0001", review_count=45, years_in_business=6,
        )
        self.assertEqual(lead.category_verdict, CategoryVerdict.NON_ELECTRICAL)
        self.assertEqual(lead.status, Status.DISQUALIFIED)

    def test_plumber_and_hvac_and_gc_never_qualify(self):
        for cats in (["plumber", "plumbing"], ["hvac", "heating and cooling"],
                     ["general contractor", "remodeling"]):
            lead = make_lead(
                name="Trade Co", website="https://example.com/t", city="Denver", region="CO",
                categories=cats, phone="+1-303-555-0002",
                employees=80, review_count=300, years_in_business=25,
                decision_makers=[{"name": "Owner"}],
            )
            self.assertEqual(lead.category_verdict, CategoryVerdict.NON_ELECTRICAL, cats)
            self.assertEqual(lead.status, Status.DISQUALIFIED, cats)

    def test_general_contractor_with_electrical_can_qualify(self):
        lead = make_lead(
            name="BuildRight GC & Electrical", website="https://example.com/b",
            city="Denver", region="CO", categories=["general contractor", "electrical contractor"],
            phone="+1-303-555-0003", employees=120, review_count=90, years_in_business=25,
        )
        self.assertEqual(lead.category_verdict, CategoryVerdict.ELECTRICAL)
        self.assertEqual(lead.status, Status.QUALIFIED)

    def test_adjacent_solar_only_cannot_qualify(self):
        lead = make_lead(
            name="PureSun Solar", website="https://example.com/s", city="Denver", region="CO",
            categories=["solar", "photovoltaic"], phone="+1-303-555-0004",
            review_count=80, years_in_business=9,
        )
        self.assertEqual(lead.category_verdict, CategoryVerdict.ADJACENT)
        self.assertNotEqual(lead.status, Status.QUALIFIED)

    def test_ambiguous_no_evidence_cannot_qualify(self):
        lead = make_lead(name="Current Solutions Group", website=None, city="Denver", region="CO",
                         categories=[])
        self.assertEqual(lead.category_verdict, CategoryVerdict.AMBIGUOUS)
        self.assertNotEqual(lead.status, Status.QUALIFIED)

    # --- Scoring properties -----------------------------------------------------
    def test_breakdown_sums_to_score(self):
        lead = make_lead(
            name="Mid Electric", website="https://example.com/m", city="Denver", region="CO",
            categories=["electrician"], phone="+1-303-555-0005",
            employees=10, review_count=30, years_in_business=6,
        )
        self.assertEqual(sum(lead.score_breakdown.values()), lead.qualification_score)

    def test_score_bounded_0_100(self):
        lead = make_lead(
            name="Max Electrical Contractor", website="https://example.com/z",
            city="Denver", region="CO", country="USA",
            categories=["electrical contractor", "commercial electrical", "industrial electrical"],
            phone="+1", email="a@example.com", contact_form_url="https://x", socials=["https://s"],
            employees=999, review_count=9999, years_in_business=99,
            decision_makers=[{"name": "A"}, {"name": "B"}],
        )
        self.assertGreaterEqual(lead.qualification_score, 0)
        self.assertLessEqual(lead.qualification_score, 100)

    def test_every_contribution_has_a_reason(self):
        lead = make_lead(name="Denver Electric", website="https://example.com/e",
                         city="Denver", region="CO", categories=["electrical contractor"],
                         phone="+1-303-555-0006")
        self.assertTrue(lead.score_contributions)
        for c in lead.score_contributions:
            self.assertTrue(c.reason, f"contribution {c.signal} missing reason")
            self.assertIn(c.kind, ("positive", "negative"))

    def test_negative_signal_reduces_score(self):
        lead = make_lead(name="Handy Home Helpers", city="Denver", region="CO",
                         categories=["handyman"])
        neg = [c for c in lead.score_contributions if c.kind == "negative"]
        self.assertTrue(neg, "expected a negative signal for a handyman")
        self.assertLess(min(c.points for c in neg), 0)

    def test_thresholds_from_config(self):
        self.assertEqual(QUALIFY_THRESHOLD, CONFIG.qualified_threshold)
        self.assertEqual(REVIEW_THRESHOLD, CONFIG.review_threshold)

    def test_deterministic(self):
        kw = dict(name="Denver Electric", website="https://example.com/e", city="Denver",
                  region="CO", categories=["electrical contractor"], phone="+1",
                  employees=40, review_count=100, years_in_business=12)
        a = make_lead(**kw)
        b = make_lead(**kw)
        self.assertEqual(a.qualification_score, b.qualification_score)
        self.assertEqual(a.score_breakdown, b.score_breakdown)
        self.assertEqual(a.status, b.status)


if __name__ == "__main__":
    unittest.main()
