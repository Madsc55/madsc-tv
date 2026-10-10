#!/usr/bin/env python3
"""9. geliştirme: adaylar için salt-okunur akıllı tekrar test planı."""
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

STATE = Path("aday_bekletme/gecmis.json")
OUTPUT = Path("aday_bekletme/AKILLI_TEKRAR_TEST_TAKVIMI.csv")
FIELDS = ["KANAL", "YAYIN_URL", "SON_TEST", "SONUC", "TEST_ARALIGI_SAAT", "SONRAKI_TEST", "TEST_ZAMANI_GELDI"]

def plan(records, now):
    rows = []
    for url, record in sorted(records.items()):
        if not isinstance(record, dict):
            continue
        runs = record.get("runs") or []
        successes = record.get("successful_runs") or []
        last = record.get("last_seen") or record.get("first_seen")
        try:
            tested = datetime.fromisoformat(last.replace("Z", "+00:00")).astimezone(timezone.utc) if last else now
        except (ValueError, AttributeError):
            tested = now
        passed = record.get("technical") == "TEKNIK_AKIS_VAR" and record.get("media") == "VIDEO_SES_VAR"
        # Hata alan adaylar daha sık; art arda doğrulanan adaylar daha seyrek.
        hours = 24 if passed and len(successes) >= 3 else 12 if passed and len(successes) >= 2 else 6 if passed else 2
        next_test = tested + timedelta(hours=hours)
        rows.append({"KANAL": record.get("name", ""), "YAYIN_URL": url,
                     "SON_TEST": tested.isoformat(timespec="seconds"), "SONUC": "BASARILI" if passed else "TEKRAR_KONTROL",
                     "TEST_ARALIGI_SAAT": hours, "SONRAKI_TEST": next_test.isoformat(timespec="seconds"),
                     "TEST_ZAMANI_GELDI": "EVET" if next_test <= now else "HAYIR"})
    return rows

def main():
    if not STATE.exists():
        raise SystemExit("Aday geçmişi bulunamadı")
    records = json.loads(STATE.read_text(encoding="utf-8"))
    if not isinstance(records, dict):
        raise SystemExit("Aday geçmişi JSON nesnesi olmalı")
    now = datetime.now(timezone.utc)
    rows = plan(records, now)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Akıllı tekrar test planı: {len(rows)} aday; zamanı gelen: {sum(r['TEST_ZAMANI_GELDI']=='EVET' for r in rows)}. Ana listeye dokunulmadı.")

if __name__ == "__main__":
    main()
