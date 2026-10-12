#!/usr/bin/env python3
"""Read-only source inventory audit; no stream tests or playlist edits."""
import ast
import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path

tree = ast.parse(Path("madsc_akilli_kesif.py").read_text(encoding="utf-8"))
sources = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SOURCES" for t in node.targets):
        sources = ast.literal_eval(node.value)
        break
daily = {"iptv-turk-tr-EK-KAYNAK","iptv-org-TR","iptv-org-TURKIYE","iptv-org-TURKCE","omerdenizhan-TR","ilyswch-TR","itasli-TR","gkhncksn-TR","Lunedor-TR","dearbulut-TR","dearbulut-TURKCE"}
report_path = Path("madsc_kesif/kaynak_erisim_raporu.csv")
rows = []
if report_path.exists():
    rows = list(csv.DictReader(io.StringIO(report_path.read_text(encoding="utf-8-sig"))))
status = {r["kaynak"]: r for r in rows}
report = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "mode": "READ_ONLY_INVENTORY",
    "configured_sources": len(sources),
    "daily_sources": len(daily & sources.keys()),
    "not_in_daily_scan": len(sources.keys() - daily),
    "last_daily_source_status": [{"name": name, "status": status.get(name, {}).get("durum", "NOT_CHECKED"), "channels": status.get(name, {}).get("kanal_sayisi", "")} for name in sorted(daily & sources.keys())],
    "sources_outside_daily": sorted(sources.keys() - daily),
    "warning": "This audit does not fetch the 144 extra feeds, identify channels, or perform playback tests."
}
print(json.dumps(report, ensure_ascii=False, indent=2))
