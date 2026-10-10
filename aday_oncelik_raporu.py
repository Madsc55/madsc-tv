#!/usr/bin/env python3
"""Adayları inceleme önceliğine göre raporla; ana listeyi değiştirmez."""
import csv
from pathlib import Path

SOURCE = Path("aday_bekletme/ADAY_DURUM_RAPORU.csv")
TARGET = Path("aday_bekletme/ADAY_ONCELIK_RAPORU.csv")
if not SOURCE.exists():
    raise SystemExit("Aday durum raporu bulunamadı")
with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
def rank(row):
    verified = row.get("DURUM") == "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR"
    new = row.get("ADAY_TURU") == "YENI_KANAL_ADAYI"
    media = row.get("MEDYA_TEST") == "VIDEO_SES_VAR"
    return (0 if verified and new else 1 if verified else 2 if media and new else 3 if media else 4, row.get("KANAL", "").casefold())
TARGET.parent.mkdir(parents=True, exist_ok=True)
with TARGET.open("w", encoding="utf-8-sig", newline="") as stream:
    fields = ["ONCELIK", "INCELEME_NOTU"] + (list(rows[0]) if rows else ["KANAL", "DURUM", "YAYIN_URL"])
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in sorted(rows, key=rank):
        tier = rank(row)[0]
        writer.writerow({"ONCELIK": tier + 1, "INCELEME_NOTU": "Kanal kimliği elle doğrulanmalı; otomatik ekleme yasak", **row})
print(f"Öncelik raporu hazır: {len(rows)} aday. Ana liste ve yedekler değiştirilmedi.")
