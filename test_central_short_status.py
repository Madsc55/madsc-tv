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
    def test_kanit_olmayinca_basari_uydurulmaz(self):
        result = render(None,None,None)
        self.assertIn("BILINMIYOR",result)
        self.assertIn("BULUNAMADI",result)

if __name__ == "__main__":
    unittest.main()
