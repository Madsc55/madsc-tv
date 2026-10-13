"""Teknik medya probe raporunun kolon kaymasina karsi salt okunur regresyon."""
import ast
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


class OncelikliKanalCsvTesti(unittest.TestCase):
    def test_ffprobe_hatasi_sekiz_kolonda_ve_hata_alaninda_kalir(self):
        path = Path(__file__).parent / "scripts/oncelikli_kanal_dogrula.py"
        parsed = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        probe = next(node for node in parsed.body
                     if isinstance(node, ast.FunctionDef) and node.name == "probe")
        isolated = ast.fix_missing_locations(ast.Module(body=[probe], type_ignores=[]))
        fake_subprocess = SimpleNamespace(run=Mock(return_value=SimpleNamespace(
            returncode=1, stderr="HTTP 403 Forbidden", stdout="")))
        namespace = {"subprocess": fake_subprocess, "json": json}
        exec(compile(isolated, str(path), "exec"), namespace)
        row = namespace["probe"](("TGRT Belgesel", "TGRT Belgesel",
                                  "https://example.org/live.m3u8",
                                  "https://example.org/source.m3u"))
        self.assertEqual(len(row), 8)
        self.assertEqual(row[2], "DOGRULANAMADI")
        self.assertIn("HTTP 403", row[5])
        self.assertEqual(row[6], "https://example.org/live.m3u8")
        self.assertEqual(row[7], "https://example.org/source.m3u")
        fake_subprocess.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
