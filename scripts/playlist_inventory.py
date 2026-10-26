#!/usr/bin/env python3
"""Read-only M3U playlist inventory. Does not rewrite playlists."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAYLISTS = ("CALISANLAR.m3u", "YENILER.m3u")
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
IMPORTANT = ("TRT 1", "DHA CANLI")
GROUPS = ("⭐ FAVORİLER", "📦 YEDEKLER")


def analyze(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    result = {
        "file": path.name, "exists": True, "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data), "header_valid": bool(lines and lines[0].strip().startswith("#EXTM3U")),
        "channels": 0, "groups": {}, "duplicate_urls": [],
        "important_channels": {name: [] for name in IMPORTANT},
        "protected_groups": {name: 0 for name in GROUPS},
        "invalid_entries": [], "unpaired_metadata": 0,
    }
    categories = collections.Counter()
    seen = {}
    pending = None
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if line.startswith("#EXTINF:"):
            if pending is not None:
                result["unpaired_metadata"] += 1
            attrs = dict(ATTR.findall(line))
            title = line.split(",", 1)[1].strip() if "," in line else ""
            pending = (number, attrs, title)
        elif line and not line.startswith("#"):
            if pending is None:
                result["invalid_entries"].append({"line": number, "reason": "URL without EXTINF"})
                continue
            meta_line, attrs, title = pending
            group = attrs.get("group-title", "GRUPSUZ")
            categories[group] += 1
            result["channels"] += 1
            if line in seen:
                result["duplicate_urls"].append({
                    "line": number, "first_line": seen[line], "group": group, "title": title
                })
            else:
                seen[line] = number
            for group_name in GROUPS:
                if group_name.casefold() in group.casefold():
                    result["protected_groups"][group_name] += 1
            for name in IMPORTANT:
                if name.casefold() in title.casefold():
                    result["important_channels"][name].append({
                        "line": meta_line, "title": title, "group": group
                    })
            pending = None
    if pending is not None:
        result["unpaired_metadata"] += 1
    result["groups"] = dict(sorted(categories.items()))
    result["duplicate_url_count"] = len(result["duplicate_urls"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="playlist_inventory.json")
    args = parser.parse_args()
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "playlists": [],
    }
    for name in PLAYLISTS:
        path = ROOT / name
        report["playlists"].append(analyze(path) if path.is_file() else {
            "file": name, "exists": False
        })
    dest = pathlib.Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in report["playlists"]:
        print(f"{item['file']}: {item.get('channels', 'MISSING')} channels")
    print(f"Inventory: {dest}")


if __name__ == "__main__":
    main()
