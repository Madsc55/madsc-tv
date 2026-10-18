"""Regression: unspecified legacy permissions must block migration parity."""
import tempfile
import unittest
from pathlib import Path
from scripts.five_category_92_workflow_audit import inspect


class LegacyPermissionGapTests(unittest.TestCase):
    def test_explicit_read_permission_does_not_raise_inherited_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for i in range(92):
                (folder / f"legacy-{i:02}.yml").write_text(
                    "name: legacy\non:\n  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n",
                    encoding="utf-8",
                )
            report = inspect(Path(tmp))
            self.assertTrue(all(
                "INHERITED_PERMISSION_REQUIRES_REVIEW" not in row["migration_gap_reasons"]
                for row in report["items"]
            ))
            self.assertEqual(report["behavioral_parity_verified_count"], 0)

    def test_job_write_override_is_flagged_even_with_workflow_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for i in range(92):
                (folder / f"legacy-{i:02}.yml").write_text(
                    "name: legacy\non:\n  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  writer:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: write\n    steps:\n      - run: echo ok\n", encoding="utf-8",
                )
            report = inspect(Path(tmp))
            self.assertTrue(all(row["contents_write"] for row in report["items"]))
            self.assertTrue(all(
                "MIXED_READ_WRITE_PERMISSION_REQUIRES_REVIEW" in row["migration_gap_reasons"]
                for row in report["items"]
            ))
            self.assertEqual(report["behavioral_parity_verified_count"], 0)

    def test_missing_legacy_workflow_blocks_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for i in range(91):
                (folder / f"legacy-{i:02}.yml").write_text(
                    "name: legacy\non:\n  workflow_dispatch:\npermissions:\n  contents: read\njobs: {}\n", encoding="utf-8",
                )
            with self.assertRaisesRegex(SystemExit, "expected 92, found 91"):
                inspect(Path(tmp))

    def test_inherited_permissions_are_reported_as_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for i in range(92):
                (folder / f"legacy-{i:02}.yml").write_text(
                    "name: legacy\non:\n  workflow_dispatch:\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n",
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
