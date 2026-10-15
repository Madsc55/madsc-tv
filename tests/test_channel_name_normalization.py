"""Regression checks for shared channel-name normalization; no scanner imports."""
import re
import unittest
import unicodedata

from channel_name_normalization import normalize_channel_name


def legacy_wide(s):
    s = re.sub(r'\[[^]]*\]|\([^)]*\)', '', s).casefold()
    s = ''.join(c for c in unicodedata.normalize('NFKD', s.replace('ı', 'i')) if not unicodedata.combining(c))
    s = re.sub(r'\b(4k|uhd|fhd|hd|sd|hq|1440p|1080p|720p|576p|480p|360p|270p|aday|alternatif|tr)\b', '', s)
    return re.sub(r'[^a-z0-9]', '', s)


def legacy_new(name):
    name = name.upper().translate(str.maketrans("İÇŞĞÜÖ", "ICSGUO"))
    name = re.sub(r"\[[^]]*\]|\([^)]*\)", " ", name)
    name = re.sub(r"\b(?:TR|TURKIYE|HD|FHD|UHD|QHD|SD|1080P|720P|576P|480P|360P)\b", " ", name)
    return re.sub(r"[^A-Z0-9]", "", name)


class NormalizationParity(unittest.TestCase):
    CASES = (
        "TRT 1 HD", "TRT ÇOCUK", "İmam Hussein TV 5", "KANAL D (YEDEK)",
        "SHOW TV [ADAY]", "TRT TÜRK 1080p", "TGRT BELGESEL", "İSTANBUL TV",
        "ısparta tv", "Türkiye TR HD", "TV 8.5", "BRT 2", "Kanal 7",
        "ÖZGÜR TV", "4K UHD TRT 1", "Show Max Alternatif", "", "A [X] (Y)",
    )

    def test_wide_scan_legacy_parity(self):
        for name in self.CASES:
            with self.subTest(name=name):
                self.assertEqual(normalize_channel_name(name, "wide_scan"), legacy_wide(name))

    def test_new_scan_legacy_parity(self):
        for name in self.CASES:
            with self.subTest(name=name):
                self.assertEqual(normalize_channel_name(name, "new_scan"), legacy_new(name))

    def test_satellite_profiles_keep_distinct_numeric_rules(self):
        self.assertEqual(normalize_channel_name("TRT 1 HD", "satellite"), "trt1")
        self.assertEqual(normalize_channel_name("TRT 1 HD", "satellite_playlist"), "trt1")
        self.assertEqual(normalize_channel_name("SHOW TV 2", "satellite"), "showtv2")
        self.assertEqual(normalize_channel_name("SHOW TV 2", "satellite_playlist"), "showtv")
        self.assertEqual(normalize_channel_name("Imam Hussein TV 5", "satellite_playlist"), "imamhusseintv5")
        self.assertEqual(normalize_channel_name("SHOW TV (TEST) HD", "satellite"), "showtv")

    def test_unknown_profile_fails_closed(self):
        with self.assertRaises(ValueError):
            normalize_channel_name("TRT 1", "unknown")


if __name__ == "__main__":
    unittest.main()
