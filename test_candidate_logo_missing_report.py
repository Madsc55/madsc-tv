import unittest
from scripts.candidate_logo_missing_report import build

class YeniAdayLogoTesti(unittest.TestCase):
    def test_eksik_logo_ve_kimlik_onayi(self):
        candidates = [
            {"channel": "Test TV", "stream_sha256": "a", "logo_url": "", "source": "kaynak"},
            {"channel": "Test TV", "stream_sha256": "b", "logo_url": "https://raw.githubusercontent.com/a/logo.png"},
            {"channel": "Diğer", "stream_sha256": "c", "logo_url": "http://local/logo.png",
             "logo_source_review_required": True}]
        prepared = [{"stream_sha256": "b", "status": "PNG_READY_REVIEW_PENDING"}]
        result = build(candidates, prepared)
        self.assertEqual(result["total_candidates"], 3)
        self.assertEqual(result["category_counts"]["LOGO_KAYNAGI_YOK"], 1)
        self.assertEqual(result["category_counts"]["PNG_HAZIR_KIMLIK_ONAYI_BEKLIYOR"], 1)
        self.assertEqual(result["category_counts"]["LOGO_KAYNAGI_GUVENLIK_INCELEMESI"], 1)
        self.assertEqual(len(result["candidates"][0]["same_name_source_suggestions"]), 1)
        self.assertTrue(all(not r["identity_verified"] and not r["playlist_approved"]
                            for r in result["candidates"]))
        self.assertFalse(result["main_playlist_modified"])

    def test_ayni_isim_farkli_logo_otomatik_onaylanmaz(self):
        rows = build([{"channel": "A", "stream_sha256": "1", "logo_url": ""},
                      {"channel": "A", "stream_sha256": "2", "logo_url": "https://a/logo.png"}], [])
        self.assertEqual(len(rows["candidates"][0]["same_name_source_suggestions"]), 1)
        self.assertFalse(rows["candidates"][0]["playlist_approved"])

if __name__ == "__main__":
    unittest.main()
