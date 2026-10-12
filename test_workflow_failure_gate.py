import unittest
from tools.workflow_failure_gate import should_stop

def run(i, conclusion, status="completed"):
    return {"id":i,"created_at":f"2026-10-13T00:{i:02d}:00Z","status":status,"conclusion":conclusion}

class GateTests(unittest.TestCase):
    def test_two_failures_stop(self):
        self.assertEqual(should_stop([run(1,"failure"),run(2,"timed_out")],3),(True,2))
    def test_success_resets(self):
        self.assertEqual(should_stop([run(1,"failure"),run(2,"success"),run(3,"failure")],4),(False,1))
    def test_cancelled_breaks_chain(self):
        self.assertEqual(should_stop([run(1,"failure"),run(2,"cancelled"),run(3,"failure")],4),(False,1))
    def test_current_run_ignored(self):
        self.assertEqual(should_stop([run(1,"failure"),run(2,"failure", "in_progress")],2),(False,1))
if __name__ == "__main__":
    unittest.main()
