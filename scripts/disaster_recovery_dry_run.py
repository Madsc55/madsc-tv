#!/usr/bin/env python3
"""Simulate disaster and restore tracked protected playlists from a Git commit in isolation."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

FILES = ("CALISANLAR.m3u", "YENILER.m3u")

def git_bytes(path):
    return subprocess.check_output(["git", "show", f"HEAD:{path}"])

def checksum(data):
    return hashlib.sha256(data).hexdigest()

def validate(data):
    lines = data.decode("utf-8-sig").splitlines()
    if not lines or not lines[0].strip().startswith("#EXTM3U"):
        raise ValueError("Invalid M3U header")
    channel_count = sum(line.startswith("#EXTINF:") for line in lines)
    if channel_count < 1:
        raise ValueError("No channels")
    return channel_count

def main():
    results = []
    with tempfile.TemporaryDirectory(prefix="madsc-disaster-recovery-") as tmp:
        for name in FILES:
            original = Path(name).read_bytes()
            snapshot = git_bytes(name)
            if original != snapshot:
                raise AssertionError(f"Working tree differs from committed snapshot: {name}")
            before_count = validate(snapshot)
            recovery = Path(tmp) / name
            recovery.write_bytes(b"CORRUPTED\n#EXTINF:-1,Lost\n")
            try:
                validate(recovery.read_bytes())
            except ValueError:
                pass
            else:
                raise AssertionError("Corruption was not detected")
            recovery.write_bytes(snapshot)
            restored = recovery.read_bytes()
            assert restored == snapshot == original, f"Restore mismatch: {name}"
            assert validate(restored) == before_count
            assert Path(name).read_bytes() == original, f"Original changed: {name}"
            results.append({"file":name,"channels":before_count,"source":"Git HEAD committed snapshot",
                            "simulated_damage":"detected","restore":"PASS","sha256":checksum(restored),
                            "original_untouched":True})
    report={"status":"PASS","files":results,
            "scope":"Temporary simulated corruption and full-byte restore of both protected playlists",
            "limitations":["Git commit history is not an independent offsite backup",
                           "No destructive restore of the actual repository was performed",
                           "This does not verify IBO Player playback or restore untracked files"]}
    Path("DISASTER-RECOVERY-REPORT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
