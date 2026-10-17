import tempfile
import unittest
from pathlib import Path
from scripts.central_consolidation_audit import analyze, acceptance, pending_tasks, push_rules

class TopluMerkezTesti(unittest.TestCase):
    def test_logo_epg_kesif_degisiklikleri_merkeze_gider(self):
        root = Path(".github/workflows")
        flows = {p.name: p.read_text(encoding="utf-8") for p in root.glob("*.y*ml")}
        cases = {
            "Ana logo kodu": ["scripts/automatic_png_logos.py"],
            "Ana logo workflow": [".github/workflows/automatic-png-logos.yml"],
            "Aday logo": ["scripts/candidate_logo_report.py"],
            "Keşif": ["madsc_akilli_kesif.py"],
            "EPG": ["scripts/build_epg.py"],
            "EPG yayını": [".github/workflows/epg-pages.yml"],
        }
        result = analyze(flows, cases)
        for case in result["senaryolar"]:
            self.assertEqual(case["push_is_akislari"],
                             ["madsc-aylik-merkezi-denetim.yml"], case["islem"])

    def test_tum_yeni_testler_ve_analiz_araclari_tek_merkeze_gider(self):
        root = Path(".github/workflows")
        flows = {p.name: p.read_text(encoding="utf-8") for p in root.glob("*.y*ml")}
        scenarios = {
            "Yeni test": ["test_yeni_regresyon.py"],
            "Yeni analiz": ["scripts/yeni_analiz.py"],
            "Ana liste yayın kodu": ["scripts/ana_liste_saglik.py"],
            "Ana liste sağlık workflow": [".github/workflows/madsc-ana-liste-saglik.yml"],
            "Merkezi denetim kodu": ["scripts/central_workflow_inventory.py"],
        }
        report = analyze(flows, scenarios)
        for case in report["senaryolar"]:
            expected = ["madsc-aylik-merkezi-denetim.yml"]
            # The branch-only five-stage CI intentionally runs for central
            # security/audit changes. Keep the second trigger visible rather
            # than incorrectly asserting that it does not exist.
            if case["islem"] == "Merkezi denetim kodu":
                expected = ["madsc-05-genel-bakim.yml", *expected]
            self.assertEqual(case["push_is_akislari"], expected, case["islem"])

    def test_not_degisikligi_agir_merkezi_push_baslatmaz(self):
        root = Path(".github/workflows")
        flows = {p.name: p.read_text(encoding="utf-8") for p in root.glob("*.y*ml")}
        report = analyze(flows, {"Not": ["DEVAM_NOTU.md"],
                                 "Toplu rapor": ["TOPLU_DURUM_RAPORU.md"]})
        for case in report["senaryolar"]:
            self.assertEqual(case["push_is_akislari"], [], case["islem"])
        central = flows["madsc-aylik-merkezi-denetim.yml"]
        for name in ("DEVAM_NOTU.md", "TOPLU_DURUM_RAPORU.md"):
            self.assertIn("test -s " + name, central)

    def test_raporda_bilerek_tetiklenmeyen_notlar_hata_sayilmaz(self):
        flows = {"merkez.yml": "on:\n  push:\n    paths:\n      - 'CALISANLAR.m3u'\njobs:\n  test:\n    runs-on: ubuntu-latest\n"}
        report = analyze(flows, {"Proje notu": ["DEVAM_NOTU.md"],
                                 "Toplu durum belgesi": ["TOPLU_DURUM_RAPORU.md"],
                                 "Kanal listesi": ["CALISANLAR.m3u"]})
        self.assertEqual(report["bilerek_push_tetiklemeyen_notlar"],
                         ["Proje notu", "Toplu durum belgesi"])
        self.assertEqual(report["merkezi_denetime_ulasamayan_senaryolar"], [])
        self.assertEqual(report["tekrarli_senaryolar"], [])

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

    def test_sifir_push_kosusu_temiz_sayilmaz(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "tek_islem_coklu_push_analizi.json").write_text(json.dumps({
                "senaryolar": [{"islem": "Yeni test", "ayri_kosu_sayisi": 0}],
                "tekrarli_senaryolar": [],
                "merkezi_denetime_ulasamayan_senaryolar": ["Yeni test"]}))
            report = acceptance(folder)
        statuses = {x["alan"]: x["durum"] for x in report["kriterler"]}
        self.assertEqual(statuses["Tek işlem / tek merkezi push hedefi"],
                         "MERKEZI_PUSH_TETIKLEME_EKSIK")
        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")

    def test_92_workflow_parity_requires_all_verified(self):
        import json
        for verified, expected in ((0, "DAVRANISSAL_ESDEGERLIK_EKSIK_0_92"),
                                   (91, "DAVRANISSAL_ESDEGERLIK_EKSIK_91_92"),
                                   (92, "DAVRANISSAL_ESDEGERLIK_DOGRULANDI")):
            with self.subTest(verified=verified), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp)
                (folder / "92_workflow_gorev_ve_kategori_haritasi.json").write_text(
                    json.dumps({"total": 92, "behavioral_parity_verified_count": verified}),
                    encoding="utf-8")
                report = acceptance(folder)
                row = next(x for x in report["kriterler"]
                           if x["alan"] == "92 eski workflow davranissal esdegerligi")
                self.assertEqual(row["durum"], expected)
                self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")
                todo = pending_tasks(report)
                parity_task = next(x for x in todo["isler"]
                                   if x["alan"] == "92 eski workflow davranissal esdegerligi")
                self.assertFalse(parity_task["tamamlandi"])
                if verified < 92:
                    self.assertFalse(parity_task["kanit_mevcut"])

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
