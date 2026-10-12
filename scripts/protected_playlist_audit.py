"""Read-only security audit of protected IPTV playlist files.

This checks file existence and playlist syntax. It is NOT an approval gate:
branch rules are needed to prevent unauthorized merges.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = ("CALISANLAR.m3u", "YENILER.m3u")

def main():
    for name in PROTECTED:
        path = ROOT / name
        if not path.is_file():
            raise SystemExit(f"FAIL: protected playlist missing: {name}")
        with path.open("rb") as handle:
            header = handle.readline().strip()
        if not header.startswith(b"#EXTM3U"):
            raise SystemExit(f"FAIL: invalid M3U header: {name}")
        print(f"PASS: {name} exists and has M3U header (no changes made)")
    policy = ROOT / "AGENTS.md"
    if not policy.is_file():
        raise SystemExit("FAIL: AGENTS.md protection policy missing")
    print("PASS: protection policy present; CI is read-only, not an authorization gate")

if __name__ == "__main__":
    main()
