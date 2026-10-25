#!/usr/bin/env python3
"""K4: Verify a supplied TAR backup safely in a temporary directory.

A successful local test is NOT proof of offsite storage or historical recovery.
"""
import argparse
import hashlib
import json
import re
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

MAX_FILES = 10000
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024
MAX_FILE_BYTES = 512 * 1024 * 1024

def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name:
        return False
    p = PurePosixPath(name)
    return not p.is_absolute() and all(part not in (".", "..") for part in name.split("/")) and bool(p.parts)

def verify_archive(archive, manifest):
    expected = json.loads(Path(manifest).read_text(encoding="utf-8"))
    if not isinstance(expected, dict) or not expected or len(expected) > MAX_FILES:
        raise ValueError("Invalid manifest size")
    for name, digest in expected.items():
        if not safe_name(name) or not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("Unsafe manifest entry")
    with tempfile.TemporaryDirectory(prefix="madsc-k4-restore-") as tmp:
        with tarfile.open(archive, "r:*") as tar:
            members = tar.getmembers()
            names = [m.name for m in members]
            if len(members) > MAX_FILES or len(names) != len(set(names)) or set(names) != set(expected):
                raise ValueError("Archive differs from manifest")
            total = 0
            for member in members:
                if not member.isfile() or not safe_name(member.name) or member.size < 0 or member.size > MAX_FILE_BYTES:
                    raise ValueError("Unsafe archive member")
                total += member.size
                if total > MAX_TOTAL_BYTES:
                    raise ValueError("Archive exceeds size limit")
            for member in members:
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError("Unreadable archive member")
                destination = Path(tmp).joinpath(*PurePosixPath(member.name).parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                copied = 0
                with destination.open("wb") as output:
                    while block := source.read(min(1024 * 1024, member.size - copied + 1)):
                        copied += len(block)
                        if copied > member.size:
                            raise ValueError("Archive member exceeds declared size")
                        digest.update(block)
                        output.write(block)
                if copied != member.size or digest.hexdigest() != expected[member.name]:
                    raise ValueError("SHA256 or size mismatch: " + member.name)
        return {"status": "PASS", "verified_files": len(expected),
                "supplied_archive_integrity_verified": True,
                "external_backup_verified": False,
                "historical_recovery_verified": False,
                "production_modified": False,
                "limitations": "Archive provenance, independent storage, historical age and production recovery remain unverified"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("manifest")
    args = parser.parse_args()
    print(json.dumps(verify_archive(args.archive, args.manifest), ensure_ascii=False))

if __name__ == "__main__":
    main()
