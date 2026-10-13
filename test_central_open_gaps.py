import unittest
from scripts.central_open_gaps import build

class AcikIsDenetimiTesti(unittest.TestCase):
    def test_rapor_varligi_gorev_tamamlandi_sayilmaz(self):
        tasks = {"tasks":[{"no":1,"gorev":"Test","eksikler":["Cihaz kaniti eksik"]},
                          {"no":2,"gorev":"Diger","eksikler":[]}]}
        management = {"sections":{"logo":{"status":"RAPOR_VAR"},
                                  "backup":{"status":"KANIT_YOK"}}}
        report = build(tasks,management)
        self.assertEqual(report["open_task_count"],1)
        self.assertEqual(report["missing_or_invalid_reports"],["backup"])
        self.assertNotEqual(report["tasks"][1]["durum"],"TAMAMLANDI")
        self.assertEqual(report["tasks"][0]["user_ibo_approval"],"NOT_VERIFIED")
    def test_eksik_rapor_basari_sayilmaz(self):
        report = build(None,None)
        self.assertFalse(report["task_report_present"])
        self.assertFalse(report["management_report_present"])

if __name__ == "__main__":
    unittest.main()
