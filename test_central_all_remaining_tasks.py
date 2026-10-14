import unittest
from scripts.central_all_remaining_tasks import assemble

class TopluKalanIsTesti(unittest.TestCase):
    def test_sekiz_is_tek_raporda_ve_onay_korunur(self):
        result = assemble({"defined":156,"target":155,"difference":1,"duplicate_endpoints":[],"invalid_endpoint_definitions":[]},
                          {"excess_test_runs":3}, {"protected_missing":[]}, {}, {"failed_runs_in_sample":2}, {"tasks":[]})
        self.assertEqual(result["total"],8)
        self.assertFalse(result["all_done"])
        self.assertEqual(result["jobs"][0]["status"],"INCELEME_GEREKLI")
        self.assertEqual(result["jobs"][1]["evidence"]["excess_test_runs"],3)
        self.assertEqual(result["jobs"][5]["status"],"ONAY_BEKLIYOR")
        self.assertIn(6,result["requires_user_or_external_evidence"])
    def test_izole_geri_yukleme_harici_yedekle_karistirilmaz(self):
        result = assemble(None, None,
                          {"protected_missing": [], "restore_test": "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI"},
                          None, None, None)
        self.assertEqual(result["jobs"][2]["status"],
                         "GIT_HEAD_IZOLE_ESLESME_VAR_HARICI_YEDEK_DOGRULANMADI")
        self.assertFalse(result["jobs"][2]["evidence"]["historical_recovery_verified"])
        self.assertFalse(result["all_done"])

    def test_olcum_dosyasi_var_sayi_yoksa_olcum_sayilmaz(self):
        result = assemble({}, {"status": "OK"}, {}, {}, {}, {})
        self.assertEqual(result["jobs"][1]["status"], "GECMIS_KANITI_YOK")

    def test_eksik_kanit_basarili_sayilmaz(self):
        result = assemble(None,None,None,None,None,None)
        self.assertEqual(result["jobs"][0]["status"],"KANIT_YOK")
        self.assertEqual(result["jobs"][1]["status"],"GECMIS_KANITI_YOK")

if __name__ == "__main__":
    unittest.main()
