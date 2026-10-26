import unittest
from scripts.youtube_turkish_tv_discovery import classify

class TurkishTvGateTests(unittest.TestCase):
    def test_accepts_turkish_tv_for_review_only(self):
        self.assertEqual(classify("TRT 1 TV", url="https://example.org/live.m3u8"),
                         "REVIEW_TURKISH_TV_CANDIDATE_NOT_APPROVED")
    def test_rejects_radio(self):
        self.assertEqual(classify("Türk Radyo FM", url="https://example.org/live"),
                         "REJECT_RADIO")
    def test_rejects_encrypted(self):
        self.assertEqual(classify("Türk TV DRM", url="https://example.org/live"),
                         "REJECT_ENCRYPTED_OR_PAID")
    def test_rejects_foreign_language(self):
        self.assertEqual(classify("Türk TV", language="en", url="https://example.org/live"),
                         "REJECT_NON_TURKISH_LANGUAGE")
    def test_unverified_language_is_not_approved(self):
        self.assertEqual(classify("World News", url="https://example.org/live"),
                         "REVIEW_TURKISH_LANGUAGE_UNVERIFIED")
    def test_youtube_requires_live(self):
        self.assertEqual(classify("Türk TV", url="https://youtube.com/watch?v=abcdefghijk", youtube=True),
                         "REJECT_NOT_CONFIRMED_LIVE")
    def test_never_grants_playlist_approval(self):
        self.assertNotIn("APPROVED", classify("Türk TV", url="https://example.org/live"))

if __name__ == "__main__":
    unittest.main()
