import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from scripts.central_main_playlist_run_evidence import build

class AnaListeKosuKanitiTest(unittest.TestCase):
    def test_kanit_yoksa_basarili_sayilmaz(self):
        with TemporaryDirectory() as tmp:
            report = build(Path(tmp))
            self.assertEqual(report["durum"], "KOSU_KANITI_YOK")
            self.assertFalse(report["butun_ana_liste_test_edildi"])

    def test_yesil_kosu_kanal_onayi_degil(self):
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "son_100_kosu.json").write_text(json.dumps([
                {"name": "MADSC - 3. Aşama Ana Liste Sağlık Kontrolü",
                 "run_id": 100, "status": "completed", "conclusion": "success",
                 "created_at": "2026-10-14T07:00:00Z"}]))
            report = build(folder)
            self.assertEqual(report["durum"], "IS_AKISI_BASARILI_KANAL_SONUCU_INCELENMELI")
            self.assertFalse(report["kanal_sonuclari_dogrulandi"])

    def test_kirmizi_kosu_belli_olur(self):
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "son_100_kosu.json").write_text(json.dumps([
                {"name": "MADSC - 3. Aşama Ana Liste Sağlık Kontrolü",
                 "run_id": 101, "status": "completed", "conclusion": "failure"}]))
            self.assertEqual(build(folder)["durum"], "IS_AKISI_BASARISIZ")

if __name__ == "__main__":
    unittest.main()
