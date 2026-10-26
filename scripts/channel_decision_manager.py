#!/usr/bin/env python3
"""User-directed IPTV decisions; default mode is preview, never auto-promotes.

Only explicit user commands may change the visible playlist. Failed/foreign/test
records remain outside visible categories. Backups are the sole testing category.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
VISIBLE = ROOT / "CALISANLAR.m3u"
ATTR = re.compile(r'group-title="([^"]*)"')
FORBIDDEN = ("TEST BEKLEYEN", "YABANCILAR", "ÇALIŞMAYANLAR")
BACKUP = "📦 YEDEKLER"
PROTECTED = ("⭐ FAVORİLER", "TRT 1", "DHA CANLI")


def entries(text):
    lines = text.splitlines(keepends=True)
    result = []
    pending = None
    for index, line in enumerate(lines):
        if line.startswith("#EXTINF:"):
            pending = index
        elif pending is not None and line.strip() and not line.startswith("#"):
            meta = lines[pending]
            match = ATTR.search(meta)
            result.append({"start": pending, "end": index, "title": meta.split(",", 1)[-1].strip(),
                           "url": line.strip(), "group": match.group(1) if match else ""})
            pending = None
    return lines, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Exact URL identifying the channel")
    parser.add_argument("--action", required=True, choices=("inspect", "working", "not-working", "remove", "backup", "assign"))
    parser.add_argument("--category", help="Existing category, required for assign")
    parser.add_argument("--apply", action="store_true", help="Request local playlist change")
    parser.add_argument("--written-approval", help="Exact written approval: ONAYLIYORUM:<action>:<url>")
    args = parser.parse_args()
    if not VISIBLE.exists():
        parser.error(f"Missing {VISIBLE}")
    original = VISIBLE.read_bytes()
    text = original.decode("utf-8-sig")
    lines, records = entries(text)
    found = [r for r in records if r["url"] == args.url]
    if len(found) != 1:
        parser.error(f"Expected exactly one URL match; found {len(found)}")
    record = found[0]
    action = args.action
    category = args.category
    existing = sorted({r["group"] for r in records})
    if action == "assign":
        if not category or category not in existing or any(x in category.upper() for x in FORBIDDEN):
            parser.error("Assignment requires an existing, approved category")
    if action in ("remove", "not-working") and (record["group"].startswith("⭐ FAVORİLER") or
            any(x in record["title"].upper() for x in ("TRT 1", "DHA CANLI"))):
        parser.error("Protected channel: manual special approval required")
    if action in ("working", "inspect"):
        message = "Recorded as user statement only; no automatic category changes"
    elif action in ("remove", "not-working"):
        message = "Remove selected channel from visible playlist; keep source archives unchanged"
    else:
        message = f"Assign selected channel to {BACKUP if action == 'backup' else category}"
    print(json.dumps({"action": action, "channel": record["title"], "current_group": record["group"],
                      "proposal": message, "apply": args.apply}, ensure_ascii=False, indent=2))
    if args.apply and action not in ("working", "inspect") and args.written_approval != f"ONAYLIYORUM:{action}:{args.url}":
        parser.error("DENIED: exact written user approval required; --apply alone is insufficient")
    if not args.apply or action in ("working", "inspect"):
        return 0
    if action in ("remove", "not-working"):
        del lines[record["start"]:record["end"] + 1]
    else:
        destination = next((g for g in existing if g.startswith(BACKUP)), None) if action == "backup" else category
        if not destination:
            parser.error("Backup group missing; refusing to create a new category")
        start = record["start"]
        meta = lines[start]
        if not ATTR.search(meta):
            parser.error("Channel has no group-title; refusing unsafe rewrite")
        lines[start] = ATTR.sub(lambda m: 'group-title="' + destination + '"', meta, count=1)
    output = "".join(lines).encode("utf-8")
    if hashlib.sha256(original).digest() == hashlib.sha256(output).digest():
        print("No change required")
        return 0
    VISIBLE.write_bytes(output)
    print("Updated visible playlist locally; no other files modified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
