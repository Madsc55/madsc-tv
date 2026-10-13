import unittest
from scripts.central_isolated_git_restore import verify

class IzoleGeriYuklemeTesti(unittest.TestCase):
    def test_korunan_dosyalar_git_head_ile_eslesir(self):
        result = verify()
        self.assertTrue(result["all_match"])
        self.assertEqual(len(result["files"]),3)
        self.assertFalse(result["external_backup_verified"])
        self.assertFalse(result["historical_recovery_verified"])

if __name__ == "__main__":
    unittest.main()
