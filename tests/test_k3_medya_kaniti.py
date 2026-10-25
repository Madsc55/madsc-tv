"""K3 medya kaniti: ag olmadan ayri video/ses decode regresyonlari."""
import subprocess
import unittest
from unittest.mock import patch
import gelismis_medya_testi as k3

ROW = {"YAYIN_URL": "https://example.org/live.m3u8", "MEDYA_TEST": "VIDEO_SES_VAR"}

def result(ok=True, payload=b"decoded"):
    return subprocess.CompletedProcess([], 0 if ok else 1, payload if ok else b"", b"stream missing")

class MedyaKanitTesti(unittest.TestCase):
    def test_iki_medya_gercekten_cozuldu(self):
        with patch.object(k3.subprocess, "run", side_effect=[result(), result()]) as run:
            value = k3.check(ROW)
        self.assertEqual(value[:2], ["EVET", "EVET"])
        self.assertEqual(value[2], "MEDYA_ORNEGI_COZULDU_KIMLIK_BEKLIYOR")
        self.assertIn("sureklilik", value[3])
        self.assertEqual(run.call_count, 2)
        self.assertIn("0:v:0", run.call_args_list[0].args[0])
        self.assertIn("0:a:0", run.call_args_list[1].args[0])

    def test_eski_csv_ses_kaniti_degil(self):
        with patch.object(k3.subprocess, "run", side_effect=[result(), result(False)]):
            value = k3.check(ROW)
        self.assertEqual(value[:2], ["EVET", "BELIRSIZ"])
        self.assertEqual(value[2], "MEDYA_BILESENI_BELIRSIZ")

    def test_bos_cikti_basari_degil(self):
        with patch.object(k3.subprocess, "run", side_effect=[result(payload=b""), result()]):
            value = k3.check(ROW)
        self.assertEqual(value[:2], ["BELIRSIZ", "EVET"])

    def test_video_olmayan_yayin_basarili_sayilmaz(self):
        with patch.object(k3.subprocess, "run", side_effect=[result(False), result()]):
            value = k3.check(ROW)
        self.assertEqual(value[:2], ["BELIRSIZ", "EVET"])
        self.assertEqual(value[2], "MEDYA_BILESENI_BELIRSIZ")

    def test_iki_bilesen_de_basarisizsa_onay_verilmez(self):
        with patch.object(k3.subprocess, "run", side_effect=[result(False), result(False)]):
            value = k3.check(ROW)
        self.assertEqual(value[:2], ["BELIRSIZ", "BELIRSIZ"])

    def test_zaman_asimi_bozuk_olarak_isaretlenmez(self):
        with patch.object(k3.subprocess, "run", side_effect=subprocess.TimeoutExpired("ffmpeg", 65)):
            value = k3.check(ROW)
        self.assertEqual(value[2], "TEKRAR_TEST_BEKLIYOR")

if __name__ == "__main__":
    unittest.main()
