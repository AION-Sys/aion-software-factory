"""Tests for the DataAxleProvider adapter (MISSION-005 preparation).

All tests use an INJECTED MOCK transport — no network call is ever made, no
credential is real, and no data is acquired. These verify the gate/cap enforcement
that must hold before any live execution.
"""
import os
import unittest

from leadintel.models import Query, Status
from leadintel.pipeline import build_leads
from leadintel.providers.dataaxle import DataAxleGateError, DataAxleProvider

DENVER = Query(market="electrical contractors", location="Denver, CO")

# Mock Data Axle rows (clearly fabricated for tests; documented field shape).
MOCK_ROWS = [
    {
        "name": "Front Range Electrical Contractors",
        "website": "https://example.com/frec", "city": "Denver", "state": "CO",
        "naics": "238210", "naics_description": "Electrical Contractors",
        "phone": "+1-303-555-0180", "email": "info@example.com", "employees": 45,
        "primary_contact_first_name": "Pat", "primary_contact_last_name": "Sample",
        "primary_contact_job_title": "Owner", "source_url": "https://example.com/frec-rec",
    },
    {
        "name": "Denver Handyman Services",
        "website": "https://example.com/dhs", "city": "Denver", "state": "CO",
        "naics": "811490", "naics_description": "Handyman / home repair",
        "phone": "+1-303-555-0181", "employees": 3,
    },
]


def _mock_transport(rows):
    return lambda request: list(rows)


def _armed(**over):
    """A fully-armed provider for cap/parse tests (mock transport, fake env key)."""
    kwargs = dict(enabled=True, cost_per_record_usd=0.05, transport=_mock_transport(MOCK_ROWS))
    kwargs.update(over)
    return DataAxleProvider(**kwargs)


class TestDataAxleGates(unittest.TestCase):
    def setUp(self):
        os.environ["DATA_AXLE_API_KEY"] = "test-not-a-real-key"

    def tearDown(self):
        os.environ.pop("DATA_AXLE_API_KEY", None)

    def test_disabled_by_default(self):
        with self.assertRaises(DataAxleGateError):
            DataAxleProvider().search(DENVER)  # enabled defaults False

    def test_requires_credential(self):
        os.environ.pop("DATA_AXLE_API_KEY", None)
        with self.assertRaises(DataAxleGateError):
            _armed().search(DENVER)

    def test_requires_verified_cost_per_record(self):
        p = DataAxleProvider(enabled=True, cost_per_record_usd=None,
                             transport=_mock_transport(MOCK_ROWS))
        with self.assertRaises(DataAxleGateError):
            p.search(DENVER)

    def test_market_guard_blocks_other_markets(self):
        with self.assertRaises(DataAxleGateError):
            _armed().search(Query(market="electrical contractors", location="Austin, TX"))

    def test_market_guard_rejects_substring_lookalikes(self):
        # Whole-token city AND state required — no substring false positives.
        for bad in ("Aurora, IL", "Colorado Springs, CO", "Concord, CA",
                    "Denver, PA", "Lakewood, NJ", "Denver"):
            with self.assertRaises(DataAxleGateError, msg=bad):
                _armed().search(Query(market="electrical contractors", location=bad))

    def test_market_guard_allows_approved_metro(self):
        for good in ("Denver, CO", "Aurora, CO", "Lakewood, CO", "Denver, Colorado"):
            # Should not raise on the market check (mock transport returns rows).
            self.assertTrue(
                _armed().search(Query(market="electrical contractors", location=good))
            )

    def test_volume_cap_enforced(self):
        many = [dict(MOCK_ROWS[0], name=f"EC {i}") for i in range(1000)]
        p = _armed(max_records=500, transport=_mock_transport(many))
        results = p.search(Query(market="electrical contractors", location="Denver, CO", limit=1000))
        self.assertLessEqual(len(results), 500)

    def test_spend_cap_clamps_records(self):
        # $100 cap at $0.30/record -> at most 333 records, even if 500 requested.
        many = [dict(MOCK_ROWS[0], name=f"EC {i}") for i in range(500)]
        p = _armed(cost_per_record_usd=0.30, spend_cap_usd=100.0,
                   max_records=500, transport=_mock_transport(many))
        results = p.search(DENVER)
        self.assertLessEqual(len(results), 333)

    def test_spend_cap_too_low_raises(self):
        p = _armed(cost_per_record_usd=1000.0, spend_cap_usd=100.0)
        with self.assertRaises(DataAxleGateError):
            p.search(DENVER)

    def test_live_transport_not_implemented(self):
        # No injected transport + enabled -> the real transport must refuse.
        p = DataAxleProvider(enabled=True, cost_per_record_usd=0.05)
        with self.assertRaises(NotImplementedError):
            p.search(DENVER)


class TestDataAxleParsing(unittest.TestCase):
    def setUp(self):
        os.environ["DATA_AXLE_API_KEY"] = "test-not-a-real-key"

    def tearDown(self):
        os.environ.pop("DATA_AXLE_API_KEY", None)

    def test_parse_maps_fields_and_decision_maker(self):
        raw = DataAxleProvider.parse_record(MOCK_ROWS[0])
        self.assertEqual(raw.name, "Front Range Electrical Contractors")
        self.assertIn("electrical contractor", raw.categories)
        self.assertEqual(raw.phone, "+1-303-555-0180")
        self.assertEqual(len(raw.decision_makers), 1)
        self.assertEqual(raw.decision_makers[0]["name"], "Pat Sample")

    def test_end_to_end_through_existing_engine(self):
        leads = build_leads(DENVER, _armed())
        by_name = {l.company: l for l in leads}
        ec = by_name["Front Range Electrical Contractors"]
        self.assertEqual(ec.status, Status.QUALIFIED)
        self.assertFalse(ec.is_synthetic)  # real provider -> NOT synthetic
        handy = by_name["Denver Handyman Services"]
        self.assertNotEqual(handy.status, Status.QUALIFIED)  # gate holds on real path


if __name__ == "__main__":
    unittest.main()
