"""Bes is icin tek dosyada merkezi entegrasyon kontrolleri.

Bu testler canli yayin veya IBO Player testi degildir.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKFLOW = ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml"


class BesIsTekDosyaTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_01_kanal_kesfi_ve_yayin_kaniti(self):
        self.assertIn("scripts/central_all_remaining_tasks.py", self.workflow)
        self.assertIn("scripts/central_main_playlist_run_evidence.py", self.workflow)
        self.assertTrue((ROOT / "scripts/central_all_remaining_tasks.py").is_file())

    def test_01b_tek_ekranda_aday_alternatif_ozeti(self):
        source = (ROOT / "scripts/central_single_screen_report.py").read_text(encoding="utf-8")
        self.assertIn('"kesif_ve_yabanci_kaynak_toplu_ozet.json"', source)
        self.assertIn('"aday_ve_alternatif"', source)
        self.assertIn('Aday ve alternatif URL dökümü', source)

    def test_02_logo_epg_kimlik_kaniti(self):
        self.assertIn("scripts/central_identity_epg_logo_audit.py", self.workflow)
        self.assertIn("scripts.candidate_logo_missing_report", self.workflow)

    def test_03_yedek_geri_yukleme_kaniti(self):
        self.assertIn("scripts/central_isolated_git_restore.py", self.workflow)
        self.assertIn("scripts/central_backup_evidence.py", self.workflow)

    def test_04_otomasyon_ve_koruma(self):
        self.assertIn("scripts/central_workflow_inventory.py", self.workflow)
        self.assertIn("scripts/central_consolidation_audit.py", self.workflow)
        self.assertIn("scripts/central_protected_write_gate.py", self.workflow)
        self.assertIn("contents: read", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)

    def test_06_bes_is_gercek_rapor_entegrasyonu(self):
        """Tek kosuda bes bolumun acik kanitlari kaybolmadan raporlanir."""
        import json
        import tempfile
        from scripts.central_single_screen_report import build, markdown
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            discovery = folder / "kesif"
            discovery.mkdir()
            (folder / "kesif_ve_yabanci_kaynak_toplu_ozet.json").write_text(
                json.dumps({"candidate_queue_count": 3, "alternative_queue_count": 2,
                            "candidate_queue_missing_url": 1,
                            "alternative_queue_missing_url": 1}), encoding="utf-8")
            (folder / "tek_islem_coklu_push_analizi.json").write_text(
                json.dumps({"tekrarli_senaryolar": ["ornek tekrar"],
                            "merkezi_denetime_ulasamayan_senaryolar": []}), encoding="utf-8")
            (discovery / "candidate_logo_missing_report.json").write_text(
                json.dumps({"total_candidates": 3,
                            "category_counts": {"LOGO_KAYNAGI_YOK": 2}}), encoding="utf-8")
            report = build(folder, discovery)
        groups = {row["alan"]: row["acik"] for row in report["toplu_alan_ozeti"]}
        self.assertEqual(len(groups), 5)
        self.assertEqual(sum(groups.values()), report["acik_is_sayisi"])
        self.assertGreater(groups["GUVENLIK_YEDEK"], 0)
        self.assertGreater(groups["KANAL_KESIF"], 0)
        self.assertGreater(groups["LOGO_EPG"], 0)
        self.assertGreater(groups["OTOMASYON"], 0)
        self.assertGreater(groups["KABUL"], 0)
        self.assertEqual(report["aday_ve_alternatif"]["candidate_queue_missing_url"], 1)
        self.assertEqual(report["aday_ve_alternatif"]["alternative_queue_count"], 2)
        missing_urls = [item for item in report["acik_isler"]
                        if item["tur"] == "YAYIN_ADRESI_EKSIK"]
        self.assertEqual(len(missing_urls), 2)
        self.assertGreaterEqual(groups["KANAL_KESIF"], 3)

        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")
        output = markdown(report)
        for group in groups:
            self.assertIn(group, output)
        self.assertIn("IBO Player", output)

    def test_05_tek_rapor_ve_genel_kabul(self):
        self.assertIn("scripts/central_single_screen_report.py", self.workflow)
        self.assertIn("TEK_EKRAN_TOPLU_SONUC.md", self.workflow)
        self.assertIn("python3 -m unittest discover -s . -p 'test_*.py'", self.workflow)
        self.assertIn("actions/upload-artifact@v4", self.workflow)


if __name__ == "__main__":
    unittest.main()
