import unittest
from scripts.k1_24_rule_evidence import audit, EVIDENCE

class K124RuleEvidenceTests(unittest.TestCase):
    def test_documented_rules(self):
        result = audit()
        self.assertTrue(result["rule_count_valid"])
        self.assertEqual(len(result["rows"]), 26)
        self.assertEqual(result["documented_rules"], list(range(1, 27)))
        self.assertEqual(set(EVIDENCE), set(range(1, 27)))

    def test_unverified_rules_are_not_marked_complete(self):
        result = audit()
        self.assertEqual(result["fully_verified_rules"], 0)
        self.assertTrue(all(row["status"] in ("PARTIAL_EVIDENCE", "NEEDS_EVIDENCE") for row in result["rows"]))

if __name__ == "__main__":
    unittest.main()
