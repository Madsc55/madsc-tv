"""Negative security tests for the read-only workflow inventory."""
import tempfile
import unittest
from pathlib import Path

from scripts.audit_workflow_security import inspect_workflow


class WorkflowSecurityAuditTests(unittest.TestCase):
    def test_detects_write_and_sensitive_file_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            # inspect_workflow expects a path under repository ROOT.
            from scripts.audit_workflow_security import ROOT
            path = ROOT / "tests" / "_security_audit_fixture.yml"
            # Do not write into the repository: mock read_text and relative_to.
            from unittest.mock import patch
            source = ("on:\n  workflow_run:\npermissions:\n  contents: write\n"
                      "jobs:\n  test:\n    steps:\n      - run: git push origin HEAD\n"
                      "      - run: echo CALISANLAR.m3u\n")
            with patch.object(Path, "read_text", return_value=source):
                result = inspect_workflow(path)
            self.assertTrue(result["manual_review_required"])
            self.assertIn("git_push", result["risk_line_numbers"])
            self.assertIn("write_permissions", result["risk_line_numbers"])
            self.assertIn("protected_file_reference", result["risk_line_numbers"])

    def test_flags_force_push_and_token_signals(self):
        from scripts.audit_workflow_security import ROOT
        from unittest.mock import patch
        path = ROOT / "tests" / "_security_audit_fixture.yml"
        source = "permissions:\n  contents: write\nsteps:\n  - run: git -c user.name=bot push --force origin HEAD\n  - run: echo $GH_TOKEN\n"
        with patch.object(Path, "read_text", return_value=source):
            result = inspect_workflow(path)
        self.assertIn("git_force_push", result["risk_line_numbers"])
        self.assertIn("git_push", result["risk_line_numbers"])
        self.assertIn("github_token_env", result["risk_line_numbers"])

    def test_read_only_workflow_no_false_write_signal(self):
        from scripts.audit_workflow_security import ROOT
        from unittest.mock import patch
        path = ROOT / "tests" / "_security_audit_fixture.yml"
        with patch.object(Path, "read_text", return_value="on:\n  workflow_dispatch:\npermissions:\n  contents: read\n"):
            result = inspect_workflow(path)
        self.assertNotIn("write_permissions", result["risk_line_numbers"])
        self.assertFalse(result["manual_review_required"])


if __name__ == "__main__":
    unittest.main()
