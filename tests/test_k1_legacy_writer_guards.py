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
        self.assertIn("  kesif:\n    if: github.ref == 'refs/heads/main'\n", source)
        self.assertIn("python3 tools/protected_write_gate.py --base origin/main", source)
        self.assertIn("git push origin HEAD:main", source)

    def test_epg_writer_is_main_only_and_protected_outputs_remain_blocked(self):
        from tools.protected_write_gate import blocked_paths
        source = (ROOT / "epg-gunluk.yml").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^    if: github\.ref == 'refs/heads/main'$")
        self.assertIn("tools/protected_write_gate.py", source)
        outputs = ("epg/madsc-epg.xml", "epg/ibo-test-epg.xml",
                   "epg/report.json", "epg/tv_kontrol_bekliyor.json")
        self.assertEqual(blocked_paths(outputs), list(outputs),
                         "EPG outputs require explicit authorization; no silent bypass")

    def test_png_writer_outputs_remain_blocked(self):
        from tools.protected_write_gate import blocked_paths
        source = (ROOT / "publish-iptv-png-logos.yml").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^    if: github\.ref == 'refs/heads/main'$")
        self.assertIn("tools/protected_write_gate.py", source)
        self.assertEqual(blocked_paths(["logos/duzeltilmis-ornek.png"]),
                         ["logos/duzeltilmis-ornek.png"])

    def test_epg_png_and_vod_writers_serialize_publication(self):
        for name in ("epg-gunluk.yml", "publish-iptv-png-logos.yml", "vod-guncelle.yml"):
            with self.subTest(workflow=name):
                source = (ROOT / name).read_text(encoding="utf-8-sig")
                self.assertIn("group: madsc-protected-publish-main", source)
                self.assertIn("cancel-in-progress: false", source)

    def test_vod_revalidates_after_rebase_before_push(self):
        source = (ROOT / "vod-guncelle.yml").read_text(encoding="utf-8-sig")
        script = source.split("git diff --cached --quiet ||", 1)[1]
        self.assertLess(script.index("git pull --rebase origin main"),
                        script.index("tools/protected_write_gate.py --base origin/main"))
        self.assertLess(script.index("tools/protected_write_gate.py --base origin/main"),
                        script.index("git push"))

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
