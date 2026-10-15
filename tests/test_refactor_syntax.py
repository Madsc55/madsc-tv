"""Compile changed refactor files without importing scanners or touching playlists."""
import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "channel_name_normalization.py",
    "discovery_m3u_parser.py",
    "scripts/evidence_reader.py",
    "genis_kanal_tara.py",
    "yeni_kanal_tara.py",
    "liste_kontrol/build.py",
    "arastirma/uydu_karsilastir.py",
    "scripts/central_management_summary.py",
    "scripts/central_open_gaps.py",
    "scripts/central_short_status.py",
    "scripts/central_single_screen_report.py",
    "scripts/central_identity_epg_logo_audit.py",
)


class RefactorSyntaxTests(unittest.TestCase):
    def test_all_refactored_modules_parse(self):
        for name in FILES:
            with self.subTest(file=name):
                source = (ROOT / name).read_text(encoding="utf-8-sig")
                ast.parse(source, filename=name)


if __name__ == "__main__":
    unittest.main()
