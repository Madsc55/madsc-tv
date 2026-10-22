import unittest
from scripts.k1_24_rule_evidence import audit, EVIDENCE

class K124RuleEvidenceTests(unittest.TestCase):
    def test_documented_rules(self):
        result = audit()
        self.assertTrue(result["rule_count_valid"])
        self.assertEqual(len(result["rows"]), 26)
        self.assertEqual(result["documented_rules"], list(range(1, 27)))
        self.assertEqual(set(EVIDENCE), set(range(1, 27)))

    def test_test_candidates_are_visible_but_not_runtime_proof(self):
        rows = {row["rule"]: row for row in audit()["rows"]}
        for number in (1, 2, 17, 21, 24, 25):
            with self.subTest(rule=number):
                self.assertTrue(rows[number]["automated_test_candidates"])
                self.assertEqual(rows[number]["automated_test_files_present"],
                                 rows[number]["automated_test_candidates"])
                self.assertFalse(rows[number]["runtime_enforcement_verified"])

    def test_evidence_counts_are_consistent(self):
        report = audit()
        self.assertEqual(report["partial_evidence_count"] + report["needs_evidence_count"], 26)
        self.assertEqual(report["runtime_unverified_rule_numbers"], list(range(1, 27)))
        self.assertFalse(report["runtime_acceptance_allowed"])

    def test_unverified_rules_are_not_marked_complete(self):
        result = audit()
        self.assertEqual(result["fully_verified_rules"], 0)
        self.assertTrue(all(row["status"] in ("PARTIAL_EVIDENCE", "NEEDS_EVIDENCE") for row in result["rows"]))

if __name__ == "__main__":
    unittest.main()
