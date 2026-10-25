import unittest
from scripts.k5_github_evidence_probe import probe


class K5GithubEvidenceProbeTests(unittest.TestCase):
    def test_valid_run_job_artifact_metadata(self):
        row = {"legacy_workflow": "legacy.yml", "replacement_workflow": "madsc-05-genel-bakim.yml",
               "source_sha": "a" * 40, "run_id": 10, "job_id": 20, "artifact_id": 30}
        responses = {
            "actions/runs/10": {"conclusion": "success", "head_sha": "a" * 40,
                                "path": ".github/workflows/madsc-05-genel-bakim.yml"},
            "actions/jobs/20": {"run_id": 10, "conclusion": "success"},
            "actions/artifacts/30": {"workflow_run": {"id": 10}, "expired": False, "size_in_bytes": 10},
        }
        result = probe([row], "Madsc55/madsc-tv", "token", lambda repo, endpoint, token: responses[endpoint])
        self.assertEqual(result["github_metadata_verified_count"], 1)
        self.assertEqual(result["independently_verified_behavior_count"], 0)
        self.assertFalse(result["production_ready"])

    def test_wrong_artifact_run_fails(self):
        row = {"legacy_workflow": "legacy.yml", "replacement_workflow": "madsc-05-genel-bakim.yml",
               "source_sha": "a" * 40, "run_id": 10, "job_id": 20, "artifact_id": 30}
        responses = {
            "actions/runs/10": {"conclusion": "success", "head_sha": "a" * 40,
                                "path": ".github/workflows/madsc-05-genel-bakim.yml"},
            "actions/jobs/20": {"run_id": 10, "conclusion": "success"},
            "actions/artifacts/30": {"workflow_run": {"id": 99}, "expired": False, "size_in_bytes": 10},
        }
        result = probe([row], "Madsc55/madsc-tv", "token", lambda repo, endpoint, token: responses[endpoint])
        self.assertEqual(result["github_metadata_verified_count"], 0)
        self.assertIn("artifact_run", result["records"][0]["errors"])

    def test_invalid_repository_rejected(self):
        with self.assertRaises(ValueError):
            probe([], "../outside", "token")

    def test_malformed_artifact_fails_closed(self):
        row = {"legacy_workflow": "legacy.yml", "replacement_workflow": "madsc-05-genel-bakim.yml",
               "source_sha": "a" * 40, "run_id": 10, "job_id": 20, "artifact_id": 30}
        result = probe([row], "Madsc55/madsc-tv", "token", lambda *args: {"workflow_run": None})
        self.assertEqual(result["github_metadata_verified_count"], 0)


if __name__ == "__main__":
    unittest.main()
