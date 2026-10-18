"""Read-only tests for the Rule 24 failure circuit breaker."""
import unittest
from unittest.mock import patch, MagicMock
import io
import json
import os
from tools.workflow_failure_gate import should_stop, main


def run(run_id, conclusion, status="completed", created="2026-10-16T00:00:00Z"):
    return {"id": run_id, "conclusion": conclusion, "status": status, "created_at": created}


class FailureGateTests(unittest.TestCase):
    def test_two_failures_open_circuit(self):
        stop, streak = should_stop([run(4, None, "in_progress"), run(3, "failure"), run(2, "timed_out")], 4)
        self.assertEqual((stop, streak), (True, 2))

    def test_success_resets_failure_streak(self):
        stop, streak = should_stop([run(4, None, "in_progress"), run(3, "failure"), run(2, "success"), run(1, "failure")], 4)
        self.assertEqual((stop, streak), (False, 1))

    def test_cancelled_run_breaks_streak(self):
        stop, streak = should_stop([run(4, None, "in_progress"), run(3, "failure"), run(2, "cancelled"), run(1, "failure")], 4)
        self.assertEqual((stop, streak), (False, 1))

    def test_active_and_current_runs_ignored(self):
        stop, streak = should_stop([run(4, "failure"), run(3, None, "in_progress"), run(2, "failure")], 4)
        self.assertEqual((stop, streak), (False, 1))

    def test_later_runs_do_not_count_against_rerun_of_older_job(self):
        runs = [run(10, "failure", created="2026-10-18T10:00:00Z"),
                run(9, "failure", created="2026-10-18T09:00:00Z"),
                run(8, "success", created="2026-10-18T08:00:00Z"),
                run(7, None, status="in_progress", created="2026-10-18T07:00:00Z")]
        self.assertEqual(should_stop(runs, 7), (False, 0))

    def test_same_timestamp_newer_run_is_not_prior_history(self):
        runs = [run(8, "failure"), run(7, "failure"), run(6, None, "in_progress"),
                run(5, "success")]
        self.assertEqual(should_stop(runs, 6), (False, 0))

    def test_undated_prior_runs_fail_closed(self):
        runs = [run(4, None, "in_progress"),
                run(3, "failure", created=None),
                run(2, "failure", created=None)]
        with self.assertRaisesRegex(ValueError, "missing creation timestamp"):
            should_stop(runs, 4)

    def test_undated_active_runs_do_not_block_completed_history(self):
        runs = [run(4, None, "in_progress"), run(3, None, "in_progress", created=None),
                run(2, "success")]
        self.assertEqual(should_stop(runs, 4), (False, 0))

    def test_missing_current_run_metadata_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Current workflow run missing"):
            should_stop([run(3, "failure"), run(2, "failure")], 4)

    def test_github_api_failure_does_not_allow_execution(self):
        env = {"GITHUB_REPOSITORY": "Madsc55/madsc-tv",
               "GITHUB_WORKFLOW_REF": "Madsc55/madsc-tv/.github/workflows/test.yml@refs/heads/main",
               "GITHUB_RUN_ID": "4", "GITHUB_REF_NAME": "main", "GH_TOKEN": "fake"}
        with patch.dict(os.environ, env), patch("urllib.request.urlopen", side_effect=OSError("API unavailable")):
            with self.assertRaises(OSError):
                main()

    def test_missing_current_run_is_not_interpreted_as_success(self):
        payload = {"workflow_runs": [dict(run(3, "failure"), head_branch="main"),
                                     dict(run(2, "failure"), head_branch="main")]}
        env = {"GITHUB_REPOSITORY": "Madsc55/madsc-tv",
               "GITHUB_WORKFLOW_REF": "Madsc55/madsc-tv/.github/workflows/test.yml@refs/heads/main",
               "GITHUB_RUN_ID": "4", "GITHUB_REF_NAME": "main", "GH_TOKEN": "fake"}
        with patch.dict(os.environ, env), patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps(payload).encode())):
            with self.assertRaisesRegex(ValueError, "Current workflow run missing"):
                main()

    def test_manual_dispatch_does_not_bypass_open_circuit(self):
        payload = {"workflow_runs": [
            dict(run(4, None, "in_progress"), head_branch="main"),
            dict(run(3, "failure"), head_branch="main"),
            dict(run(2, "timed_out"), head_branch="main"),
        ]}
        response = io.BytesIO(json.dumps(payload).encode())
        env = {"GITHUB_REPOSITORY": "Madsc55/madsc-tv",
               "GITHUB_WORKFLOW_REF": "Madsc55/madsc-tv/.github/workflows/test.yml@refs/heads/main",
               "GITHUB_RUN_ID": "4", "GITHUB_REF_NAME": "main",
               "GITHUB_EVENT_NAME": "workflow_dispatch", "GH_TOKEN": "fake"}
        with patch.dict(os.environ, env), patch("urllib.request.urlopen", return_value=response) as mocked:
            with self.assertRaises(SystemExit) as caught:
                main()
        self.assertEqual(caught.exception.code, 1)
        mocked.assert_called_once()

    def test_main_filters_other_branches_and_encodes_branch(self):
        payload = {"workflow_runs": [
            dict(run(4, None, "in_progress"), head_branch="madsc/bes-sistem-toplu-birlestirme"),
            dict(run(3, "failure"), head_branch="main"),
            dict(run(2, "failure"), head_branch="main"),
            dict(run(1, "success"), head_branch="madsc/bes-sistem-toplu-birlestirme"),
        ]}
        response = io.BytesIO(json.dumps(payload).encode())
        env = {"GITHUB_REPOSITORY": "Madsc55/madsc-tv",
               "GITHUB_WORKFLOW_REF": "Madsc55/madsc-tv/.github/workflows/test.yml@refs/heads/madsc/bes-sistem-toplu-birlestirme",
               "GITHUB_RUN_ID": "4", "GITHUB_REF_NAME": "madsc/bes-sistem-toplu-birlestirme",
               "GITHUB_EVENT_NAME": "push", "GH_TOKEN": "fake"}
        with patch.dict(os.environ, env), patch("urllib.request.urlopen", return_value=response) as mocked:
            main()
        url = mocked.call_args.args[0].full_url
        self.assertIn("branch=madsc%2Fbes-sistem-toplu-birlestirme", url)


if __name__ == "__main__":
    unittest.main()
