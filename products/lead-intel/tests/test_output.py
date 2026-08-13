import csv
import json
import tempfile
import unittest
from pathlib import Path

from leadintel.models import Query
from leadintel.output import CSV_COLUMNS, write_csv, write_json, write_jsonl
from leadintel.pipeline import build_leads
from leadintel.providers.fixture import FixtureProvider

DATASET = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "synthetic_leads.json"
LEADS = build_leads(Query(market="electrical contractors", location="Denver, CO"),
                    FixtureProvider(fixture_path=DATASET))


class TestOutput(unittest.TestCase):
    def test_csv_columns_and_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_csv(LEADS, Path(tmp) / "leads.csv")
            with open(path, encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), len(LEADS))
            self.assertEqual(list(rows[0].keys()), CSV_COLUMNS)

    def test_csv_marks_synthetic_and_explains_why(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_csv(LEADS, Path(tmp) / "leads.csv")
            with open(path, encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            for row in rows:
                self.assertEqual(row["synthetic"], "yes")
                self.assertTrue(row["why"], "expected an explanation in 'why'")
                self.assertIn(row["category_verdict"],
                              ("ELECTRICAL", "ADJACENT", "NON_ELECTRICAL", "AMBIGUOUS"))

    def test_json_shape_has_disclaimer_and_leads(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_json(LEADS, Path(tmp) / "leads.json")
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            self.assertIn("_disclaimer", data)
            self.assertIn("SYNTHETIC", data["_disclaimer"])
            self.assertEqual(data["count"], len(LEADS))
            self.assertIn("qualification_score", data["leads"][0])
            self.assertIn("score_contributions", data["leads"][0])

    def test_jsonl_lines_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_jsonl(LEADS, Path(tmp) / "leads.jsonl")
            lines = [l for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
            self.assertEqual(len(lines), len(LEADS))
            json.loads(lines[0])

    def test_missing_values_render_empty_not_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_csv(LEADS, Path(tmp) / "leads.csv")
            with open(path, encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            for row in rows:
                self.assertNotIn("None", (row["website"], row["phone"], row["email"]))


if __name__ == "__main__":
    unittest.main()
