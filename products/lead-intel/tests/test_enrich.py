import unittest

from leadintel.enrich import enrich
from leadintel.models import Query
from leadintel.providers.base import RawBusiness

QUERY = Query(market="electrical contractors", location="Austin, TX")


class TestEnrich(unittest.TestCase):
    def test_missing_fields_are_none_not_fabricated(self):
        raw = RawBusiness(name="No Web Electric", city="Austin", region="TX")
        lead = enrich(raw, QUERY)
        self.assertIsNone(lead.website)
        self.assertIsNone(lead.contact_channels.phone)
        self.assertEqual(lead.decision_makers, [])
        self.assertIn("No website found", lead.research_notes)
        self.assertIn("No decision-maker", lead.research_notes)

    def test_decision_makers_only_when_present(self):
        raw = RawBusiness(
            name="DM Electric", city="Austin", region="TX",
            decision_makers=[{"name": "Sample Owner", "title": "Owner", "source": "site"}],
        )
        lead = enrich(raw, QUERY)
        self.assertEqual(len(lead.decision_makers), 1)
        self.assertEqual(lead.decision_makers[0].name, "Sample Owner")
        self.assertEqual(lead.decision_makers[0].title, "Owner")

    def test_decision_maker_without_name_is_dropped(self):
        raw = RawBusiness(
            name="Anon Electric", city="Austin", region="TX",
            decision_makers=[{"title": "Owner"}],  # no name -> not usable
        )
        lead = enrich(raw, QUERY)
        self.assertEqual(lead.decision_makers, [])

    def test_source_provenance_recorded(self):
        raw = RawBusiness(name="Prov Electric", source_url="https://example.com/x")
        lead = enrich(raw, QUERY)
        self.assertIsNotNone(lead.source)
        self.assertEqual(lead.source.url, "https://example.com/x")
        self.assertIsNotNone(lead.source.retrieved_at)


if __name__ == "__main__":
    unittest.main()
