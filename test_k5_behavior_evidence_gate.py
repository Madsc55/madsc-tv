#!/usr/bin/env python3
import unittest
from scripts.k5_behavior_evidence_gate import validate

def rows():
    return [{"legacy_workflow": f"legacy-{n:02d}.yml",
             "migration_decision": "BLOCKED_NEEDS_BEHAVIOR_EVIDENCE"} for n in range(92)]

class K5BehaviorEvidenceTests(unittest.TestCase):
    def test_empty_registry_never_claims_parity(self):
        # The actual CSV is exercised by the workflow; unit checks the registry contract.
        import csv
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "matrix.csv"
            with path.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["legacy_workflow", "migration_decision"])
                writer.writeheader()
                writer.writerows(rows())
            result = validate(path, {})
            self.assertEqual(result["inventory_total"], 92)
            self.assertEqual(result["evidence_complete_pass_count"], 0)
            self.assertFalse(result["production_parity_verified"])
            self.assertEqual(result["errors"], [])

    def test_unknown_evidence_fails_closed(self):
        import csv
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "matrix.csv"
            with path.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["legacy_workflow", "migration_decision"])
                writer.writeheader()
                writer.writerows(rows())
            result = validate(path, {"unrecognized.yml": {"decision": "PASS"}})
            self.assertTrue(result["errors"])

    def test_forged_run_url_and_invalid_sha_fail_closed(self):
        import csv
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "matrix.csv"
            with path.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["legacy_workflow", "migration_decision"])
                writer.writeheader()
                writer.writerows(rows())
            evidence = {"legacy-00.yml": {
                "legacy_sha": "not-a-sha", "replacement_sha": "b" * 40,
                "trigger_comparison": "checked", "input_output_comparison": "checked",
                "failure_comparison": "checked", "write_permission_comparison": "checked",
                "actions_run_url": "https://github.com/Madsc55/madsc-tv/actions/runs/123/../../fake",
                "decision": "PASS"}}
            result = validate(path, evidence)
            self.assertTrue(result["errors"])
            self.assertEqual(result["evidence_complete_pass_count"], 0)

if __name__ == "__main__":
    unittest.main()
