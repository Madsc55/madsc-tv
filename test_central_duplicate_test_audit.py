import unittest
from scripts.central_duplicate_test_audit import inspect

class TekrarTestDenetimi(unittest.TestCase):
    def test_tekrar_ve_ilk_test_ayrimi(self):
        report = inspect({"a":{"runs":1},"b":{"runs":3,"channel":"Kanal"},"c":{"runs":0}})
        self.assertEqual(report["tested_urls"],2)
        self.assertEqual(report["urls_tested_more_than_once"],1)
        self.assertEqual(report["excess_test_runs"],2)
    def test_bozuk_gecmis_kayitlari_yok_sayilmaz(self):
        report = inspect({"x":{"runs":"hatali"},"y":None})
        self.assertEqual(report["invalid_history_records"],2)

if __name__ == "__main__":
    unittest.main()
