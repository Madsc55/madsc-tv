import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pathlib import Path
import json
from scripts.k5_parity_evidence_gate import main
from scripts.k5_parity_evidence_gate import validate

NAMES = [f"legacy-{i:02d}.yml" for i in range(92)]

def sample():
    return {"legacy_workflow": NAMES[0], "replacement_workflow": "madsc-05-genel-bakim.yml",
            "source_sha": "a" * 40, "run_id": 1, "job_id": 2, "artifact_id": 3,
            "checks": {name: True for name in ("trigger", "outputs", "failure_behavior",
                                               "permissions", "protected_paths", "regression")}}

class K5EvidenceGateTests(unittest.TestCase):
    def test_duplicate_replacement_candidates_rejected(self):
        mapping = {name: ["madsc-05-genel-bakim.yml"] for name in NAMES}
        mapping[NAMES[-1]] = ["madsc-05-genel-bakim.yml", "madsc-05-genel-bakim.yml"]
        with self.assertRaises(ValueError):
            validate([], NAMES, mapping)

    def test_unknown_unused_replacement_rejected(self):
        mapping = {name: ["madsc-05-genel-bakim.yml"] for name in NAMES}
        mapping[NAMES[-1]] = ["unknown.yml"]
        with self.assertRaises(ValueError):
            validate([], NAMES, mapping)

    def test_invalid_unused_mapping_candidate_rejected(self):
        mapping = {name: ["madsc-05-genel-bakim.yml"] for name in NAMES}
        mapping[NAMES[-1]] = [None]
        with self.assertRaises(ValueError):
            validate([], NAMES, mapping)

    def test_non_string_legacy_name_rejected(self):
        with self.assertRaises(ValueError):
            validate([], NAMES[:-1] + [None])

    def test_non_string_replacement_rejected(self):
        row = sample()
        row["replacement_workflow"] = None
        with self.assertRaises(ValueError):
            validate([row], NAMES)

    def test_incomplete_mapping_inventory_rejected(self):
        with self.assertRaises(ValueError):
            validate([], NAMES, {NAMES[0]: ["madsc-05-genel-bakim.yml"]})

    def test_non_workflow_inventory_name_rejected(self):
        with self.assertRaises(ValueError):
            validate([], NAMES[:-1] + ["not-a-workflow.txt"])

    def test_unmapped_replacement_rejected(self):
        with self.assertRaises(ValueError):
            validate([sample()], NAMES, {NAMES[0]: ["madsc-01-guvenlik.yml"]})

    def test_mapped_replacement_candidate_still_not_verified(self):
        result = validate([sample()], NAMES, {name: ["madsc-05-genel-bakim.yml"] for name in NAMES})
        self.assertEqual(result["independently_verified_count"], 0)

    def test_production_switch_fails_closed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            inventory = root / "inventory.json"
            evidence = root / "evidence.json"
            output = root / "report.json"
            inventory.write_text(json.dumps({"items": [{"file": name, "possible_replacement_workflows": ["madsc-05-genel-bakim.yml"]} for name in NAMES]}))
            evidence.write_text("[]")
            with patch("sys.argv", ["gate", "--inventory", str(inventory), "--evidence", str(evidence), "--output", str(output), "--require-production-ready"]):
                self.assertEqual(main(), 1)
            self.assertFalse(json.loads(output.read_text())["production_ready"])

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
