"""Read-only CI evidence must survive failures without weakening security gates."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
K1 = ROOT / ".github/workflows/k1-protected-write-tests.yml"
K5 = ROOT / ".github/workflows/madsc-05-genel-bakim.yml"
SECURITY = ROOT / ".github/workflows/madsc-01-guvenlik.yml"


class EvidenceContinuityTests(unittest.TestCase):
    def test_k1_evidence_steps_run_after_failed_regression(self):
        source = K1.read_text(encoding="utf-8")
        for name in ("Korunan dosyalari ana dal ile karsilastir",
                     "Tum workflow risk envanterini olustur",
                     "Workflow calistirmadan envanter sayisini dogrula"):
            with self.subTest(step=name):
                self.assertIn("      - name: " + name + "\n        if: ${{ !cancelled() }}", source)
        self.assertIn("      - name: Workflow risk envanterini sakla\n        if: always()", source)
        self.assertIn("      - name: K1 korunan dosya calisma sonu butunluk kontrolu\n        if: always()", source)

    def test_k5_stages_stop_after_failed_security(self):
        source = K5.read_text(encoding="utf-8")
        for stage in ("kademe-1-guvenlik", "kademe-2-kesif", "kademe-3-kanal-test"):
            with self.subTest(stage=stage):
                self.assertIn("needs." + stage + ".result == 'success'", source)
                self.assertNotIn("needs." + stage + ".result != 'cancelled'", source)

    def test_k5_inventory_independent_and_fail_closed(self):
        source = K5.read_text(encoding="utf-8")
        self.assertIn("id: inventory_92\n        if: always()\n        run: python3 scripts/five_category_92_workflow_audit.py", source)
        self.assertLess(source.index("id: inventory_92"), source.index("id: category_evidence"))
        self.assertEqual(source.count('"inventory_92"'), 2)
        self.assertIn('if [[ "${value}" != "success" ]]', source)

    def test_protected_integrity_is_not_confused_with_missing_category_evidence(self):
        source = K5.read_text(encoding="utf-8")
        protected = source.split("      - name: Korunan dosyalar degismedi", 1)[1].split("      - name:", 1)[0]
        self.assertIn("if: always()", protected)
        self.assertIn("--mode check --manifest", protected)
        self.assertNotIn("category_evidence_collect.py --verify", protected)
        category = source.split("      - name: Kategori kanit aktarimini ayri dogrula\n", 1)[1].split("      - name:", 1)[0]
        self.assertIn("if: always()", category)
        self.assertIn("run: python3 scripts/category_evidence_collect.py --verify", category)
        self.assertNotIn("continue-on-error: true", category)

    def test_runtime_rule_acceptance_is_not_waived(self):
        source = SECURITY.read_text(encoding="utf-8")
        self.assertIn("if len(verified) != 26:", source)
        self.assertIn('if [[ "${{ steps.rule_evidence.outcome }}" != "success" ]]', source)

    def test_trigger_paths_cover_new_regressions(self):
        for workflow in (K1, K5):
            source = workflow.read_text(encoding="utf-8")
            for path in ("scripts/k1_reviewed_readonly_scanner.py",
                         "tests/test_k1_reviewed_readonly_scanner.py",
                         "tests/test_k1_k5_ci_evidence.py"):
                with self.subTest(workflow=workflow.name, path=path):
                    self.assertIn("'"+path+"'", source)


if __name__ == "__main__":
    unittest.main()
