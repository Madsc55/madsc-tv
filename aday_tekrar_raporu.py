#!/usr/bin/env python3
"""Group duplicate candidate stream URLs; never modify playlists."""
import csv
from collections import defaultdict
from pathlib import Path

SOURCE = Path("aday_bekletme/HAM_ADAY_KAYNAKLARI.csv")
OUTPUT = Path("aday_bekletme/TEKRAR_EDEN_ADAYLAR.csv")

def duplicate_groups(rows):
    groups = defaultdict(list)
    for row in rows:
        url = (row.get("YAYIN_URL") or "").strip()
        if url:
            groups[url].append(row)
    return [(url, entries) for url, entries in sorted(groups.items()) if len(entries) > 1]

def main():
    if not SOURCE.exists():
        raise SystemExit("Tarama raporu bulunamadi")
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["YAYIN_URL", "TEKRAR_SAYISI", "KANAL_ADLARI", "KAYNAKLAR"])
        groups = duplicate_groups(rows)
        for url, entries in groups:
            writer.writerow([url, len(entries),
                             " | ".join(sorted({e.get("KANAL", "") for e in entries})),
                             " | ".join(sorted({e.get("KAYNAK", "") for e in entries}))])
    print(f"Tekrar grubu: {len(groups)}; ana liste degismedi")

if __name__ == "__main__":
    main()
