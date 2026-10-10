#!/usr/bin/env python3
"""Read-only disaster recovery rehearsal: restore backup playlists into a temporary directory."""
import hashlib
import json
import tempfile
from pathlib import Path

BACKUPS = (
    Path("yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u"),
    Path("yedekler/ADAY_KANALLAR_2026-10-09.txt"),
)
PROTECTED = (Path("CALISANLAR.m3u"), Path("YENILER.m3u"))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def parse_playlist(data):
    text = data.decode("utf-8-sig")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or lines[0] != "#EXTM3U":
        raise ValueError("Missing #EXTM3U header")
    channels = []
    index = 1
    while index < len(lines):
        metadata = lines[index]
        if not metadata.startswith("#EXTINF:"):
            raise ValueError(f"Unexpected line {index+1}")
        if index + 1 >= len(lines) or not lines[index+1].startswith(("http://", "https://")):
            raise ValueError(f"Missing/invalid URL after line {index+1}")
        channels.append((metadata, lines[index+1]))
        index += 2
    if not channels:
        raise ValueError("No channels to restore")
    return channels

def main():
    snapshots = {str(p):sha(p.read_bytes()) for p in PROTECTED}
    result = {"status":"FAIL","backups":[],"negative_test":"NOT_RUN","protected_unchanged":False,
              "scope":"Restore backup files to temporary directory only; no replacement of protected playlists"}
    with tempfile.TemporaryDirectory(prefix="madsc-restore-") as folder:
        dest = Path(folder)
        for source in BACKUPS:
            original = source.read_bytes()
            channels = parse_playlist(original)
            # Actual recovery from a backup file into a clean, temporary destination.
            restored = dest / source.name
            restored.write_bytes(original)
            recovered = restored.read_bytes()
            assert sha(recovered) == sha(original), f"Restore checksum mismatch: {source}"
            assert parse_playlist(recovered) == channels, f"Restore channel mismatch: {source}"
            result["backups"].append({"source":str(source),"restored_to":"temporary sandbox",
                "channels":len(channels),"sha256":sha(original),"byte_identical":True})
        try:
            parse_playlist(b"#EXTM3U\n#EXTINF:-1,Broken channel\n")
        except ValueError:
            result["negative_test"] = "PASS: corrupt backup rejected"
        else:
            raise AssertionError("Corrupt backup incorrectly accepted")
    result["protected_unchanged"] = all(sha(p.read_bytes()) == snapshots[str(p)] for p in PROTECTED)
    assert result["protected_unchanged"], "Protected playlists changed"
    result["status"] = "PASS"
    Path("RESTORE-DRY-RUN-REPORT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
