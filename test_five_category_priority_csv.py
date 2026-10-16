import ast
import csv
import io
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class PriorityCSVTests(unittest.TestCase):
    def probe(self, result):
        # Load only the existing probe function; importing the module runs live scans.
        source = Path(__file__).parent / 'scripts/oncelikli_kanal_dogrula.py'
        node = next(n for n in ast.parse(source.read_text()).body
                    if isinstance(n, ast.FunctionDef) and n.name == 'probe')
        run = Mock(return_value=result)
        namespace = {'subprocess': SimpleNamespace(run=run), 'json': json}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
        return namespace['probe'](('Fixture', 'Channel', 'https://example.test/stream', 'fixture-source'))

    def test_failed_media_roundtrip_preserves_url_source_and_error_columns(self):
        row = self.probe(SimpleNamespace(returncode=1, stderr='fixture ffprobe failure'))
        self.assertEqual(len(row), 8)
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(['GRUP', 'KANAL', 'TEKNIK_MEDYA', 'COZUNURLUK', 'SES_IZI', 'HATA', 'YAYIN_URL', 'KAYNAK'])
        writer.writerow(row)
        actual = next(csv.DictReader(io.StringIO(stream.getvalue())))
        self.assertEqual(actual['YAYIN_URL'], 'https://example.test/stream')
        self.assertEqual(actual['KAYNAK'], 'fixture-source')
        self.assertEqual(actual['HATA'], 'fixture ffprobe failure')
        self.assertEqual(actual['TEKNIK_MEDYA'], 'DOGRULANAMADI')
        self.assertNotIn(None, actual)

    def test_successful_media_keeps_same_contract(self):
        row = self.probe(SimpleNamespace(returncode=0, stdout=json.dumps({'streams': [
            {'codec_type': 'video', 'width': 1920, 'height': 1080}, {'codec_type': 'audio'}]})))
        self.assertEqual(len(row), 8)
        self.assertEqual(row[2], 'VIDEO_SES_VAR')
        self.assertEqual(row[3], '1920x1080')
        self.assertEqual(row[6:], ('https://example.test/stream', 'fixture-source'))
