"""Regression tests for read-only workflow push risk inventory."""
import tempfile
import unittest
from pathlib import Path
from scripts.k1_workflow_risk_inventory import inspect

class WorkflowRiskInventoryTests(unittest.TestCase):
    def inspect_text(self, content):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root / ".github" / "workflows") as tmp:
            p = Path(tmp) / "fixture.yml"
            p.write_text(content, encoding="utf-8")
            return inspect(p)

    def test_force_push_with_git_config_is_detected(self):
        record = self.inspect_text("steps:\n  - run: git -c user.name=bot push --force origin HEAD\n")
        self.assertEqual(record["git_push_count"], 1)
        self.assertEqual(record["force_push_count"], 1)
        self.assertEqual(record["tier"], "CRITICAL_UNGATED_PUSH")

    def test_two_push_commands_flagged(self):
        record = self.inspect_text("steps:\n  - run: git push origin HEAD\n  - run: git push origin HEAD\n")
        self.assertEqual(record["git_push_count"], 2)
        self.assertTrue(record["multiple_push_signal"])

    def test_actions_api_get_reports_are_read_only(self):
        for command in (
            'gh api "repos/${GITHUB_REPOSITORY}/actions/runs?per_page=100" --jq ".workflow_runs"',
            'gh api --paginate "repos/${GITHUB_REPOSITORY}/actions/workflows?per_page=100" --jq ".workflows"',
        ):
            with self.subTest(command=command):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n  - run: " + command + "\n"
                    + "  - run: cat CALISANLAR.m3u\n"
                )
                self.assertFalse(record["write_command_signal"])
                self.assertEqual(record["tier"], "LOW_STATIC_SIGNAL")

    def test_actions_api_mutations_remain_write_signals(self):
        commands = (
            'gh api -X POST "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api --method PATCH "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api -f value=1 "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api --input payload.json "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api graphql -f query=mutation',
            'gh api repos/${GITHUB_REPOSITORY}/dispatches',
        )
        for command in commands:
            with self.subTest(command=command):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n  - run: " + command + "\n"
                    + "  - run: cat CALISANLAR.m3u\n"
                )
                self.assertTrue(record["write_command_signal"])
                self.assertEqual(record["tier"], "HIGH_WRITE_OR_TRIGGER")

    def test_read_only_workflow_not_flagged(self):
        record = self.inspect_text("permissions:\n  contents: read\nsteps:\n  - run: echo safe\n")
        self.assertEqual(record["git_push_count"], 0)
        self.assertEqual(record["force_push_count"], 0)
        self.assertFalse(record["multiple_push_signal"])

    def test_gh_cli_mutations_are_write_signals(self):
        for command in ("gh workflow run next.yml --ref main",
                        "gh workflow enable next.yml",
                        "gh workflow disable next.yml",
                        "gh run rerun 12345"):
            with self.subTest(command=command):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n  - run: " + command
                    + "\n  - run: cat CALISANLAR.m3u\n"
                )
                self.assertTrue(record["write_command_signal"])
                self.assertEqual(record["tier"], "HIGH_WRITE_OR_TRIGGER")

    def test_gh_cli_read_only_commands_remain_read_only(self):
        for command in ("gh workflow list", "gh run list", "gh workflow view next.yml"):
            with self.subTest(command=command):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n  - run: " + command + "\n"
                )
                self.assertFalse(record["write_command_signal"])
                self.assertEqual(record["tier"], "LOW_STATIC_SIGNAL")

    def test_indirect_writer_and_additional_cli_mutations_are_flagged(self):
        commands = ("python3 scripts/publish_channels.py", "bash tools/deploy.sh",
                    "gh release upload v1 artifact.zip", "gh pr merge 71",
                    "git reset --hard HEAD", "git clean -fd")
        for command in commands:
            with self.subTest(command=command):
                record = self.inspect_text("permissions:\n  contents: read\nsteps:\n  - run: " + command
                                           + "\n  - run: cat CALISANLAR.m3u\n")
                self.assertTrue(record["write_command_signal"], command)
                self.assertEqual(record["tier"], "HIGH_WRITE_OR_TRIGGER")

    def test_indirect_writer_without_gate_is_reported_not_runtime_verified(self):
        record = self.inspect_text("permissions:\n  contents: read\nsteps:\n  - run: python3 scripts/publish_channels.py\n")
        self.assertTrue(record["indirect_write_signal"])
        self.assertTrue(record["indirect_write_without_gate_reference"])
        self.assertFalse(record["runtime_gate_order_verified"])

    def test_gate_reference_is_not_runtime_order_proof(self):
        record = self.inspect_text("steps:\n  - run: python3 scripts/publish_channels.py\n  - run: python3 tools/protected_write_gate.py --base HEAD~1\n")
        self.assertFalse(record["indirect_write_without_gate_reference"])
        self.assertFalse(record["runtime_gate_order_verified"])

    def test_gate_after_push_cannot_protect_earlier_write(self):
        record = self.inspect_text("steps:\n  - run: git push origin HEAD:main\n  - run: python3 tools/protected_write_gate.py --base origin/main\n")
        self.assertEqual(record["pushes_without_prior_gate_signal"], 1)
        self.assertEqual(record["tier"], "CRITICAL_UNGATED_PUSH")
        self.assertFalse(record["runtime_gate_order_verified"])

    def test_gate_before_push_is_only_static_order_signal(self):
        record = self.inspect_text("steps:\n  - run: python3 tools/protected_write_gate.py --base origin/main\n  - run: git push origin HEAD:main\n")
        self.assertEqual(record["pushes_without_prior_gate_signal"], 0)
        self.assertTrue(record["push_gate_order_static_signal_only"])
        self.assertFalse(record["runtime_gate_order_verified"])

    def test_same_line_gate_before_push_is_detected(self):
        record = self.inspect_text(
            "steps:\n  - run: python3 tools/protected_write_gate.py --base HEAD && git push origin main\n"
        )
        self.assertEqual(record["pushes_without_prior_gate_signal"], 0)
        self.assertFalse(record["runtime_gate_order_verified"])

    def test_same_line_gate_after_push_is_still_critical(self):
        record = self.inspect_text(
            "steps:\n  - run: git push origin main && python3 tools/protected_write_gate.py --base HEAD\n"
        )
        self.assertEqual(record["pushes_without_prior_gate_signal"], 1)
        self.assertEqual(record["tier"], "CRITICAL_UNGATED_PUSH")

    def test_other_protected_paths_are_identified(self):
        for path in ("HEPSI", "FAVORILER", "YEDEKLER/backup.m3u", "EPG/tv.xml", "logolar/x.png", "arsiv/archive.json"):
            with self.subTest(path=path):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n"
                    "  - run: gh workflow run next.yml\n"
                    + "  - run: echo " + path + "\n"
                )
                self.assertTrue(record["protected_reference"])
                self.assertEqual(record["tier"], "HIGH_WRITE_OR_TRIGGER")

    def test_failure_gate_filename_mentions_are_not_calls(self):
        for mention in ("# python3 tools/workflow_failure_gate.py",
                        "  - 'tools/workflow_failure_gate.py'",
                        '  - run: echo "python3 tools/workflow_failure_gate.py"'):
            with self.subTest(mention=mention):
                record = self.inspect_text(mention + "\n  - run: gh workflow run next.yml\n")
                self.assertEqual(record["failure_gate_call_signal_count"], 0)
                self.assertTrue(record["mutation_or_write_permission_without_failure_gate_signal"])

    def test_failure_gate_call_is_static_scope_not_runtime_proof(self):
        for invocation in ("  - run: python3 tools/workflow_failure_gate.py",
                           "  - run: |\n      python tools/workflow_failure_gate.py"):
            with self.subTest(invocation=invocation):
                record = self.inspect_text(invocation + "\n  - run: git push origin HEAD\n")
                self.assertEqual(record["failure_gate_call_signal_count"], 1)
                self.assertFalse(record["mutation_or_write_permission_without_failure_gate_signal"])
                self.assertFalse(record["failure_circuit_runtime_verified"])
                # A failure circuit never substitutes for protected-write authorization.
                self.assertEqual(record["tier"], "CRITICAL_UNGATED_PUSH")

    def test_write_permission_without_command_still_needs_circuit_review(self):
        record = self.inspect_text("permissions:\n  actions: write\nsteps:\n  - run: echo pending\n")
        self.assertTrue(record["mutation_or_write_permission_without_failure_gate_signal"])
        readonly = self.inspect_text("permissions:\n  contents: read\nsteps:\n  - run: echo safe\n")
        self.assertFalse(readonly["mutation_or_write_permission_without_failure_gate_signal"])

    def test_real_scope_report_does_not_treat_ci_path_filters_as_enforcement(self):
        from scripts.k1_workflow_risk_inventory import audit
        report = audit()
        calls = report["failure_gate_call_signal_workflows"]
        self.assertEqual(set(calls), {".github/workflows/" + name for name in
                                     ("madsc-birlesik-kesif.yml", "madsc-son-kontrol.yml", "madsc-uc-asama.yml")})
        self.assertEqual(report["failure_circuit_runtime_verified_workflows"], 0)
        self.assertIn(".github/workflows/vod-guncelle.yml", report["failure_circuit_scope_review_paths"])

if __name__ == "__main__":
    unittest.main()
