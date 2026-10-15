"""Pure parser parity fixtures; scanner modules are never imported."""
import unittest

from discovery_m3u_parser import parse_discovery_m3u


class DiscoveryM3UParserTests(unittest.TestCase):
    TEXT = """#EXTM3U
#EXTINF:-1 tvg-logo="https://logo.invalid/a.png", TRT 1 HD
https://example.invalid/1.m3u8
#EXTINF:-1,SHOW TV
#COMMENT ignored
https://example.invalid/2.m3u8
#EXTINF:-1,BAD
rtmp://example.invalid/3
https://example.invalid/4.m3u8
#EXTINF:-1,EMPTY
https://example.invalid/5.m3u8
"""

    def test_wide_scan_preserves_original_metadata_and_late_url(self):
        rows = parse_discovery_m3u(self.TEXT, "wide_scan")
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0][0], " TRT 1 HD")
        self.assertEqual(rows[0][2], '#EXTINF:-1 tvg-logo="https://logo.invalid/a.png", TRT 1 HD')
        self.assertEqual(rows[2][0], "BAD")
        self.assertEqual(rows[2][1], "https://example.invalid/4.m3u8")

    def test_new_scan_consumes_pending_entry_on_non_url(self):
        rows = parse_discovery_m3u(self.TEXT, "new_scan")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ("TRT 1 HD", "https://example.invalid/1.m3u8", "https://logo.invalid/a.png"))
        self.assertEqual(rows[1][0], "SHOW TV")
        self.assertEqual(rows[2][0], "EMPTY")

    def test_unknown_policy_rejected(self):
        with self.assertRaises(ValueError):
            parse_discovery_m3u("", "unknown")


if __name__ == "__main__":
    unittest.main()
