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

MAX_MANIFEST_BYTES = 2 * 1024 * 1024
MAX_FILES = 10000
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024
MAX_FILE_BYTES = 512 * 1024 * 1024

def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name:
        return False
    p = PurePosixPath(name)
    return not p.is_absolute() and all(part not in (".", "..") for part in name.split("/")) and bool(p.parts)

def reject_duplicate_manifest_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate manifest entry: " + key)
        result[key] = value
    return result

def verify_archive(archive, manifest):
    manifest_path = Path(manifest)
    if manifest_path.stat().st_size > MAX_MANIFEST_BYTES:
        raise ValueError("Manifest exceeds size limit")
    expected = json.loads(manifest_path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_manifest_keys)
    if not isinstance(expected, dict) or not expected or len(expected) > MAX_FILES:
        raise ValueError("Invalid manifest size")
    for name, digest in expected.items():
        if not safe_name(name) or not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("Unsafe manifest entry")
    # Streaming avoids materializing attacker-controlled TAR headers in memory.
    with tempfile.TemporaryDirectory(prefix="madsc-k4-restore-") as tmp:
        seen = set()
        total = 0
        with tarfile.open(archive, "r|*") as tar:
            for member in tar:
                name = member.name
                if not safe_name(name) or name not in expected or name in seen:
                    raise ValueError("Archive differs from manifest")
                if len(seen) >= MAX_FILES or not member.isfile() or member.size < 0 or member.size > MAX_FILE_BYTES:
                    raise ValueError("Unsafe archive member")
                seen.add(name)
                total += member.size
                if total > MAX_TOTAL_BYTES:
                    raise ValueError("Archive exceeds size limit")
                source = tar.extractfile(member)
                if source is None:
                    raise ValueError("Unreadable archive member")
                destination = Path(tmp).joinpath(*PurePosixPath(name).parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                copied = 0
                with source, destination.open("wb") as output:
                    while copied < member.size:
                        block = source.read(min(1024 * 1024, member.size - copied))
                        if not block:
                            raise ValueError("Archive member truncated")
                        copied += len(block)
                        digest.update(block)
                        output.write(block)
                if digest.hexdigest() != expected[name]:
                    raise ValueError("SHA256 or size mismatch: " + name)
        if seen != set(expected):
            raise ValueError("Archive differs from manifest")
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
