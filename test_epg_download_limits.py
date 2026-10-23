"""Offline regression tests for bounded EPG feed downloads."""
import gzip
import io
import unittest
from unittest.mock import patch

from scripts.build_epg import download


class EpgDownloadTests(unittest.TestCase):
    def _read(self, payload):
        with patch("scripts.build_epg.urllib.request.urlopen", return_value=io.BytesIO(payload)):
            return download("https://example.invalid/guide.xml.gz")

    def test_plain_xml(self):
        self.assertEqual(self._read(b"<tv/>"), b"<tv/>")

    def test_gzip_xml(self):
        self.assertEqual(self._read(gzip.compress(b"<tv/>")), b"<tv/>")

    def test_corrupt_gzip_fails_closed(self):
        with self.assertRaises(ValueError):
            self._read(b"\x1f\x8bnot-a-valid-gzip")

    def test_truncated_gzip_fails_closed(self):
        with self.assertRaises(ValueError):
            self._read(gzip.compress(b"<tv/>")[:-5])

    def test_oversized_compressed_feed_fails_closed(self):
        with patch("scripts.build_epg.urllib.request.urlopen", return_value=io.BytesIO(b"x" * 120_000_001)):
            with self.assertRaises(ValueError):
                download("https://example.invalid/guide.xml")


if __name__ == "__main__":
    unittest.main()
