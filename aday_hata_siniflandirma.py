#!/usr/bin/env python3
"""12: classify candidate failures conservatively, without changing playlists."""
import csv
from pathlib import Path

SOURCE = Path("aday_bekletme/ADAY_DURUM_RAPORU.csv")
OUTPUT = Path("aday_bekletme/ADAY_HATA_SINIFLANDIRMA.csv")

def classify(row):
    details = " ".join(str(row.get(key) or "") for key in ("TEKNIK_TEST", "MEDYA_TEST", "ACIKLAMA")).lower()
    if any(term in details for term in ("401", "403", "unauthorized", "forbidden", "token expired", "token_expired", "signature expired")):
        return "ERISIM_VEYA_TOKEN_SORUNU", "HTTP yetki hatasi tek basina token suresinin doldugunu kanitlamaz"
    if any(term in details for term in ("geo_block", "geoblock", "geo-restricted", "not available in your country", "region blocked")):
        return "OLASI_COGRAFI_ENGEL", "Bolgesel engel ancak farkli konumlardan testle dogrulanabilir"
    if any(term in details for term in ("timeout", "timed out", "connection reset", "502", "503", "504", "temporarily unavailable")):
        return "GECICI_ERISIM_SORUNU_OLASI", "Tek test kalici kesintiyi kanitlamaz; tekrar test gerekli"
    if row.get("TEKNIK_TEST") == "TEKNIK_AKIS_VAR" and row.get("MEDYA_TEST") == "VIDEO_SES_VAR":
        return "TEKNIK_AKIS_DOGRULANDI", "Kanal kimligi ayrica dogrulanmalidir"
    return "NEDEN_BELIRSIZ", "Ek HTTP ve medya test kaniti gerekiyor"

def main():
    if not SOURCE.exists():
        raise SystemExit(f"Rapor bulunamadi: {SOURCE}")
    with SOURCE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["KANAL", "HATA_SINIFI", "GEREKCE"])
        writer.writeheader()
        for row in rows:
            category, reason = classify(row)
            writer.writerow({"KANAL": row.get("KANAL", ""), "HATA_SINIFI": category, "GEREKCE": reason})
    print(f"Siniflandirilan aday: {len(rows)}; oynatma listeleri degismedi")

if __name__ == "__main__":
    main()
