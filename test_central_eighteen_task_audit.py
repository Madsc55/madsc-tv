import unittest
from scripts.central_eighteen_task_audit import build

class OnSekizGorevTesti(unittest.TestCase):
    def test_tum_gorevler_bes_asamada_ve_onaysiz(self):
        report = build()
        self.assertEqual(report["toplam"], 18)
        self.assertEqual(sum(report["bes_asama"].values()), 18)
        self.assertEqual([x["no"] for x in report["gorevler"]], list(range(1, 19)))
        self.assertEqual(sum(x["issue"] == 3 for x in report["gorevler"]), 10)
        self.assertFalse(report["tamamlandi"])
        self.assertEqual(report["tamamlanmis_gorev_sayisi"], 0)
        self.assertEqual(report["canli_kanit_bekleyen_gorevler"], list(range(1, 19)))
        self.assertTrue(all(not x["ibo_onaylandi"] and not x["canli_dogrulandi"] for x in report["gorevler"]))

    def test_eksik_dosya_tamamlandi_sayilmaz(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as tmp:
            report = build(Path(tmp))
            self.assertEqual(report["kod_kaniti_eksik"], 18)
            self.assertEqual(report["eksik_kod_gorevleri"], list(range(1, 19)))
            self.assertTrue(all(x["durum"] == "KOD_KANITI_EKSIK" for x in report["gorevler"]))

if __name__ == "__main__":
    unittest.main()
