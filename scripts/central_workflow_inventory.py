#!/usr/bin/env python3
"""Salt okunur GitHub Actions envanteri; hiçbir iş akışını tetiklemez."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
items = []
for path in sorted((root / ".github/workflows").glob("*")):
    if path.suffix not in (".yml", ".yaml"):
        continue
    raw = path.read_text(encoding="utf-8")
    cron = re.findall(r"^\s*-\s*cron:\s*['\"]?([^'\"\n#]+)", raw, re.M)
    items.append({
        "file": path.name,
        "name": next((x.strip().strip("'\"") for x in re.findall(r"^name:\s*(.+)$", raw, re.M)), path.name),
        "schedule_utc": [x.strip() for x in cron],
        "manual": bool(re.search(r"^\s*workflow_dispatch\s*:", raw, re.M)),
        "push": bool(re.search(r"^\s*push\s*:", raw, re.M)),
        "workflow_run": bool(re.search(r"^\s*workflow_run\s*:", raw, re.M)),
        "writes_contents": bool(re.search(r"^\s*contents:\s*write\s*$", raw, re.M)),
        "has_concurrency": bool(re.search(r"^concurrency\s*:", raw, re.M)),
    })
out = root / "madsc_merkezi_denetim"
out.mkdir(exist_ok=True)
(out / "otomasyon_haritasi.json").write_text(
    json.dumps({"workflow_count": len(items), "scheduled_count": sum(bool(x["schedule_utc"]) for x in items),
                "workflows": items, "note": "Statik envanterdir; etkinlik, başarı ve çakışma kanıtı değildir."},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(items)} workflow envantere alındı; hiçbiri değiştirilmedi veya tetiklenmedi.")
