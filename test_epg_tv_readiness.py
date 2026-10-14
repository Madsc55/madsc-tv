import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from scripts.epg_tv_readiness import inspect, TARGETS

class EPGReadinessTest(unittest.TestCase):
    def test_five_channel_xmltv_device_approval_stays_pending(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for filename in ("full.xml", "pilot.xml"):
                tv = ET.Element("tv")
                for cid in TARGETS:
                    ET.SubElement(tv, "channel", id=cid)
                    ET.SubElement(tv, "programme", channel=cid, start="20261014120000 +0000", stop="20261014130000 +0000")
                ET.ElementTree(tv).write(root / filename, encoding="utf-8")
            (root / "report.json").write_text(json.dumps({"programmes": 5, "playlist_entries": 1039, "matched_entries": 730, "usable_playlist_entries": 583, "sources": []}))
            result = inspect(root / "full.xml", root / "pilot.xml", root / "report.json")
            self.assertTrue(result["technical_xmltv_ready"])
            self.assertFalse(result["tv_ibo_player_verified"])
            self.assertEqual(result["status"], "TV_KONTROLU_BEKLIYOR")
            self.assertEqual(len(result["pilot_channels"]), 5)

    def test_missing_programme_not_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tv = ET.Element("tv")
            for cid in TARGETS:
                ET.SubElement(tv, "channel", id=cid)
                ET.SubElement(tv, "programme", channel=cid)
            ET.ElementTree(tv).write(root / "full.xml", encoding="utf-8")
            tv.remove(tv.findall("programme")[0])
            ET.ElementTree(tv).write(root / "pilot.xml", encoding="utf-8")
            (root / "report.json").write_text('{"programmes":5}')
            result = inspect(root / "full.xml", root / "pilot.xml", root / "report.json")
            self.assertFalse(result["technical_xmltv_ready"])
            self.assertEqual(result["status"], "TEKNIK_HAZIRLIK_EKSIK")

if __name__ == "__main__":
    unittest.main()
