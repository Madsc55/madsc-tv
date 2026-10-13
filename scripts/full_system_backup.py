#!/usr/bin/env python3
"""Create and verify one restorable snapshot of every tracked repository file."""
import hashlib
import io
import json
import pathlib
import subprocess
import tarfile
import tempfile

ROOT = pathlib.Path(".")
OUTPUT = pathlib.Path("MADSC-TUM-SISTEM-YEDEK.tar.gz")
REPORT = pathlib.Path("MADSC-TUM-SISTEM-YEDEK-RAPORU.json")
MAX_BYTES = 400 * 1024 * 1024

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    paths = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    paths = sorted(p for p in paths if p)
    settings = pathlib.Path("MADSC-SISTEM-AYAR-ENVANTERI.json")
    if settings.is_file():
        paths.append(settings.name)
    if not paths:
        raise RuntimeError("Takip edilen dosya yok")
    manifest = {}
    total = 0
    with tarfile.open(OUTPUT, "w:gz") as archive:
        for name in paths:
            path = ROOT / name
            if not path.is_file() or path.is_symlink():
                raise RuntimeError(f"Dosya eksik veya sembolik bag: {name}")
            data = path.read_bytes()
            total += len(data)
            if total > MAX_BYTES:
                raise RuntimeError("Yedek boyut siniri asildi; eksik arsiv kabul edilmez")
            manifest[name] = {"sha256": digest(data), "bytes": len(data)}
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            entry.mode = 0o600
            archive.addfile(entry, io.BytesIO(data))
        metadata = json.dumps(manifest, ensure_ascii=False, sort_keys=True).encode()
        entry = tarfile.TarInfo("_MADSC_YEDEK_MANIFEST.json")
        entry.size = len(metadata)
        archive.addfile(entry, io.BytesIO(metadata))
    # Restore to an isolated directory and compare every file byte for byte.
    with tempfile.TemporaryDirectory(prefix="madsc-full-restore-") as folder:
        destination = pathlib.Path(folder)
        with tarfile.open(OUTPUT, "r:gz") as archive:
            members = archive.getmembers()
            if sorted(m.name for m in members) != sorted([*paths, "_MADSC_YEDEK_MANIFEST.json"]):
                raise RuntimeError("Yedek icerigi eksik veya fazla")
            for member in members:
                if not member.isfile() or pathlib.PurePosixPath(member.name).is_absolute() or ".." in pathlib.PurePosixPath(member.name).parts:
                    raise RuntimeError("Guvenli olmayan arsiv girdisi")
                target = destination / member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source:
                    target.write_bytes(source.read())
        restored = json.loads((destination / "_MADSC_YEDEK_MANIFEST.json").read_text())
        if restored != manifest:
            raise RuntimeError("Manifest eslesmedi")
        for name, item in manifest.items():
            if digest((destination / name).read_bytes()) != item["sha256"]:
                raise RuntimeError(f"Geri yukleme dogrulamasi basarisiz: {name}")
    REPORT.write_text(json.dumps({
        "status": "PASS", "file_count": len(manifest), "bytes": total,
        "archive_sha256": digest(OUTPUT.read_bytes()),
        "verified": "Full restore to temporary directory; all tracked files byte-identical",
        "limitations": ["Only Git-tracked files are included", "GitHub artifact retention is limited",
                        "No automatic overwrite of live files", "No independent long-term offsite backup"]
    }, ensure_ascii=False, indent=2))
    print(REPORT.read_text())

if __name__ == "__main__":
    main()
