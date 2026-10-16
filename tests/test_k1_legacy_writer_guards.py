"""Static K1 regression: old write-capable jobs must not run on feature branches."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / ".github" / "workflows"
WRITERS = (
    "madsc-genis-kaynak-kontrol", "madsc-ibo-354-classify",
    "madsc-ibo-364-355-364", "madsc-ibo-398-16-49",
    "madsc-ibo-530-archive", "madsc-ibo-6115-second",
    "madsc-ibo-ilk-239", "madsc-ibo-kararlar-grup1",
    "madsc-ibo-second-voice", "madsc-turk-kanal-geri-sec",
    "madsc-uc-asama", "madsc-yedek-turk-ayir",
    "madsc-yedekler-sayi-duzelt", "publish-iptv-png-logos",
    "vod-guncelle",
)

class LegacyWriterGuards(unittest.TestCase):
    def test_all_15_have_main_ref_job_guard_and_gate(self):
        for name in WRITERS:
            with self.subTest(workflow=name):
                source = (ROOT / (name + ".yml")).read_text(encoding="utf-8-sig")
                self.assertRegex(source, r"(?m)^    if: github\.ref == 'refs/heads/main'$")
                self.assertIn("tools/protected_write_gate.py", source)
                self.assertIn("git push", source)
    def test_combined_discovery_writer_is_main_only(self):
        source = (ROOT / "madsc-birlesik-kesif.yml").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^  kesif:\\n    if: github\\.ref == 'refs/heads/main'$")
        self.assertIn("python3 tools/protected_write_gate.py --base origin/main", source)
        self.assertIn("git push origin HEAD:main", source)

    def test_report_missing_explicit_permissions(self):
        from scripts.k1_workflow_risk_inventory import audit
        report = audit()
        missing = report["missing_permission_paths"]
        print("K1 missing explicit permissions:", ", ".join(missing))
        self.assertEqual(len(missing), report["missing_explicit_permissions"])
        self.assertEqual(missing, [], "Every workflow must declare explicit permissions")

    def test_read_only_ci_has_no_write_permission(self):
        source = (ROOT / "k1-protected-write-tests.yml").read_text()
        self.assertRegex(source, r"(?m)^  contents: read$")
        self.assertIn("persist-credentials: false", source)

if __name__ == "__main__":
    unittest.main()
