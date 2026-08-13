import tempfile
import unittest
from pathlib import Path

from leadintel.models import Query, Status
from leadintel.pipeline import build_leads, run
from leadintel.providers.fixture import FixtureProvider
from leadintel.providers.live import LiveProvider, LiveProviderNotEnabled

AUSTIN = Query(market="electrical contractors", location="Austin, TX")


class TestPipeline(unittest.TestCase):
    def test_build_leads_offline_returns_sorted_leads(self):
        leads = build_leads(AUSTIN, FixtureProvider())
        self.assertGreater(len(leads), 0)
        scores = [l.qualification_score for l in leads]
        self.assertEqual(scores, sorted(scores, reverse=True))  # sorted desc

    def test_location_filtering_excludes_other_markets(self):
        leads = build_leads(AUSTIN, FixtureProvider())
        names = " ".join(l.company for l in leads).lower()
        self.assertNotIn("bay area", names)  # San Jose, CA sample must be filtered out

    def test_all_required_fields_present(self):
        leads = build_leads(AUSTIN, FixtureProvider())
        for lead in leads:
            d = lead.to_dict()
            for key in (
                "company", "website", "location", "service_type",
                "estimated_opportunity", "decision_makers", "contact_channels",
                "qualification_score", "score_breakdown", "research_notes",
                "source", "status",
            ):
                self.assertIn(key, d)
            self.assertIn(lead.status, list(Status))

    def test_limit_is_respected(self):
        leads = build_leads(Query(market="electrical contractors",
                                  location="Austin, TX", limit=2), FixtureProvider())
        self.assertLessEqual(len(leads), 2)

    def test_run_writes_all_files_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(AUSTIN, provider=FixtureProvider(), out_dir=tmp, run_id="test-run")
            for kind in ("jsonl", "json", "csv", "summary"):
                self.assertIn(kind, result.files)
                self.assertTrue(Path(result.files[kind]).exists())
            self.assertEqual(sum(result.by_status.values()), result.total_leads)

    def test_live_provider_is_gated(self):
        with self.assertRaises(LiveProviderNotEnabled):
            build_leads(AUSTIN, LiveProvider(enabled=False))


if __name__ == "__main__":
    unittest.main()
