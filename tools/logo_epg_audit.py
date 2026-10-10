"""Read-only M3U logo and EPG identity quality checks."""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ATTR = re.compile(r'([\w-]+)="([^"]*)"')

def audit(text):
    channels = []
    for line in text.splitlines():
        if not line.startswith("#EXTINF:"):
            continue
        metadata, _, name = line.partition(",")
        attrs = dict(ATTR.findall(metadata))
        channels.append({"name": name.strip(), "tvg_id": attrs.get("tvg-id", "").strip(), "logo": attrs.get("tvg-logo", "").strip()})
    ids = defaultdict(list)
    warnings = []
    for ch in channels:
        if ch["tvg_id"]:
            ids[ch["tvg_id"].casefold()].append(ch["name"])
        else:
            warnings.append({"type": "missing_tvg_id", "channel": ch["name"]})
        if not ch["logo"]:
            warnings.append({"type": "missing_logo", "channel": ch["name"]})
        elif not ch["logo"].lower().startswith(("https://", "http://")):
            warnings.append({"type": "suspicious_logo_url", "channel": ch["name"]})
    for key, names in sorted(ids.items()):
        if len(names) > 1:
            warnings.append({"type": "duplicate_tvg_id", "tvg_id": key, "channels": names})
    return {"channels_checked": len(channels), "warnings": warnings}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist", nargs="?", default="CALISANLAR.m3u")
    args = parser.parse_args()
    print(json.dumps(audit(Path(args.playlist).read_text(encoding="utf-8-sig")), ensure_ascii=False, indent=2))
