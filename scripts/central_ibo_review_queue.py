#!/usr/bin/env python3
"""Adaylari IBO onayi icin ayri, salt okunur CSV ve ozet halinde hazirla."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)
INPUT = ROOT / "madsc_kesif/candidate_epg_logo_join.json"
FIELDS = ("channel", "stream_sha256", "channel_id", "epg_pilot_status", "logo_status",
          "logo_visual_match", "broadcast_status", "sweden_ibo_status",
          "user_decision", "ready_for_playlist")

def prepare(raw):
    if not isinstance(raw, dict) or not isinstance(raw.get("candidate_results"), list):
        return [], "KAYNAK_KANITI_YOK"
    rows = []
    seen = set()
    for item in raw["candidate_results"]:
        if not isinstance(item, dict):
            continue
        digest = str(item.get("stream_sha256") or "").strip()
        channel = str(item.get("channel") or "").strip()
        # Kimlik kaniti olmayan farkli adaylari tek kayda indirme.
        # Yalniz dolu SHA256 ile ayni kanal tekrarlarini ayikla.
        key = (digest, channel) if digest else None
        if key is not None and key in seen:
            continue
        if key is not None:
            seen.add(key)
        rows.append({
            "channel": channel, "stream_sha256": digest,
            "channel_id": str(item.get("channel_id") or ""),
            "epg_pilot_status": str(item.get("epg_pilot_status") or "KANIT_YOK"),
            "logo_status": str(item.get("logo_status") or "KANIT_YOK"),
            "logo_visual_match": str(item.get("logo_visual_match") or "NOT_VERIFIED"),
            "broadcast_status": str(item.get("broadcast_status") or "NOT_VERIFIED"),
            "sweden_ibo_status": "NOT_DEVICE_VERIFIED",
            "user_decision": "ONAY_BEKLIYOR",
            "ready_for_playlist": "HAYIR",
        })
    return rows, "ADAY_LISTESI_OKUNDU"

if __name__ == "__main__":
    if INPUT.is_file():
        try:
            raw = json.loads(INPUT.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError):
            raw = None
    else:
        raw = None
    rows, status = prepare(raw)
    with (OUT / "ibo_aday_inceleme_kuyrugu.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    report = {"status": status, "candidate_count": len(rows),
              "epg_statuses": dict(Counter(x["epg_pilot_status"] for x in rows)),
              "logo_statuses": dict(Counter(x["logo_status"] for x in rows)),
              "user_approved": 0, "playlist_changes": 0,
              "limitations": "Yalniz mevcut aday kanitindan inceleme CSV'si. Canli test, Isvec IBO cihaz testi, lisans veya kullanici onayi degildir."}
    (OUT / "ibo_aday_inceleme_ozeti.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"IBO aday inceleme kuyrugu: {len(rows)}; durum: {status}")
