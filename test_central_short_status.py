import unittest
from scripts.central_short_status import render

class KisaDurumOzetiTesti(unittest.TestCase):
    def test_basarisiz_ve_eksik_kanit_gorunur(self):
        result = render({"classifications":{"BASARILI":2,"BASARISIZ":1}},
                        {"tasks":[{"eksikler":["bekliyor"]},{"eksikler":[]}]},
                        {"runs":[{"run_id":42,"workflow":"Denetim","failed_jobs":[
                            {"job":"Kontrol","failed_steps":[{"name":"Yayin testi"}]}]}]})
        self.assertIn("Basarisiz: 1", result)
        self.assertIn("Takip gerektiren: 1 / 2", result)
        self.assertIn("Yayin testi", result)
        self.assertIn("kok neden icin log gerekir", result)
    def test_bes_asama_eksikleri_tek_turkce_ozette(self):
        report = render(None, None, None, {
            "five_stage_results": [
                {"number": 1, "name": "Güvenlik", "missing_evidence": []},
                {"number": 2, "name": "Keşif", "missing_evidence": ["kaynak_mutabakati"]},
            ],
            "open_blockers": [{"code": "SOURCE_TARGET_MISMATCH", "status": "INCELEME_GEREKLI"}],
        })
        self.assertIn("Beş aşamalı toplu denetim", report)
        self.assertIn("Keşif: Kanıt eksik", report)
        self.assertIn("SOURCE_TARGET_MISMATCH", report)
        self.assertIn("İnceleme gerektiren engel: 1", report)

    def test_kanit_olmayinca_basari_uydurulmaz(self):
        result = render(None,None,None)
        self.assertIn("BILINMIYOR",result)
        self.assertIn("BULUNAMADI",result)

if __name__ == "__main__":
    unittest.main()
