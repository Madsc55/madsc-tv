"""Regression for read-only EPG/Pages and backup shadow workflow permissions."""
import unittest
from scripts.five_category_permission_gate import validate, main, TARGETS

GATE = "EPG ve Pages yayin baglantisi salt okunur kabul kontrolu"

class ShadowPermissionGateTests(unittest.TestCase):
    def test_inline_heredoc_text_is_not_a_permission(self):
        raw = """permissions:
  contents: read
  actions: read
jobs:
  check:
    steps:
      - name: EPG ve Pages yayin baglantisi salt okunur kabul kontrolu
        run: |
          python3 - <<'PY'
          text = 'contents: write'
          print(text)
          PY
"""
        self.assertEqual(validate(raw, GATE), [("contents", "read"), ("actions", "read")])

    def test_nested_write_permission_is_rejected(self):
        raw = """permissions:
  contents: read
jobs:
  check:
    permissions:
      contents: write
    steps:
      - name: EPG ve Pages yayin baglantisi salt okunur kabul kontrolu
        run: echo test
"""
        with self.assertRaisesRegex(AssertionError, "Write or unknown"):
            validate(raw, GATE)

    def test_missing_acceptance_gate_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, "Missing shadow"):
            validate("permissions:\n  contents: read\n", GATE)

    def test_current_two_workflows_remain_read_only(self):
        result = main()
        self.assertEqual(set(result), set(TARGETS))

if __name__ == "__main__":
    unittest.main()
