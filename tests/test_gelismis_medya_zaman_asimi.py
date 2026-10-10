"""Zaman aşımı yayınları bozuk sayılmamalı; gerçek ağa erişmeden kontrol."""
import subprocess
import unittest
from unittest.mock import patch

import gelismis_medya_testi


class ZamanAsimiTesti(unittest.TestCase):
    def test_zaman_asimi_tekrar_test_bekliyor(self):
        aday = {"YAYIN_URL": "https://example.org/test.m3u8", "MEDYA_TEST": "VIDEO_SES_VAR"}
        with patch.object(gelismis_medya_testi.subprocess, "run", side_effect=subprocess.TimeoutExpired(cmd="ffmpeg", timeout=65)):
            sonuc = gelismis_medya_testi.check(aday)
        self.assertEqual(sonuc[2], "TEKRAR_TEST_BEKLIYOR")
        self.assertIn("bozuk sayilmadi", sonuc[3])
        self.assertEqual(sonuc[:2], ["BELIRSIZ", "BELIRSIZ"])


if __name__ == "__main__":
    unittest.main()
