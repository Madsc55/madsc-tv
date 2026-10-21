"""Pinned read-only workflow exemption must fail closed on every source edit."""
import unittest
from unittest.mock import patch
from scripts import k1_reviewed_readonly_scanner as m

FIXTURE = """name: fixture
permissions:
  contents: read
jobs:
  test:
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: |
          python - <<'PY'
          if re.search(r"\\bgit\\s+push\\b",raw): report["warnings"].append("review")
          PY
"""


class PinnedReadOnlyScannerTests(unittest.TestCase):
    def accepted(self, text=FIXTURE, name=m.REVIEWED_WORKFLOW):
        with patch.object(m, "REVIEWED_BLOB_SHA", m.git_blob_sha(FIXTURE)):
            return m.is_reviewed_readonly_scanner(name, text)

    def test_exact_reviewed_fixture(self):
        self.assertTrue(self.accepted())

    def test_other_workflow_is_not_exempt(self):
        self.assertFalse(self.accepted(name="writer.yml"))

    def test_any_source_edit_invalidates_exception(self):
        for change in ("\n# changed", "\n  contents: write", "\n  git push origin main",
                       "\n  if git push origin main; then echo ok; fi",
                       "\n  python -c \"import os;os.system('git push origin main')\""):
            with self.subTest(change=change):
                self.assertFalse(self.accepted(FIXTURE + change))

    def test_credential_change_invalidates_exception(self):
        self.assertFalse(self.accepted(FIXTURE.replace("persist-credentials: false", "persist-credentials: true")))

    def test_literal_scanner_change_invalidates_exception(self):
        self.assertFalse(self.accepted(FIXTURE.replace("if re.search", "if not re.search")))

    def test_pin_has_full_git_blob_hash(self):
        self.assertEqual(len(m.REVIEWED_BLOB_SHA), 40)


if __name__ == "__main__":
    unittest.main()
