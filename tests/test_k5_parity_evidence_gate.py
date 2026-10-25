import unittest
from scripts.k5_parity_evidence_gate import validate

NAMES = [f"legacy-{i:02d}.yml" for i in range(92)]

def sample():
    return {"legacy_workflow": NAMES[0], "replacement_workflow": "madsc-05-genel-bakim.yml",
            "source_sha": "a" * 40, "run_id": 1, "job_id": 2, "artifact_id": 3,
            "checks": {name: True for name in ("trigger", "outputs", "failure_behavior",
                                               "permissions", "protected_paths", "regression")}}

class K5EvidenceGateTests(unittest.TestCase):
    def test_empty_evidence_is_not_approval(self):
        result = validate([], NAMES)
        self.assertEqual(result["independently_verified_count"], 0)
        self.assertFalse(result["production_ready"])
        self.assertEqual(len(result["missing_evidence"]), 92)

    def test_candidate_is_not_verified(self):
        result = validate([sample()], NAMES)
        self.assertEqual(result["candidate_evidence_count"], 1)
        self.assertEqual(result["independently_verified_count"], 0)

    def test_missing_check_rejected(self):
        row = sample()
        row["checks"]["protected_paths"] = False
        with self.assertRaises(ValueError):
            validate([row], NAMES)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            validate([sample(), sample()], NAMES)

    def test_fake_run_rejected(self):
        row = sample()
        row["run_id"] = "1"
        with self.assertRaises(ValueError):
            validate([row], NAMES)

    def test_unknown_workflow_rejected(self):
        row = sample()
        row["legacy_workflow"] = "unknown.yml"
        with self.assertRaises(ValueError):
            validate([row], NAMES)

    def test_duplicate_inventory_rejected(self):
        with self.assertRaises(ValueError):
            validate([], NAMES[:-1] + [NAMES[0]])

    def test_unrecognized_replacement_rejected(self):
        row = sample()
        row["replacement_workflow"] = "madsc-00-fake.yml"
        with self.assertRaises(ValueError):
            validate([row], NAMES)

    def test_inventory_count_rejected(self):
        with self.assertRaises(ValueError):
            validate([], NAMES[:-1])

if __name__ == "__main__":
    unittest.main()
