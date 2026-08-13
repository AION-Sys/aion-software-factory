import unittest

from leadintel.enrich import enrich
from leadintel.normalize import normalize
from leadintel.providers.base import RawBusiness


def _enrich(**kw):
    raw = RawBusiness(name=kw.pop("name", "Test Electric"), **kw)
    return enrich(normalize(raw, "fixture", is_synthetic=True))


class TestNormalizeEnrich(unittest.TestCase):
    def test_missing_fields_are_none_not_fabricated(self):
        lead = _enrich(name="No Web Electric", city="Denver", region="CO")
        self.assertIsNone(lead.website)
        self.assertIsNone(lead.contact_channels.phone)
        self.assertEqual(lead.decision_makers, [])
        self.assertIn("No website found", lead.research_notes)
        self.assertIn("No decision-maker", lead.research_notes)

    def test_categories_lowercased_and_deduped(self):
        lead = _enrich(name="Electric", categories=["Electrical Contractor", "electrical contractor", " Electrician "])
        self.assertEqual(lead.service_type, ["electrical contractor", "electrician"])

    def test_decision_makers_only_when_present(self):
        lead = _enrich(name="DM Electric", city="Denver",
                       decision_makers=[{"name": "Sample Owner", "title": "Owner", "source": "site"}])
        self.assertEqual(len(lead.decision_makers), 1)
        self.assertEqual(lead.decision_makers[0].name, "Sample Owner")

    def test_decision_maker_without_name_dropped(self):
        lead = _enrich(name="Anon Electric", decision_makers=[{"title": "Owner"}])
        self.assertEqual(lead.decision_makers, [])

    def test_completeness_and_provenance(self):
        full = _enrich(name="Full Electric", website="https://example.com/f", city="Denver",
                       categories=["electrical contractor"], phone="+1", employees=10,
                       decision_makers=[{"name": "Owner"}], source_url="https://example.com/f")
        self.assertEqual(full.data_completeness, 1.0)
        self.assertTrue(full.provenance_complete)

        sparse = _enrich(name="Sparse", source_url=None)
        self.assertLess(sparse.data_completeness, 1.0)
        self.assertFalse(sparse.provenance_complete)  # no source url

    def test_synthetic_flag_propagates(self):
        self.assertTrue(_enrich(name="X").is_synthetic)


if __name__ == "__main__":
    unittest.main()
