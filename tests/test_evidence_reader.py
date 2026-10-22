"""Isolated evidence reader regression tests; no repository outputs modified."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.evidence_reader import read_json_evidence


class EvidenceReaderTests(unittest.TestCase):
    def test_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(read_json_evidence(Path(folder) / "missing.json"), ("missing", None))

    def test_invalid(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("{", encoding="utf-8")
            self.assertEqual(read_json_evidence(path), ("invalid", None))

    def test_present_object(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            path.write_text(json.dumps({"status": "NOT_VERIFIED"}), encoding="utf-8")
            self.assertEqual(read_json_evidence(path), ("present", {"status": "NOT_VERIFIED"}))

    def test_present_non_object_is_not_implicitly_approved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            path.write_text("[]", encoding="utf-8")
            self.assertEqual(read_json_evidence(path), ("present", []))


if __name__ == "__main__":
    unittest.main()
