#!/usr/bin/env python3
"""Read-only candidate quarantine. Never edits main playlist or backups."""
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPORT = Path("YENILER_TARAMA_RAPORU.csv")
STATE = Path("aday_bekletme/gecmis.json")
OUTPUT = Path("aday_bekletme/ADAY_DURUM_RAPORU.csv")
FIELDS = ["KANAL", "ADAY_TURU", "TEKNIK_TEST", "MEDYA_TEST", "YAYIN_URL", "KAYNAK", "ILK_GORULME", "SON_GORULME", "GORULME_SAYISI", "BASARILI_TARAMA_SAYISI", "DURUM", "ACIKLAMA"]
now = datetime.now(timezone.utc).isoformat(timespec="seconds")
run_id = os.getenv("GITHUB_RUN_ID") or now

def main():
    if not REPORT.exists():
        raise SystemExit(f"Rapor bulunamadi: {REPORT}")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    previous = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if not isinstance(previous, dict):
        raise SystemExit("Gecmis JSON formati gecersiz")
    with REPORT.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    seen = set()
    for row in rows:
        url = (row.get("YAYIN_URL") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        record = previous.setdefault(url, {
            "first_seen": now, "last_seen": now, "runs": [], "successful_runs": [],
            "name": "", "kind": "", "source": "", "technical": "", "media": ""
        })
        record["last_seen"] = now
        record["name"] = row.get("KANAL", "")
        record["kind"] = row.get("ADAY_TURU", "")
        record["source"] = row.get("KAYNAK", "")
        record["technical"] = row.get("TEKNIK_TEST", "")
        record["media"] = row.get("MEDYA_TEST", "")
        if run_id not in record["runs"]:
            record["runs"].append(run_id)
        # HLS segment alone is insufficient: require detected video AND audio.
        passed = record["technical"] == "TEKNIK_AKIS_VAR" and record["media"] == "VIDEO_SES_VAR"
        if passed and run_id not in record["successful_runs"]:
            record["successful_runs"].append(run_id)
    result = []
    for url, record in sorted(previous.items(), key=lambda item: (item[1].get("name", ""), item[0])):
        successes = len(record.get("successful_runs", []))
        if successes >= 2:
            status = "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR"
        elif successes == 1:
            status = "TEKRAR_TEST_BEKLIYOR"
        else:
            status = "TEKNIK_DOGRULAMA_BEKLIYOR"
        result.append({
            "KANAL": record.get("name", ""), "ADAY_TURU": record.get("kind", ""),
            "TEKNIK_TEST": record.get("technical", ""), "MEDYA_TEST": record.get("media", ""),
            "YAYIN_URL": url, "KAYNAK": record.get("source", ""),
            "ILK_GORULME": record.get("first_seen", ""), "SON_GORULME": record.get("last_seen", ""),
            "GORULME_SAYISI": len(record.get("runs", [])),
            "BASARILI_TARAMA_SAYISI": successes, "DURUM": status,
            "ACIKLAMA": "Kanal kimligi dogrulanmadi; ana listeye otomatik ekleme yok"
        })
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(result)
    STATE.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Bekletilen aday: {len(result)}; farkli test kosusu: {run_id}; ana liste degismedi")

if __name__ == "__main__":
    main()
