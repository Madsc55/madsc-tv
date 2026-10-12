#!/usr/bin/env python3
"""Read-only M3U/XMLTV identity audit. Never changes playlists, EPG or workflows."""
import argparse
import collections
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTR = re.compile(r'([\w-]+)="([^"]*)"')

def inspect(playlist, xmltv):
    raw = playlist.read_text(encoding="utf-8-sig")
    entries = []
    for line in raw.splitlines():
        if not line.startswith("#EXTINF"):
            continue
        attrs = dict(ATTR.findall(line))
        entries.append({"name": line.rsplit(",", 1)[-1].strip(),
                        "tvg_id": attrs.get("tvg-id", "").strip()})
    tree = ET.parse(xmltv)
    root = tree.getroot()
    if root.tag != "tv":
        raise ValueError("XMLTV root is not <tv>")
    guide_ids = {ch.get("id") for ch in root.findall("channel") if ch.get("id")}
    programme_counts = collections.Counter(p.get("channel") for p in root.findall("programme"))
    used = collections.Counter(e["tvg_id"] for e in entries if e["tvg_id"])
    missing_id = [e["name"] for e in entries if not e["tvg_id"]]
    unmatched = [e for e in entries if e["tvg_id"] and e["tvg_id"] not in guide_ids]
    no_programme = [e for e in entries if e["tvg_id"] in guide_ids and not programme_counts[e["tvg_id"]]]
    matching = [e for e in entries if e["tvg_id"] in guide_ids and programme_counts[e["tvg_id"]]]
    return {
        "playlist_entries": len(entries),
        "unique_nonempty_tvg_ids": len(used),
        "blank_tvg_id_count": len(missing_id),
        "xmltv_channels": len(guide_ids),
        "xmltv_programmes": sum(programme_counts.values()),
        "matching_entries_with_programmes": len(matching),
        "unmatched_nonempty_tvg_id_count": len(unmatched),
        "matched_id_without_programmes_count": len(no_programme),
        "blank_tvg_id_names": missing_id,
        "unmatched_nonempty_tvg_id_entries": unmatched,
        "matched_id_without_programmes_entries": no_programme,
        "shared_tvg_ids": [{"id": k, "entries": v} for k, v in sorted(used.items()) if v > 1],
        "note": "Shared IDs can be legitimate quality variants. Blank IDs do not prove EPG failure. This is not a device playback test."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--playlist", type=Path, default=ROOT / "CALISANLAR.m3u")
    parser.add_argument("--xmltv", type=Path, default=ROOT / "epg/madsc-epg.xml")
    parser.add_argument("--output", type=Path, help="Optional new report file; never write to input paths")
    args = parser.parse_args()
    result = inspect(args.playlist, args.xmltv)
    report = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        resolved = args.output.resolve()
        if resolved in (args.playlist.resolve(), args.xmltv.resolve()):
            parser.error("Output must not overwrite an input")
        if resolved.exists():
            parser.error("Output already exists; refusing to overwrite")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

if __name__ == "__main__":
    main()
