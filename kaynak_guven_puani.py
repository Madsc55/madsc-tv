#!/usr/bin/env python3
"""Read-only source reliability scoring from candidate quarantine history."""
import csv
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

STATE = Path("aday_bekletme/gecmis.json")
OUTPUT = Path("aday_bekletme/KAYNAK_GUVEN_PUANLARI.csv")

def main():
    history = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if not isinstance(history, dict):
        raise SystemExit("Gecmis dosyasi gecersiz")
    sources = defaultdict(lambda: {"total": 0, "passed": 0, "retested": 0})
    for url, item in history.items():
        if not isinstance(item, dict):
            continue
        source = str(item.get("source") or "").strip()
        if not source:
            try:
                source = urlsplit(url).hostname or "BILINMIYOR"
            except ValueError:
                source = "BILINMIYOR"
        stats = sources[source]
        stats["total"] += 1
        runs = len(set(map(str, item.get("runs", []))))
        successes = len(set(map(str, item.get("successful_runs", []))))
        if successes:
            stats["passed"] += 1
        if successes >= 2 and runs >= 2:
            stats["retested"] += 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["KAYNAK", "ADAY_SAYISI", "EN_AZ_BIR_BASARI", "TEKRAR_DOGRULANAN", "GUVEN_PUANI", "NOT"])
        for name, s in sorted(sources.items()):
            # Bayesian smoothing: small samples do not get unjustified perfect scores.
            score = round(100 * (s["passed"] + 2 * s["retested"] + 1) / (3 * s["total"] + 2))
            writer.writerow([name, s["total"], s["passed"], s["retested"], score,
                             "Teknik guven puani; kanal kimligi veya yayin hakki dogrulamasi degildir"])
    print(f"Puanlanan kaynak: {len(sources)}; ana liste degismedi")

if __name__ == "__main__":
    main()
