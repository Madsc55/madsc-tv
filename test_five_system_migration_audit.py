"""Regression checks for the read-only five-workflow migration inventory."""
import tempfile
import unittest
from pathlib import Path
from scripts.five_system_migration_audit import inspect

class MigrationAuditTests(unittest.TestCase):
    def test_counts_and_detects_missing_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            w=root/".github"/"workflows"
            w.mkdir(parents=True)
            (w/"one.yml").write_text("name: Discovery\non:\n  schedule:\n    - cron: '0 6,18 * * *'\n  workflow_dispatch:\npermissions:\n  contents: write\njobs:\n  test:\n    steps:\n      - run: gh api repos/x/actions/workflows/missing.yml/dispatches\n")
            report=inspect(root)
            self.assertEqual(report["workflow_count"],1)
            self.assertEqual(report["scheduled_count"],1)
            self.assertEqual(report["manual_count"],1)
            self.assertEqual(report["write_permission_count"],1)
            self.assertEqual(report["unresolved_dispatch_targets"],[{"source":"one.yml","target":"missing.yml"}])
            self.assertFalse(report["migration_complete"])

    def test_five_files_without_parity_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            w = root / ".github" / "workflows"
            w.mkdir(parents=True)
            for i in range(5):
                (w / f"workflow-{i}.yml").write_text("name: Placeholder\non:\n  workflow_dispatch:\n")
            report = inspect(root)
            self.assertEqual(report["workflow_count"], 5)
            self.assertFalse(report["migration_complete"])

    def test_empty_repository_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            report=inspect(Path(d))
            self.assertEqual(report["workflow_count"],0)
            self.assertFalse(report["migration_complete"])

if __name__=="__main__":
    unittest.main()
