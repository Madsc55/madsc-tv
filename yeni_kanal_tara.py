#!/usr/bin/env python3
"""Salt okunur yeni kanal aday taramasi; ana listeyi asla degistirmez."""
import csv
import re
import urllib.request
from pathlib import Path

SOURCE = "https://iptv-org.github.io/iptv/countries/tr.m3u"
OUT = Path("YENILER_TARAMA_RAPORU.csv")

def parse(content):
    found = []
    meta = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            meta = line
        elif line and not line.startswith("#") and meta:
            name = meta.rsplit(",", 1)[-1].strip()
            tvg = re.search(r'tvg-name="([^"]+)"', meta)
            found.append(((tvg.group(1) if tvg else name).strip(), line))
            meta = None
    return found

def norm(name):
    return re.sub(r"[^A-Z0-9]", "", name.upper().replace("İ", "I").replace("Ç", "C").replace("Ş", "S").replace("Ğ", "G").replace("Ü", "U").replace("Ö", "O"))

existing = parse(Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig"))
names = {norm(n) for n, _ in existing}
urls = {u for _, u in existing}
req = urllib.request.Request(SOURCE, headers={"User-Agent": "MADSC-TV-Candidate-Scanner/1.0"})
with urllib.request.urlopen(req, timeout=30) as response:
    candidates = parse(response.read().decode("utf-8-sig", errors="replace"))
rows = []
seen = set()
for name, url in candidates:
    if not url.startswith(("https://", "http://")) or url in urls or (name, url) in seen:
        continue
    seen.add((name, url))
    rows.append((name, "YENI_KANAL" if norm(name) not in names else "YENI_ALTERNATIF", url, SOURCE))
with OUT.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(("KANAL", "DURUM", "YAYIN_URL", "KAYNAK"))
    writer.writerows(rows)
print(f"Tarama tamamlandi: {len(candidates)} kaynak, {len(rows)} aday. Ana liste degismedi.")
