import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class TopluDurumRaporuTesti(unittest.TestCase):
    def test_bes_asama_ve_acik_kabul_korunur(self):
        report = (ROOT / "TOPLU_DURUM_RAPORU.md").read_text(encoding="utf-8")
        for section in ("1. Güvenlik", "2. Keşif", "3. Kanal testleri",
                        "4. Logo ve EPG", "5. Arşiv ve kabul"):
            self.assertIn(section, report)
        self.assertIn("HENÜZ ONAYLANMADI", report)
        self.assertIn("kullanıcı onayı", report.lower())
        self.assertIn("yeni bulunan adaylara", report)
    def test_merkez_raporu_izler(self):
        flow = (ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml").read_text()
        self.assertIn("'TOPLU_DURUM_RAPORU.md'", flow)
        self.assertIn("test -s TOPLU_DURUM_RAPORU.md", flow)
        self.assertIn("sha256sum AGENTS.md DEVAM_NOTU.md TOPLU_DURUM_RAPORU.md", flow)

if __name__ == "__main__":
    unittest.main()
