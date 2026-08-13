import csv
import json
import tempfile
import unittest
from pathlib import Path

from leadintel.models import Query
from leadintel.output import CSV_COLUMNS, write_csv, write_json, write_jsonl
from leadintel.pipeline import build_leads
from leadintel.providers.fixture import FixtureProvider

LEADS = build_leads(Query(market="electrical contractors", location="Austin, TX"),
                    FixtureProvider())


class TestOutput(unittest.TestCase):
    def test_csv_has_required_columns_and_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_csv(LEADS, Path(tmp) / "leads.csv")
            with open(path, encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), len(LEADS))
            self.assertEqual(list(rows[0].keys()), CSV_COLUMNS)

    def test_json_is_valid_and_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_json(LEADS, Path(tmp) / "leads.json")
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            self.assertEqual(len(data), len(LEADS))
            self.assertIn("qualification_score", data[0])

    def test_jsonl_line_count_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_jsonl(LEADS, Path(tmp) / "leads.jsonl")
            lines = [l for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
            self.assertEqual(len(lines), len(LEADS))
            json.loads(lines[0])  # each line is valid JSON

    def test_missing_website_renders_empty_not_none_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_csv(LEADS, Path(tmp) / "leads.csv")
            with open(path, encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            for row in rows:
                self.assertNotIn("None", (row["website"], row["phone"], row["email"]))


if __name__ == "__main__":
    unittest.main()
