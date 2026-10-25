import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from scripts.k4_external_restore_verify import verify_archive

class K4HariciGeriYuklemeTesti(unittest.TestCase):
    def create_case(self, root, name="safe/file.txt", data=b"protected sample", kind=tarfile.REGTYPE):
        archive = root / "backup.tar.gz"
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({name: hashlib.sha256(data).hexdigest()}))
        with tarfile.open(archive, "w:gz") as tar:
            entry = tarfile.TarInfo(name)
            entry.type = kind
            entry.size = len(data) if kind == tarfile.REGTYPE else 0
            tar.addfile(entry, io.BytesIO(data) if kind == tarfile.REGTYPE else None)
        return archive, manifest

    def test_izole_geri_yukleme_harici_kanit_degildir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            result = verify_archive(archive, manifest)
            self.assertTrue(result["supplied_archive_integrity_verified"])
            self.assertFalse(result["external_backup_verified"])
            self.assertFalse(result["historical_recovery_verified"])
            self.assertFalse(result["production_modified"])

    def test_bozuk_ozet_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            manifest.write_text(json.dumps({"safe/file.txt": "0" * 64}))
            with self.assertRaisesRegex(ValueError, "SHA256"):
                verify_archive(archive, manifest)

    def test_dizin_asimi_ve_sembolik_baglanti_reddedilir(self):
        for name in ("../escape", "/absolute", "a/../escape", "a\\escape"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                archive, manifest = self.create_case(Path(folder), name=name)
                with self.assertRaises(ValueError):
                    verify_archive(archive, manifest)
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder), kind=tarfile.SYMTYPE)
            with self.assertRaisesRegex(ValueError, "Unsafe archive member"):
                verify_archive(archive, manifest)

    def test_beklenmeyen_ve_eksik_dosya_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            manifest.write_text(json.dumps({"different.txt": hashlib.sha256(b"protected sample").hexdigest()}))
            with self.assertRaisesRegex(ValueError, "Archive differs"):
                verify_archive(archive, manifest)
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            manifest.write_text(json.dumps({
                "safe/file.txt": hashlib.sha256(b"protected sample").hexdigest(),
                "missing.txt": hashlib.sha256(b"").hexdigest(),
            }))
            with self.assertRaisesRegex(ValueError, "Archive differs"):
                verify_archive(archive, manifest)

    def test_cift_tar_uyesi_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive, manifest = self.create_case(root)
            with tarfile.open(archive, "w:gz") as tar:
                for _ in range(2):
                    entry = tarfile.TarInfo("safe/file.txt")
                    entry.size = len(b"protected sample")
                    tar.addfile(entry, io.BytesIO(b"protected sample"))
            with self.assertRaisesRegex(ValueError, "Archive differs"):
                verify_archive(archive, manifest)

    def test_buyuk_manifest_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            manifest.write_bytes(b" " * (2 * 1024 * 1024 + 1))
            with self.assertRaisesRegex(ValueError, "Manifest exceeds size limit"):
                verify_archive(archive, manifest)

    def test_manifest_cift_anahtar_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            digest = hashlib.sha256(b"protected sample").hexdigest()
            manifest.write_text('{"safe/file.txt":"' + digest + '","safe/file.txt":"' + digest + '"}')
            with self.assertRaisesRegex(ValueError, "Duplicate manifest entry"):
                verify_archive(archive, manifest)

    def test_nul_karakterli_yol_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            manifest.write_text(json.dumps({"safe/\\u0000file.txt": "0" * 64}))
            with self.assertRaisesRegex(ValueError, "Unsafe manifest entry"):
                verify_archive(archive, manifest)

    def test_dosya_klasor_cakismasi_reddedilir(self):
        with tempfile.TemporaryDirectory() as folder:
            archive, manifest = self.create_case(Path(folder))
            manifest.write_text(json.dumps({
                "safe": hashlib.sha256(b"protected sample").hexdigest(),
                "safe/file.txt": hashlib.sha256(b"protected sample").hexdigest(),
            }))
            with self.assertRaisesRegex(ValueError, "path collision"):
                verify_archive(archive, manifest)

if __name__ == "__main__":
    unittest.main()
