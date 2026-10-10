#!/usr/bin/env python3
"""Safely build a separate YENILER candidate playlist from technical scan reports.

Never changes CALISANLAR.m3u. Stream identity and logo identity need player/manual review.
"""
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

MAIN = Path("CALISANLAR.m3u")
OUTPUT = Path("YENILER.m3u")
def norm(value):
    value = value.upper().translate(str.maketrans("İÇŞĞÜÖ", "ICSGUO"))
    value = re.sub(r"\[[^]]*\]|\([^)]*\)", " ", value)
    return re.sub(r"[^A-Z0-9]", "", value)

def read_m3u(path):
    if not path.exists():
        return []
    entries, meta = [], None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            meta = line
        elif meta and line.startswith(("https://", "http://")):
            entries.append((meta.rsplit(",", 1)[-1], line))
            meta = None
    return entries

def clean(value):
    return str(value or "").replace("\r", " ").replace("\n", " ").replace('"', "'").strip()

def build(report_paths):
    existing = read_m3u(MAIN)
    main_names = {norm(n) for n, _ in existing}
    main_urls = {u for _, u in existing}
    old = read_m3u(OUTPUT)
    used_names = {norm(n) for n, _ in old}
    used_urls = {u for _, u in old}
    additions = []
    for report in report_paths:
        with open(report, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("TEKNIK_TEST") != "TEKNIK_AKIS_VAR" or row.get("MEDYA_TEST") != "VIDEO_SES_VAR":
                    continue
                if row.get("ADAY_TURU") != "YENI_KANAL_ADAYI":
                    continue
                name, url = clean(row.get("KANAL")), clean(row.get("YAYIN_URL"))
                key = norm(name)
                if not key or not url.startswith(("https://", "http://")):
                    continue
                if key in main_names or key in used_names or url in main_urls or url in used_urls:
                    continue
                # Source-provided logos are candidates only, never silently treated as verified.
                logo = clean(row.get("LOGO_ADAY_URL"))
                if urlparse(logo).scheme != "https" or not re.search(r"\.(png|jpg|jpeg|webp)(?:\?|$)", logo, re.I):
                    logo = ""
                meta = f'#EXTINF:-1 group-title="YENILER" tvg-logo="{logo}",{name}'
                additions.append((meta, url))
                used_names.add(key)
                used_urls.add(url)
    lines = ["#EXTM3U"]
    for name, url in old:
        lines += [f'#EXTINF:-1 group-title="YENILER",{clean(name)}', url]
    for meta, url in additions:
        lines += [meta, url]
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"YENILER: {len(old)} previous, {len(additions)} new technically passing candidates. Identity not confirmed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 scripts/yeniler_aktar.py REPORT.csv [REPORT2.csv ...]")
    build(sys.argv[1:])
