import tempfile
import unittest
from pathlib import Path

from leadintel.models import Query, Status
from leadintel.pipeline import build_leads, run
from leadintel.providers.fixture import FixtureProvider
from leadintel.providers.live import LiveProvider, LiveProviderNotEnabled

DATASET = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "synthetic_leads.json"
QUERY = Query(market="electrical contractors", location="Denver, CO")


def _provider():
    return FixtureProvider(fixture_path=DATASET)


class TestPipeline(unittest.TestCase):
    def test_build_leads_offline_sorted(self):
        leads = build_leads(QUERY, _provider())
        self.assertGreater(len(leads), 0)
        scores = [l.qualification_score for l in leads]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_all_required_fields_present(self):
        for lead in build_leads(QUERY, _provider()):
            d = lead.to_dict()
            for key in ("company", "website", "location", "service_type",
                        "estimated_opportunity", "decision_makers", "contact_channels",
                        "qualification_score", "score_breakdown", "score_contributions",
                        "category_verdict", "research_notes", "source", "status",
                        "data_completeness", "provenance_complete", "is_synthetic"):
                self.assertIn(key, d)
            self.assertIn(lead.status, list(Status))

    def test_handyman_not_qualified_end_to_end(self):
        leads = build_leads(QUERY, _provider())
        handyman = next(l for l in leads if "handyman" in l.company.lower())
        self.assertNotEqual(handyman.status, Status.QUALIFIED)

    def test_limit_respected(self):
        leads = build_leads(Query(market="electrical contractors", location="Denver, CO", limit=3),
                            _provider())
        self.assertLessEqual(len(leads), 3)

    def test_run_writes_files_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(QUERY, provider=_provider(), out_dir=tmp, run_id="t")
            for kind in ("jsonl", "json", "csv", "summary"):
                self.assertTrue(Path(result.files[kind]).exists())
            self.assertTrue(result.is_synthetic)
            self.assertEqual(sum(result.by_status.values()), result.total_leads)
            self.assertGreaterEqual(result.average_data_completeness, 0.0)

    def test_live_provider_is_gated(self):
        with self.assertRaises(LiveProviderNotEnabled):
            build_leads(QUERY, LiveProvider(enabled=False))

    def test_engine_is_provider_independent(self):
        """Same records via two provider instances yield identical qualification."""
        a = {l.id: l.qualification_score for l in build_leads(QUERY, _provider())}
        b = {l.id: l.qualification_score for l in build_leads(QUERY, _provider())}
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
