import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts.ana_liste_saglik import entries, batch, probe, run

class AnaListeSaglikTest(unittest.TestCase):
    def test_m3u_okuma_ve_gruplama(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "liste.m3u"
            p.write_text('#EXTM3U\n#EXTINF:-1 group-title="Haber",Kanal 1\nhttps://example.org/1\n#EXTINF:-1,Kanal 2\nhttps://example.org/2\n', encoding="utf-8")
            rows = entries(p)
            self.assertEqual([x["kanal"] for x in rows], ["Kanal 1", "Kanal 2"])
            self.assertEqual(rows[0]["kategori"], "Haber")
            self.assertEqual(sum(len(batch(rows, dt.date(2026, 1, d), 1)[0]) for d in (1, 2)), 2)

    def test_hata_asla_silme_karari_degil(self):
        row = {"sira": 1, "kanal": "Örnek", "kategori": "", "url": "https://example.org/test"}
        with patch("scripts.ana_liste_saglik.subprocess.run", side_effect=OSError("erişim")):
            result = probe(row)
        self.assertEqual(result["teknik_durum"], "DOGRULANAMADI")
        self.assertNotIn("url", result)
        self.assertNotIn("https://", json.dumps(result))

    def test_parallel_probe_results_keep_playlist_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            playlist = Path(tmp) / "CALISANLAR.m3u"
            playlist.write_text("#EXTM3U\\n" + "".join(f"#EXTINF:-1,Kanal {n}\\nhttps://example.org/{n}\\n" for n in range(12)), encoding="utf-8")
            original = playlist.read_bytes()
            def fake_probe(row, timeout):
                return {"sira": row["sira"], "kanal": row["kanal"], "teknik_durum": "DOGRULANAMADI", "gerekce": "fixture"}
            with patch("scripts.ana_liste_saglik.probe", side_effect=fake_probe):
                report = run(playlist, Path(tmp) / "report", dt.date(2026, 10, 18), 100, 10)
            self.assertEqual([x["sira"] for x in report["sonuclar"]], list(range(1, 13)))
            self.assertEqual(playlist.read_bytes(), original)

    def test_sadece_rapor_ana_listeye_dokunma(self):
        with tempfile.TemporaryDirectory() as tmp:
            playlist = Path(tmp) / "CALISANLAR.m3u"
            playlist.write_text('#EXTM3U\n#EXTINF:-1,Örnek\nhttps://example.org/test\n', encoding="utf-8")
            before = playlist.read_bytes()
            with patch("scripts.ana_liste_saglik.probe", return_value={"sira": 1, "kanal": "Örnek", "kategori": "", "url_kimligi": "abc", "teknik_durum": "DOGRULANAMADI", "gerekce": "Geçici hata"}):
                report = run(playlist, Path(tmp) / "rapor", dt.date(2026, 10, 14), 50, 1)
            self.assertEqual(playlist.read_bytes(), before)
            self.assertFalse(report["otomatik_kanal_degisikligi"])
            self.assertEqual(report["bu_kosuda_test_edilen"], 1)

if __name__ == "__main__":
    unittest.main()
