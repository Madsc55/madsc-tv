"""Read-only tests for the Rule 24 failure circuit breaker."""
import unittest
from tools.workflow_failure_gate import should_stop


def run(run_id, conclusion, status="completed", created="2026-10-16T00:00:00Z"):
    return {"id": run_id, "conclusion": conclusion, "status": status, "created_at": created}


class FailureGateTests(unittest.TestCase):
    def test_two_failures_open_circuit(self):
        stop, streak = should_stop([run(3, "failure"), run(2, "timed_out")], 4)
        self.assertEqual((stop, streak), (True, 2))

    def test_success_resets_failure_streak(self):
        stop, streak = should_stop([run(3, "failure"), run(2, "success"), run(1, "failure")], 4)
        self.assertEqual((stop, streak), (False, 1))

    def test_cancelled_run_breaks_streak(self):
        stop, streak = should_stop([run(3, "failure"), run(2, "cancelled"), run(1, "failure")], 4)
        self.assertEqual((stop, streak), (False, 1))

    def test_active_and_current_runs_ignored(self):
        stop, streak = should_stop([run(4, "failure"), run(3, None, "in_progress"), run(2, "failure")], 4)
        self.assertEqual((stop, streak), (False, 1))


if __name__ == "__main__":
    unittest.main()
