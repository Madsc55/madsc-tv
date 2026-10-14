#!/usr/bin/env python3
"""Read-only XMLTV readiness check. Never claims IBO Player device success."""
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPG = ROOT / "epg"
TARGETS = {
    "af0zo9et4xguwsk": "TRT 1",
    "nzdc0yd5xxv43yl": "TRT 2",
    "pvr08e5grfsebfw": "SHOW TV",
    "2zkzbuscxwyjc4k": "ATV",
    "bbwgmhsmhhoatzg": "KANAL D",
}

def inspect(main_path, pilot_path, report_path):
    report = json.loads(report_path.read_text(encoding="utf-8"))
    full = ET.parse(main_path).getroot()
    pilot = ET.parse(pilot_path).getroot()
    if full.tag != "tv" or pilot.tag != "tv":
        raise ValueError("Invalid XMLTV root")
    full_ids = {x.get("id") for x in full.findall("channel")}
    pilot_ids = {x.get("id") for x in pilot.findall("channel")}
    full_counts = {cid: 0 for cid in TARGETS}
    pilot_counts = {cid: 0 for cid in TARGETS}
    for item in full.findall("programme"):
        cid = item.get("channel")
        if cid in full_counts:
            full_counts[cid] += 1
    for item in pilot.findall("programme"):
        cid = item.get("channel")
        if cid in pilot_counts:
            pilot_counts[cid] += 1
    source_status = [{"url": row.get("url"), "status": row.get("status")}
                     for row in report.get("sources", [])]
    ready = (pilot_ids == set(TARGETS) and set(TARGETS) <= full_ids
             and all(full_counts[cid] and pilot_counts[cid] for cid in TARGETS)
             and report.get("programmes", 0) > 0)
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "technical_xmltv_ready": bool(ready),
        "tv_ibo_player_verified": False,
        "sweden_device_verified": False,
        "status": "TV_KONTROLU_BEKLIYOR" if ready else "TEKNIK_HAZIRLIK_EKSIK",
        "full_xmltv_channels": len(full_ids),
        "full_xmltv_programmes": len(full.findall("programme")),
        "playlist_entries": report.get("playlist_entries"),
        "matched_playlist_entries": report.get("matched_entries"),
        "usable_playlist_entries": report.get("usable_playlist_entries"),
        "pilot_channels": [{"name": TARGETS[cid], "id": cid,
                            "full_programmes": full_counts[cid],
                            "pilot_programmes": pilot_counts[cid]}
                           for cid in TARGETS],
        "sources": source_status,
        "device_check": "IBO Player televizyonunda XMLTV URL ekle, yenile, 5 pilot kanalda program akisini kontrol et; kullanici onayi beklenir.",
        "protected_playlist_modified": False,
    }

def main():
    result = inspect(EPG / "madsc-epg.xml", EPG / "ibo-test-epg.xml", EPG / "report.json")
    dest = EPG / "tv_kontrol_bekliyor.json"
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "pilot": result["pilot_channels"]}, ensure_ascii=False))
    if not result["technical_xmltv_ready"]:
        raise SystemExit("EPG XMLTV pilot is not technically ready; device approval not given")

if __name__ == "__main__":
    main()
