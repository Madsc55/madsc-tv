import tempfile
import unittest
from pathlib import Path
from scripts.central_consolidation_audit import analyze, acceptance, push_rules

class TopluMerkezTesti(unittest.TestCase):
    def test_dokuman_push_yok(self):
        raw = Path(".github/workflows/madsc-documentation-check.yml").read_text()
        self.assertIsNone(push_rules(raw))

    def test_tek_degisiklik_iki_workflow_uyarisi(self):
        flows = {
            "merkez.yml": "name: merkez\non:\n  push:\n    paths:\n      - 'CALISANLAR.m3u'\n  workflow_dispatch:\njobs:\n  test:\n    runs-on: ubuntu-latest\n",
            "logo.yml": "on:\n  push:\n    paths:\n      - 'CALISANLAR.m3u'\njobs:\n  test:\n    runs-on: ubuntu-latest\n",
            "belge.yml": "on:\n  workflow_dispatch:\njobs:\n  test:\n    runs-on: ubuntu-latest\n"}
        report = analyze(flows, {"Kanal": ["CALISANLAR.m3u"]})
        self.assertEqual(report["senaryolar"][0]["ayri_kosu_sayisi"], 2)
        self.assertEqual(report["tekrarli_senaryolar"], ["Kanal"])

    def test_yalniz_merkez_tek_kosu(self):
        report = analyze({"merkez.yml": "on:\n  push:\n    paths:\n      - 'DEVAM_NOTU.md'\njobs:\n  test:\n    runs-on: ubuntu-latest\n"},
                         {"Not": ["DEVAM_NOTU.md"]})
        self.assertTrue(report["senaryolar"][0]["tek_merkez_hedefi_saglandi"])

    def test_kabul_kanitsiz_asla_tamamlanmaz(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = acceptance(Path(tmp))
        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")
        self.assertTrue(any(x["durum"] == "KULLANICI_ONAYI_BEKLENIYOR" for x in report["kriterler"]))

if __name__ == "__main__":
    unittest.main()
