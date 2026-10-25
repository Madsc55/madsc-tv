import unittest
from scripts.k5_legacy_parity_gate import compare

def workflow(name, **kwargs):
    row = {"file": name, "schedule_utc": [], "manual": True, "push": False,
           "workflow_run": False, "writes_contents": False,
           "has_concurrency": False, "concurrency_group": ""}
    row.update(kwargs)
    return row

class K5LegacyParityTest(unittest.TestCase):
    def test_same_metadata_is_not_behavioral_proof(self):
        old = {"workflows": [workflow("a.yml")]}
        result = compare(old, old)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["missing_step_level_evidence"], ["a.yml"])
        self.assertFalse(result["behavioral_parity_verified"])

    def test_missing_legacy_workflow_fails(self):
        result = compare({"workflows": [workflow("old.yml")]}, {"workflows": []})
        self.assertEqual(result["missing_workflows"], ["old.yml"])
        self.assertEqual(result["status"], "REVIEW_REQUIRED")

    def test_trigger_change_requires_review(self):
        result = compare({"workflows": [workflow("a.yml", schedule_utc=["0 7 * * *"])]},
                         {"workflows": [workflow("a.yml")]})
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIn("schedule_utc", result["changed_triggers_or_permissions"][0]["differences"])

    def test_duplicate_names_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            compare({"workflows": [workflow("a.yml"), workflow("a.yml")]}, {"workflows": []})

    def test_complete_fingerprints_pass_static_gate_only(self):
        fields = {"job_steps_sha256": "a" * 64, "dispatch_targets": ["target.yml"],
                  "job_dependencies": {"build": ["test"]},
                  "workflow_content_sha256": "b" * 64}
        old = {"workflows": [workflow("a.yml", **fields)]}
        old["historical_source"] = {"ref": "git:legacy-commit", "sha256": "c" * 64}
        old["historical_baseline_verified"] = True
        old["historical_workflow_count"] = 1
        result = compare(old, old)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["behavioral_parity_verified"])

    def test_changed_dispatch_target_requires_review(self):
        fields = {"job_steps_sha256": "a" * 64, "dispatch_targets": ["target.yml"],
                  "job_dependencies": {}, "workflow_content_sha256": "b" * 64}
        old = {"workflows": [workflow("a.yml", **fields)]}
        new = {"workflows": [workflow("a.yml", **{**fields, "dispatch_targets": ["other.yml"]})]}
        result = compare(old, new)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertIn("dispatch_targets", result["changed_triggers_or_permissions"][0]["differences"])

    def test_unverified_historical_baseline_never_passes(self):
        fields = {"job_steps_sha256": "a" * 64, "dispatch_targets": [],
                  "job_dependencies": {}, "workflow_content_sha256": "b" * 64}
        old = {"workflows": [workflow("a.yml", **fields)]}
        result = compare(old, old)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["historical_baseline_verified"])
        self.assertFalse(result["historical_count_matches"])

    def test_historical_count_mismatch_requires_review(self):
        fields = {"job_steps_sha256": "a" * 64, "dispatch_targets": [],
                  "job_dependencies": {}, "workflow_content_sha256": "b" * 64}
        old = {"workflows": [workflow("a.yml", **fields)],
               "historical_baseline_verified": True, "historical_workflow_count": 92}
        result = compare(old, old)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["historical_count_matches"])

    def test_self_attested_baseline_without_source_rejected(self):
        fields = {"job_steps_sha256": "a" * 64, "dispatch_targets": [],
                  "job_dependencies": {}, "workflow_content_sha256": "b" * 64}
        old = {"workflows": [workflow("a.yml", **fields)],
               "historical_baseline_verified": True, "historical_workflow_count": 1}
        result = compare(old, old)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse(result["historical_provenance_metadata_present"])

    def test_added_workflow_requires_review(self):
        fields = {"job_steps_sha256": "a" * 64, "dispatch_targets": [],
                  "job_dependencies": {}, "workflow_content_sha256": "b" * 64}
        old = {"workflows": [workflow("old.yml", **fields)],
               "historical_baseline_verified": True, "historical_workflow_count": 1,
               "historical_source": {"ref": "git:legacy-commit", "sha256": "c" * 64}}
        new = {"workflows": [workflow("old.yml", **fields), workflow("new.yml", **fields)]}
        result = compare(old, new)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["added_workflows"], ["new.yml"])

if __name__ == "__main__":
    unittest.main()
