import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class TekMerkezKuralTesti(unittest.TestCase):
    def test_belge_push_ayri_kosmaz(self):
        doc = (ROOT / ".github/workflows/madsc-documentation-check.yml").read_text()
        self.assertNotIn("\n  push:", doc)
        self.assertIn("workflow_dispatch:", doc)

    def test_logo_kanal_degisiminde_ayri_push_acmaz(self):
        logo = (ROOT / ".github/workflows/automatic-png-logos.yml").read_text()
        self.assertIn("  workflow_dispatch:", logo)
        self.assertIn("    - cron: '23 5 * * *'", logo)
        self.assertNotIn("      - 'CALISANLAR.m3u'", logo)
        self.assertIn("      - 'scripts/automatic_png_logos.py'", logo)
        self.assertIn("  contents: read", logo)
        self.assertIn("Korunan kanal listesi degisikliklerini engelle", logo)

    def test_kesif_kod_degisikligi_ayri_yayin_taramasi_baslatmaz(self):
        workflow = (ROOT / ".github/workflows/madsc-birlesik-kesif.yml").read_text()
        central = (ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml").read_text()
        self.assertNotIn("\n  push:", workflow)
        self.assertIn("  workflow_dispatch:", workflow)
        self.assertIn("    - cron: '0 6 * * *'", workflow)
        for path in ("madsc_akilli_kesif.py", "scripts/discovery_archive.py",
                     "scripts/candidate_logo_report.py",
                     ".github/workflows/madsc-birlesik-kesif.yml"):
            self.assertIn("'" + path + "'", central)

    def test_yeni_aday_png_tek_kesif_turunda_hazirlanir(self):
        workflow = (ROOT / ".github/workflows/madsc-birlesik-kesif.yml").read_text()
        discovery = (ROOT / "madsc_akilli_kesif.py").read_text()
        self.assertIn("python3 madsc_akilli_kesif.py", workflow)
        self.assertNotIn("python -m scripts.candidate_logo_report", workflow)
        self.assertIn("prepare_candidate_artwork(artwork,previous,limit=40)", discovery)
        self.assertIn('candidate_logo_missing_report.json', discovery)
        self.assertIn("Aday yayın logo ve EPG kanıtlarını tek raporda birleştir", workflow)

    def test_korunan_yazma_kapisi_merkezde(self):
        gate = (ROOT / ".github/workflows/test-31-protected-write-gate.yml").read_text()
        central = (ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml").read_text()
        self.assertNotIn("\\n  push:", gate)
        self.assertIn("  workflow_dispatch:", gate)
        self.assertIn("python3 scripts/central_protected_write_gate.py", central)
        self.assertIn("  contents: read", central)

    def test_merkez_dokuman_ve_kanal_kontrolu(self):
        central = (ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml").read_text()
        for name in ("AGENTS.md", "DEVAM_NOTU.md", "CALISANLAR.m3u", "GUVENLIK_KURALLARI.md"):
            self.assertIn("'"+name+"'", central)
        self.assertIn("Proje kayitlari ve dokumantasyonu merkezi kontrolde dogrula", central)
        self.assertIn("  contents: read", central)

if __name__ == "__main__":
    unittest.main()
