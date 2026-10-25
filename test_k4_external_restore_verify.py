import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from scripts.k4_external_restore_verify import verify_archive

class K4HariciGeriYuklemeTesti(unittest.TestCase):
    def test_izole_geri_yukleme_ve_bozuk_arsiv_reddi(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "backup.tar.gz"
            manifest = root / "manifest.json"
            data = b"protected sample"
            manifest.write_text(json.dumps({"safe/file.txt": hashlib.sha256(data).hexdigest()}))
            with tarfile.open(archive, "w:gz") as tar:
                entry = tarfile.TarInfo("safe/file.txt")
                entry.size = len(data)
                tar.addfile(entry, io.BytesIO(data))
            self.assertTrue(verify_archive(archive, manifest)["external_backup_verified"])
            manifest.write_text(json.dumps({"safe/file.txt": "0" * 64}))
            with self.assertRaisesRegex(ValueError, "SHA256"):
                verify_archive(archive, manifest)

    def test_path_traversal_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "backup.tar"
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"../escape": "0" * 64}))
            with self.assertRaises(ValueError):
                verify_archive(archive, manifest)

if __name__ == "__main__":
    unittest.main()
