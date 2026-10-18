"""Regression: unspecified legacy permissions must block migration parity."""
import tempfile
import unittest
from pathlib import Path
from scripts.five_category_92_workflow_audit import inspect


class LegacyPermissionGapTests(unittest.TestCase):
    def test_inherited_permissions_are_reported_as_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for i in range(92):
                (folder / f"legacy-{i:02}.yml").write_text(
                    "name: legacy\\non:\\n  workflow_dispatch:\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - run: echo ok\\n",
                    encoding="utf-8",
                )
            report = inspect(Path(tmp))
            self.assertEqual(report["total"], 92)
            self.assertEqual(report["behavioral_parity_verified_count"], 0)
            self.assertTrue(all(
                "INHERITED_PERMISSION_REQUIRES_REVIEW" in row["migration_gap_reasons"]
                for row in report["items"]
            ))


if __name__ == "__main__":
    unittest.main()
