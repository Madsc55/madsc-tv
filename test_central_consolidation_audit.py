import tempfile
import unittest
from pathlib import Path
from scripts.central_consolidation_audit import analyze, acceptance, pending_tasks, push_rules

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

    def test_paths_ignore_kontrolu(self):
        flows = {"istisna.yml": "on:\n  push:\n    paths-ignore:\n      - 'DEVAM_NOTU.md'\njobs:\n  test:\n    runs-on: ubuntu-latest\n"}
        result = analyze(flows, {"Not": ["DEVAM_NOTU.md"], "Liste": ["CALISANLAR.m3u"]})
        self.assertEqual(result["senaryolar"][0]["ayri_kosu_sayisi"], 0)
        self.assertEqual(result["senaryolar"][1]["ayri_kosu_sayisi"], 1)

    def test_merkezi_rapor_sozdizimi(self):
        import ast
        source = Path("scripts/central_consolidation_audit.py").read_text(encoding="utf-8")
        ast.parse(source)

    def test_korunan_kapi_ve_tekrar_kanitlari_kabulde(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "protected-write-gate-report.json").write_text(json.dumps({
                "workflows_scanned": 12, "review_count": 3, "errors": []}))
            (folder / "tek_islem_coklu_push_analizi.json").write_text(json.dumps({
                "senaryolar": [{"islem": "Kanal"}], "tekrarli_senaryolar": ["Kanal"]}))
            report = acceptance(folder)
        statuses = {x["alan"]: x["durum"] for x in report["kriterler"]}
        self.assertEqual(statuses["Korunan liste yazma kapısı"],
                         "DENETIM_VAR_MANUEL_INCELEME_GEREKLI")
        self.assertEqual(statuses["Tek işlem / tek merkezi push hedefi"], "TEKRARLI_PUSH_VAR")
        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")

    def test_kalan_isler_kanitli_ve_onaysizdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = acceptance(Path(tmp))
        todo = pending_tasks(report)
        self.assertEqual(todo["genel_durum"], "HENUZ_ONAYLANMADI")
        self.assertEqual(todo["bekleyen_is_sayisi"], len(report["kriterler"]))
        self.assertEqual(todo["kanit_mevcut_ama_onay_bekleyen"], 0)
        self.assertEqual(todo["kanit_eksik_veya_kullanici_onayi_bekleyen"], len(report["kriterler"]))
        self.assertTrue(all(not item["tamamlandi"] and item["kanit"] and item["sonraki_is"]
                            for item in todo["isler"]))
        self.assertTrue(any("IBO Player" in item["alan"] for item in todo["isler"]))

    def test_kanit_mevcut_olsa_bile_son_kabul_yok(self):
        report = {"genel_kabul": "HENUZ_ONAYLANMADI", "kriterler": [
            {"alan": "GitHub çalışma geçmişi", "durum": "SON_100_KOSU_VAR", "kanit": "son_100_kosu.json"},
            {"alan": "IBO Player gerçek cihaz kabulü", "durum": "KULLANICI_ONAYI_BEKLENIYOR", "kanit": "IBO"}]}
        result = pending_tasks(report)
        self.assertEqual(result["kanit_mevcut_ama_onay_bekleyen"], 1)
        self.assertEqual(result["kanit_eksik_veya_kullanici_onayi_bekleyen"], 1)
        self.assertEqual(result["bekleyen_is_sayisi"], 2)
        self.assertTrue(all(not x["tamamlandi"] for x in result["isler"]))

    def test_kabul_kanitsiz_asla_tamamlanmaz(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = acceptance(Path(tmp))
        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")
        self.assertTrue(any(x["durum"] == "KULLANICI_ONAYI_BEKLENIYOR" for x in report["kriterler"]))

if __name__ == "__main__":
    unittest.main()
