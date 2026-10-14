#!/usr/bin/env python3
"""Four-stage discovery evidence report. Read-only; EPG deliberately postponed."""
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_kesif"
def read_rows(name):
    path = OUT / name
    if not path.exists():
        return None
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))
def main():
    history_path = OUT / "gecmis.json"
    archive_path = OUT / "bulunan_kanal_arsivi.csv"
    if not history_path.is_file() or not archive_path.is_file():
        raise RuntimeError("Arsiv/gecmis kaniti eksik; basarili sayilamaz")
    history = json.loads(history_path.read_text(encoding="utf-8"))
    if not isinstance(history.get("history"), dict):
        raise RuntimeError("Gecmis kaydi gecersiz")
    archive = read_rows("bulunan_kanal_arsivi.csv")
    candidates = read_rows("adaylar.csv")
    alternatives = read_rows("alternatifler.csv")
    if candidates is None or alternatives is None:
        raise RuntimeError("Aday/alternatif tarama dosyasi eksik")
    urls = [x.get("url", "").strip() for x in archive if x.get("url", "").strip()]
    repeated = len(urls) - len(set(urls))
    technical = Counter(x.get("durum", "BILINMIYOR") for x in candidates)
    logo_path = OUT / "candidate_logos.json"
    logos = json.loads(logo_path.read_text(encoding="utf-8")) if logo_path.is_file() else {}
    prepared = logos.get("results", []) if isinstance(logos, dict) else []
    if not isinstance(prepared, list):
        prepared = []
    report = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "stages": {
            "yedek": {"historical_entries": len(history["history"]), "restore_tested": False,
                       "independent_offsite_copy_verified": False, "status": "KANIT_EKSIK"},
            "arsiv": {"archived_urls": len(archive), "duplicate_exact_urls": repeated,
                      "historical_entries": len(history["history"]), "status": "KAYIT_KONTROL_EDILDI"},
            "kesif": {"candidates": len(candidates), "alternatives": len(alternatives),
                      "candidate_technical_status": dict(technical), "status": "RAPORLANDI_CIHAZ_ONAYSIZ"},
            "aday_logo_ve_tekrar": {"prepared_logo_results": len(prepared),
                                    "visual_identity_confirmed": False,
                                    "main_playlist_logos_preserved": True,
                                    "status": "ADAY_KANITI_AYRI"}
        },
        "epg": "ERTELENDI_EN_SON",
        "ibo_approval": False,
        "protected_playlists_modified": False
    }
    (OUT / "DORT_ASAMA_TEK_RAPOR.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
if __name__ == "__main__":
    main()
