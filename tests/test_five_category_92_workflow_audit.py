"""Behavioral regression for central cron extraction; never edits project files."""
import tempfile
import unittest
from pathlib import Path

from scripts.five_category_92_workflow_audit import inspect


class CentralCronRegressionTests(unittest.TestCase):
    def test_write_side_effects_without_explicit_permissions_are_reviewed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-api-push.yml").write_text(
                "name: API push\non:\n  push:\njobs:\n  write:\n    steps:\n"
                "      - run: |\n          git push origin HEAD:main\n"
                "          gh api repos/owner/repo/actions/workflows/test.yml/dispatches -X POST\n",
                encoding="utf-8",
            )
            for number in range(91):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            item = next(x for x in report["items"] if x["file"] == "legacy-api-push.yml")
            self.assertTrue(item["write_permission_parity_unverified"])
            self.assertTrue(item["write_permission_inherited_or_unknown"])
            self.assertEqual(item["review_priority"], "HIGH")
            self.assertIn("WRITE_SIDE_EFFECTS_UNVERIFIED", item["migration_gap_reasons"])
            self.assertIn("VERIFY_API_DISPATCH_TARGET_AND_IDEMPOTENCY", item["required_acceptance_checks"])

    def test_protected_favorites_write_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-favorites.yml").write_text(
                "name: Favorites\non:\n  workflow_dispatch:\njobs:\n  write:\n"
                "    steps:\n      - run: echo FAVORILER && git push origin HEAD:main\n",
                encoding="utf-8",
            )
            for number in range(91):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            item = next(x for x in inspect(root)["items"] if x["file"] == "legacy-favorites.yml")
            self.assertTrue(item["requires_protected_write_review"])

    def test_api_only_write_is_in_risk_queue(self):
        # A workflow may dispatch or mutate through gh api without git push.
        import json
        from unittest.mock import patch
        from scripts.five_category_92_workflow_audit import main
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "legacy-api-only.yml").write_text(
                "name: API only\non:\n  workflow_dispatch:\njobs:\n  api:\n    steps:\n"
                "      - run: gh api repos/o/r/actions/workflows/other.yml/dispatches -X POST\n",
                encoding="utf-8",
            )
            for number in range(91):
                (folder / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            from scripts import five_category_92_workflow_audit as audit
            original_inspect = audit.inspect
            with patch.object(audit, "ROOT", root), patch.object(audit, "inspect", side_effect=lambda: original_inspect(root)):
                main()
            import csv
            with (root / "madsc_merkezi_denetim" / "92_workflow_esdegerlik_kabul_matrisi.csv").open(newline="", encoding="utf-8") as stream:
                csv_rows = list(csv.DictReader(stream))
            self.assertEqual(len(csv_rows), 92)
            self.assertIn("write_permission_inherited_or_unknown", csv_rows[0])
            self.assertEqual(next(row for row in csv_rows if row["legacy_workflow"] == "legacy-api-only.yml")["write_permission_inherited_or_unknown"], "True")
            queue = json.loads((root / "madsc_merkezi_denetim" / "92_workflow_yazma_risk_inceleme_kuyrugu.json").read_text())
            self.assertIn("legacy-api-only.yml", [item["file"] for item in queue["items"]])
            api_entry = next(item for item in queue["items"] if item["file"] == "legacy-api-only.yml")
            self.assertTrue(any("gh api" in cmd for cmd in api_entry["write_risk_commands"]))
            self.assertEqual(api_entry["review_priority"], "HIGH")
            self.assertIn("VERIFY_API_DISPATCH_TARGET_AND_IDEMPOTENCY", api_entry["required_acceptance_checks"])
            self.assertFalse(api_entry["requires_protected_write_review"])
            self.assertEqual(queue["total_review_items"], len(queue["items"]))

    def test_protected_playlist_write_requires_manual_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-protected.yml").write_text(
                "name: Protected\non:\n  workflow_dispatch:\njobs:\n  save:\n    steps:\n"
                "      - run: git add CALISANLAR.m3u && git push origin HEAD:main\n",
                encoding="utf-8",
            )
            for number in range(91):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            item = next(x for x in report["items"] if x["file"] == "legacy-protected.yml")
            self.assertTrue(item["requires_protected_write_review"])
            self.assertEqual(report["protected_write_review_count"], 1)
            self.assertIn("VERIFY_WRITE_AUTHORIZATION_AND_ROLLBACK", item["required_acceptance_checks"])

    def test_protected_write_review_is_scoped_to_each_workflow(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-00-protected.yml").write_text(
                "name: Protected first\non:\n  workflow_dispatch:\njobs:\n  save:\n    steps:\n"
                "      - run: git add CALISANLAR.m3u && git push origin HEAD:main\n",
                encoding="utf-8",
            )
            (workflows / "legacy-01-ordinary-write.yml").write_text(
                "name: Ordinary write\non:\n  workflow_dispatch:\njobs:\n  save:\n    steps:\n"
                "      - run: git push origin HEAD:review\n",
                encoding="utf-8",
            )
            for number in range(90):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            items = {item["file"]: item for item in report["items"]}
            self.assertTrue(items["legacy-00-protected.yml"]["requires_protected_write_review"])
            self.assertFalse(items["legacy-01-ordinary-write.yml"]["requires_protected_write_review"])
            self.assertEqual(report["protected_write_review_count"], 1)

    def test_api_dispatch_without_git_push_is_reviewed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-dispatch.yml").write_text(
                "name: Dispatch\non:\n  workflow_dispatch:\njobs:\n  dispatch:\n    steps:\n"
                "      - run: gh api repos/owner/repo/actions/workflows/next.yml/dispatches -X POST\n",
                encoding="utf-8",
            )
            for number in range(91):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            item = next(x for x in report["items"] if x["file"] == "legacy-dispatch.yml")
            self.assertEqual(item["git_push_command_count"], 0)
            self.assertTrue(item["write_permission_parity_unverified"])
            self.assertIn("WRITE_SIDE_EFFECTS_UNVERIFIED", item["migration_gap_reasons"])
            self.assertEqual(report["api_write_or_dispatch_review_count"], 1)

    def test_central_stages_stop_after_failed_dependency(self):
        """Stages 2-4 must not bypass a failed upstream security gate."""
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/madsc-05-genel-bakim.yml").read_text(encoding="utf-8")
        import re
        for stage, predecessor, called in (
            ("kademe-2-kesif", "kademe-1-guvenlik", "madsc-02-kesif.yml"),
            ("kademe-3-kanal-test", "kademe-2-kesif", "madsc-03-kanal-test.yml"),
            ("kademe-4-arsiv-yedek", "kademe-3-kanal-test", "madsc-04-arsiv-yedek.yml"),
        ):
            match = re.search(r"^  " + re.escape(stage) + r":\n(?P<body>.*?)(?=^  [a-z][\w-]*:|\Z)", workflow, re.M | re.S)
            self.assertIsNotNone(match, stage)
            body = match.group("body")
            self.assertIn("needs: " + predecessor, body)
            self.assertIn("needs." + predecessor + ".result != 'cancelled'", body)
            self.assertIn("always()", body)
            self.assertIn("uses: ./.github/workflows/" + called, body)

    def test_central_discovery_cadence_and_daily_health_rotation(self):
        root = Path(__file__).resolve().parents[1]
        discovery = (root / ".github/workflows/madsc-02-kesif.yml").read_text(encoding="utf-8")
        health = (root / ".github/workflows/madsc-03-kanal-test.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '17 5,17 * * *'", discovery)
        self.assertIn("cron: '0 6,18 * * *'", discovery)
        self.assertIn("python3 scripts/candidate_epg_logo_join.py", discovery)
        self.assertLess(discovery.index("python3 scripts/discovery_archive.py after"), discovery.index("python3 scripts/candidate_epg_logo_join.py"))
        self.assertLess(discovery.index("python3 scripts/candidate_epg_logo_join.py"), discovery.index("python3 scripts/four_stage_discovery_report.py"))
        # The new read-only daily rolling check is deliberately NOT proof of
        # legacy twice-monthly behavior equivalence; keep parity blocked.
        self.assertIn("cron: '40 6 * * *'", health)
        self.assertIn("ana_liste_saglik.py --batch-size 50 --timeout 15", health)
        self.assertIn("workflow_call:", discovery)
        self.assertIn("workflow_call:", health)
        self.assertIn("contents: read", discovery)
        self.assertIn("contents: read", health)

    def test_daily_health_rotation_covers_every_batch_without_repeats(self):
        from datetime import date, timedelta
        from scripts.ana_liste_saglik import batch

        rows = list(range(123))
        start = date(2026, 10, 18)
        selected_all = []
        groups_seen = []
        for offset in range(3):
            selected, group, total_groups = batch(rows, start + timedelta(days=offset), 50)
            self.assertEqual(total_groups, 3)
            groups_seen.append(group)
            selected_all.extend(selected)
        self.assertCountEqual(selected_all, rows)
        self.assertEqual(len(selected_all), len(rows))
        self.assertEqual(len(set(groups_seen)), 3)
        self.assertEqual(batch(rows, start, 50)[1], batch(rows, start + timedelta(days=3), 50)[1])

    def test_shadow_crons_do_not_count_as_verified_behavior(self):
        root = Path(__file__).resolve().parents[1]
        discovery = (root / ".github/workflows/madsc-02-kesif.yml").read_text(encoding="utf-8")
        health = (root / ".github/workflows/madsc-03-kanal-test.yml").read_text(encoding="utf-8")
        self.assertIn("madsc_akilli_kesif.py", discovery)
        self.assertIn("ana_liste_saglik.py --batch-size 50 --timeout 15", health)
        self.assertIn("contents: read", discovery)
        self.assertIn("contents: read", health)
        report = inspect(root)
        self.assertEqual(report["total"], 92)
        self.assertEqual(report["behavioral_parity_verified_count"], 0)
        self.assertEqual(report["migration_blocked_count"], 92)
        self.assertTrue(all(not item["behavioral_parity_verified"] for item in report["items"]))

    def test_exact_schedule_match_and_unmatched_schedule(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-matched.yml").write_text(
                "name: Matched\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs:\n  check:\n    steps:\n      - run: python3 scripts/cron_shared.py\n",
                encoding="utf-8",
            )
            (workflows / "legacy-unmatched.yml").write_text(
                'name: Unmatched\non:\n  schedule:\n    - cron: "30 7 * * 1"\njobs: {}\n',
                encoding="utf-8",
            )
            (workflows / "madsc-05-genel-bakim.yml").write_text(
                "name: Central\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs: {}\n",
                encoding="utf-8",
            )
            # Cron coverage requires a shared script linking legacy and central jobs.
            (workflows / "madsc-02-kesif.yml").write_text(
                "name: Discovery\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs:\n  check:\n    steps:\n      - run: python3 scripts/cron_shared.py\n",
                encoding="utf-8",
            )
            # The inventory enforces 92 legacy workflows, including in fixtures.
            for number in range(90):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            items = {row["file"]: row for row in report["items"]}
            self.assertEqual(report["total"], 92)
            self.assertIn("madsc-02-kesif.yml", items["legacy-matched.yml"]["possible_replacement_workflows"])
            self.assertEqual(items["legacy-matched.yml"]["unmatched_cron_expressions"], [])
            self.assertEqual(
                items["legacy-unmatched.yml"]["unmatched_cron_expressions"],
                ["30 7 * * 1"],
            )
            self.assertFalse(items["legacy-matched.yml"]["behavioral_parity_verified"])
            self.assertFalse(items["legacy-unmatched.yml"]["behavioral_parity_verified"])


    def test_gh_cli_dispatch_enable_disable_rerun_require_review(self):
        commands = ("gh workflow run next.yml --ref main",
                    "gh workflow enable next.yml",
                    "gh workflow disable next.yml",
                    "gh run rerun 12345")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "legacy-gh-cli.yml").write_text(
                "name: CLI\non:\n  workflow_dispatch:\njobs:\n  dispatch:\n    steps:\n"
                "      - run: |\n" + "".join(f"          {cmd}\n" for cmd in commands),
                encoding="utf-8",
            )
            for i in range(91):
                (folder / f"legacy-filler-{i:02d}.yml").write_text(
                    f"name: Filler {i}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            item = next(x for x in inspect(root)["items"] if x["file"] == "legacy-gh-cli.yml")
            self.assertEqual(item["git_push_command_count"], 0)
            self.assertEqual(len(item["write_risk_commands"]), len(commands))
            self.assertEqual(item["review_priority"], "HIGH")
            self.assertTrue(item["write_permission_parity_unverified"])
            self.assertIn("VERIFY_API_DISPATCH_TARGET_AND_IDEMPOTENCY", item["required_acceptance_checks"])
            self.assertFalse(item["behavioral_parity_verified"])

    def test_protected_legacy_outputs_are_flagged(self):
        names = ("CALISMAYANLAR.txt", "YABANCI_KANALLAR.m3u", "epg.xml")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for i, name in enumerate(names):
                (folder / f"legacy-protected-{i}.yml").write_text(
                    f"name: Protected {i}\non:\n  workflow_dispatch:\njobs:\n  write:\n"
                    f"    steps:\n      - run: git add {name} && git push origin HEAD:main\n",
                    encoding="utf-8",
                )
            for i in range(92 - len(names)):
                (folder / f"legacy-filler-{i:02d}.yml").write_text(
                    f"name: Filler {i}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            self.assertEqual(report["protected_write_review_count"], len(names))
            self.assertEqual(report["behavioral_parity_verified_count"], 0)

if __name__ == "__main__":
    unittest.main()
