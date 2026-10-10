#!/usr/bin/env python3
"""Recheck quarantined candidates; never change main playlists or backups."""
import csv
import json
import os
from pathlib import Path
from yeni_kanal_tara import hls_probe, ffprobe_stream

STATE = Path("aday_bekletme/gecmis.json")
OUT = Path("aday_bekletme/ALТINCI_TEKRAR_TEST.csv".replace("Т", "T"))
FIELDS = ["KANAL", "YAYIN_URL", "KAYNAK", "ONCEKI_DURUM", "TEKNIK_TEST", "MEDYA_TEST", "SON_DURUM", "ACIKLAMA"]

def eligible(record):
    return len(record.get("successful_runs", [])) < 2

def check(url, record):
    technical, explanation, _ = hls_probe(url, seconds=20)
    media = "TEST_EDILMEDI"
    if technical == "TEKNIK_AKIS_VAR":
        media, detail = ffprobe_stream(url)
        explanation += "; " + detail
    success = technical == "TEKNIK_AKIS_VAR" and media == "VIDEO_SES_VAR"
    status = "TEKNIK_TEST_GECTI_KIMLIK_BEKLIYOR" if success else "TEKRAR_TEST_BEKLIYOR"
    return [record.get("name", ""), url, record.get("source", ""),
            record.get("technical", ""), technical, media, status, explanation[:300]]

def main():
    history = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if not isinstance(history, dict):
        raise ValueError("Gecmis dosyasi hatali")
    limit = max(0, min(int(os.getenv("RETEST_LIMIT", "10")), 30))
    candidates = [(url, rec) for url, rec in history.items()
                  if isinstance(rec, dict) and eligible(rec)
                  and url.startswith(("https://", "http://"))]
    # Prioritize previously timed-out or once successful candidates.
    candidates.sort(key=lambda x: (-len(x[1].get("successful_runs", [])),
                                   x[1].get("last_seen", ""), x[0]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(FIELDS)
        for url, record in candidates[:limit]:
            writer.writerow(check(url, record))
    print(f"Altinci gelistirme: {min(limit, len(candidates))} aday yeniden denendi; ana liste degismedi")

if __name__ == "__main__":
    main()
