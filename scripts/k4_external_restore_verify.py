#!/usr/bin/env python3
"""K4: Verify an independent backup archive in an isolated temporary directory.

Never writes into the repository or restores over production files.
"""
import argparse
import hashlib
import json
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

def verify_archive(archive, manifest):
    archive = Path(archive)
    manifest = Path(manifest)
    expected = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(expected, dict) or not expected:
        raise ValueError("Manifest must be a nonempty path-to-SHA256 mapping")
    for name, digest in expected.items():
        p = PurePosixPath(name)
        if (not isinstance(name, str) or p.is_absolute() or
            any(part in ("..", ".") for part in p.parts) or
            not isinstance(digest, str) or len(digest) != 64 or
            any(c not in "0123456789abcdef" for c in digest)):
            raise ValueError("Unsafe manifest entry")
    with tempfile.TemporaryDirectory(prefix="madsc-k4-restore-") as tmp:
        with tarfile.open(archive, "r:*") as tar:
            members = tar.getmembers()
            names = [m.name for m in members]
            if len(names) != len(set(names)) or set(names) != set(expected):
                raise ValueError("Archive files differ from manifest")
            for member in members:
                p = PurePosixPath(member.name)
                if not member.isfile() or p.is_absolute() or any(x in (".", "..") for x in p.parts):
                    raise ValueError("Unsafe archive member")
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError("Unreadable archive member")
                destination = Path(tmp).joinpath(*p.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                h = hashlib.sha256()
                with destination.open("wb") as output:
                    while block := source.read(1024 * 1024):
                        h.update(block)
                        output.write(block)
                if h.hexdigest() != expected[member.name]:
                    raise ValueError("SHA256 mismatch: " + member.name)
        return {"status": "PASS", "verified_files": len(expected),
                "external_backup_verified": True,
                "production_modified": False,
                "scope": "Supplied independent archive only; provenance and remote storage not established"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("manifest")
    args = parser.parse_args()
    print(json.dumps(verify_archive(args.archive, args.manifest), ensure_ascii=False))

if __name__ == "__main__":
    main()
