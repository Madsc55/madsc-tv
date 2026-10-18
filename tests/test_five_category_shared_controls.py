"""Cross-category shared control regression checks."""
import tempfile
import unittest
from pathlib import Path
from scripts.five_category_shared_controls import CATEGORIES, inspect

class SharedControlsTests(unittest.TestCase):
    def test_shared_control_references_across_five_categories(self):
        report = inspect()
        self.assertEqual(set(report["shared_controls"]["protected_integrity"]["consumers"]), set(CATEGORIES))
        self.assertEqual(report["status"], "STATIC_READY", report["missing_consumers"])

    def test_comments_do_not_count_as_executed_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                (folder / name).write_text("# scripts/k1_protected_integrity.py\\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["status"], "BLOCKED")
            self.assertFalse(report["shared_controls"]["protected_integrity"]["all_consumers_present"])

    def test_missing_consumer_blocks_all_category_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                (folder / name).write_text("name: placeholder\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["status"], "BLOCKED")
            self.assertEqual(len(report["shared_controls"]["protected_integrity"]["consumers"]), 5)
            self.assertTrue(report["missing_consumers"])

if __name__ == "__main__":
    unittest.main()
