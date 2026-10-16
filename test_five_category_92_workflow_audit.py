"""Bulk coverage audit regression: 92 old workflows, five new categories."""
import csv
import tempfile
import unittest
from pathlib import Path
from scripts.five_category_92_workflow_audit import inspect, main


class BulkCoverageTests(unittest.TestCase):
    def test_92_legacy_workflows_all_reported_and_gaps_visible(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for n in range(92):
                script = "scripts/shared.py" if n < 50 else "scripts/missing.py"
                (folder / f"legacy-{n:02d}.yml").write_text(
                    f"name: Legacy {n}\non:\n  workflow_dispatch:\njobs:\n  audit:\n    steps:\n      - run: python3 {script}\n")
            for n, name in enumerate(("guvenlik", "kesif", "kanal-test", "arsiv-yedek", "genel-bakim"), 1):
                (folder / f"madsc-0{n}-{name}.yml").write_text(
                    "name: New category\non:\n  workflow_dispatch:\njobs:\n  audit:\n    steps:\n      - run: python3 scripts/shared.py\n")
            result = inspect(root)
            self.assertEqual(result["total"], 92)
            self.assertEqual(result["legacy_workflows_with_unmatched_scripts"], 42)
            self.assertEqual(result["legacy_workflows_with_no_shared_script"], 42)
            self.assertEqual(result["behavioral_parity_verified_count"], 0)
            self.assertEqual(result["integration_evidence_counts"]["SCRIPT_NAMES_MATCH_ONLY"], 50)
            self.assertEqual(result["integration_evidence_counts"]["PARTIAL_OR_MISSING_SCRIPT_COVERAGE"], 42)
            self.assertEqual(result["migration_gap_reason_counts"]["BEHAVIORAL_EQUIVALENCE_NOT_PROVEN"], 92)
            self.assertEqual(result["migration_gap_reason_counts"]["UNMATCHED_SCRIPT_ENTRYPOINTS"], 42)
            self.assertEqual(sum(result["integration_evidence_counts"].values()), 92)
            self.assertEqual(result["migration_blocked_count"], 92)
            self.assertTrue(all("trigger_coverage_signals" in x for x in result["items"]))
            self.assertTrue(all("unmatched_trigger_signals" in x for x in result["items"]))
            self.assertEqual(len(result["items"]), 92)
            self.assertTrue(all(not x["behavioral_parity_verified"] for x in result["items"]))

    def test_review_rows_remain_blocked_without_behavior_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for n in range(92):
                (folder / f"legacy-{n:02d}.yml").write_text(
                    "name: Legacy\non:\n  workflow_dispatch:\njobs:\n  test:\n    steps:\n      - run: python3 scripts/legacy.py\n")
            for n, name in enumerate(("guvenlik", "kesif", "kanal-test", "arsiv-yedek", "genel-bakim"), 1):
                (folder / f"madsc-0{n}-{name}.yml").write_text(
                    "name: New\njobs:\n  test:\n    steps:\n      - run: python3 scripts/legacy.py\n")
            result = inspect(Path(d))
            self.assertEqual(result["migration_blocked_count"], 92)
            self.assertTrue(all(x["migration_decision"] == "BLOCKED_NEEDS_BEHAVIOR_EVIDENCE" for x in result["items"]))
            self.assertTrue(all(x["possible_replacement_workflows"] for x in result["items"]))
            self.assertTrue(all(not x["behavioral_parity_verified"] for x in result["items"]))

    def test_missing_script_files_are_reported_without_authorizing_migration(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "present.py").write_text("print('ok')\n")
            for n in range(92):
                script = "scripts/present.py" if n < 60 else "scripts/absent.py"
                (folder / f"legacy-{n:02d}.yml").write_text(
                    f"name: Legacy\non:\n  workflow_dispatch:\njobs:\n  check:\n    steps:\n      - run: python3 {script}\n")
            for n, name in enumerate(("guvenlik", "kesif", "kanal-test", "arsiv-yedek", "genel-bakim"), 1):
                (folder / f"madsc-0{n}-{name}.yml").write_text(
                    "name: New\njobs:\n  check:\n    steps:\n      - run: python3 scripts/present.py\n")
            result = inspect(root)
            self.assertEqual(result["legacy_workflows_with_missing_script_file"], 32)
            self.assertEqual(result["migration_gap_reason_counts"]["MISSING_LEGACY_SCRIPT_FILE"], 32)
            self.assertEqual(result["migration_blocked_count"], 92)

    def test_inline_only_workflows_are_not_falsely_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for n in range(92):
                (folder / f"legacy-{n:02d}.yml").write_text(
                    "name: Legacy\\non:\\n  workflow_dispatch:\\njobs:\\n  inline:\\n    steps:\\n      - run: echo inline-only\\n"
                )
            for n, name in enumerate(("guvenlik", "kesif", "kanal-test", "arsiv-yedek", "genel-bakim"), 1):
                (folder / f"madsc-0{n}-{name}.yml").write_text("name: New\\njobs: {}\\n")
            report = inspect(root)
            self.assertEqual(report["integration_evidence_counts"]["NO_EXTRACTED_SCRIPT_REVIEW_INLINE_ACTIONS"], 92)
            self.assertEqual(report["migration_gap_reason_counts"]["INLINE_OR_ACTION_BEHAVIOR_UNREVIEWED"], 92)
            self.assertEqual(report["migration_blocked_count"], 92)

    def test_new_k1_ci_does_not_inflate_legacy_inventory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for n in range(92):
                (folder / f"legacy-{n:02d}.yml").write_text("name: Legacy\\n")
            (folder / "k1-protected-write-tests.yml").write_text("name: New K1 CI\\n")
            report = inspect(root)
            self.assertEqual(report["total"], 92)
            self.assertNotIn("k1-protected-write-tests.yml", [x["file"] for x in report["items"]])

    def test_push_risk_signals_are_recorded_without_claiming_parity(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for n in range(92):
                command = ("git -c user.name=bot push --force origin HEAD" if n == 0
                           else "git push origin HEAD && git push origin HEAD" if n == 1
                           else "echo no-push")
                (folder / f"legacy-{n:02d}.yml").write_text(
                    "name: Legacy\\non:\\n  workflow_dispatch:\\njobs:\\n  check:\\n"
                    f"    steps:\\n      - run: {command}\\n")
            report = inspect(root)
            by_name = {row["file"]: row for row in report["items"]}
            self.assertEqual(by_name["legacy-00.yml"]["force_push_command_count"], 1)
            self.assertEqual(by_name["legacy-01.yml"]["git_push_command_count"], 2)
            self.assertTrue(by_name["legacy-01.yml"]["multiple_push_command_signal"])
            self.assertIn("MULTIPLE_PUSH_COMMANDS_REVIEW", by_name["legacy-01.yml"]["migration_gap_reasons"])
            self.assertIn("FORCE_PUSH_COMMAND_REVIEW", by_name["legacy-00.yml"]["migration_gap_reasons"])
            self.assertEqual(report["migration_blocked_count"], 92)

    def test_missing_legacy_workflow_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d) / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "legacy.yml").write_text("name: Legacy\n")
            with self.assertRaises(SystemExit):
                inspect(Path(d))


if __name__ == "__main__":
    unittest.main()
