#!/usr/bin/env python3
"""Enforce user-approved visible IPTV categories without modifying playlists."""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = ("CALISANLAR.m3u", "YENILER.m3u")
FORBIDDEN = ("TEST BEKLEYEN", "TEST BEKLEYENLER", "YABANCILAR", "ÇALIŞMAYANLAR")
ALLOWED_PREFIXES = (
    "⭐ FAVORİLER", "📦 YEDEKLER", "📺 HEPSİ", "🎬 SİNEMA",
    "📺 HABER", "🇹🇷 ULUSAL", "⚽️ SPOR", "🌍 BELGESEL",
    "🧸 ÇOCUK", "🎧 MÜZİK", "📍 YEREL", "🕌 DİNİ",
)
ATTR = re.compile(r'group-title="([^"]*)"')


def audit(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {"file": path.name, "ok": False, "error": "missing file"}
    violations = []
    counts = {}
    for number, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
        if not line.startswith("#EXTINF:"):
            continue
        match = ATTR.search(line)
        group = match.group(1).strip() if match else ""
        counts[group] = counts.get(group, 0) + 1
        upper = group.upper()
        if any(term in upper for term in FORBIDDEN):
            violations.append({"line": number, "group": group, "reason": "forbidden"})
        elif path.name == "CALISANLAR.m3u" and not any(
            group.startswith(prefix) for prefix in ALLOWED_PREFIXES
        ):
            violations.append({"line": number, "group": group, "reason": "unapproved category"})
        elif path.name == "YENILER.m3u" and group != "YENILER":
            violations.append({"line": number, "group": group, "reason": "unexpected staging category"})
    return {"file": path.name, "ok": not violations, "categories": counts, "violations": violations}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, help="Optional JSON audit path")
    args = parser.parse_args()
    results = [audit(ROOT / name) for name in FILES]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in results:
        print(f"{'PASS' if item['ok'] else 'FAIL'}: {item['file']}")
        for violation in item.get("violations", []):
            print(f"  line {violation['line']}: {violation['group']} ({violation['reason']})")
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
