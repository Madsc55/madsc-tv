#!/usr/bin/env python3
"""Read-only multi-source IPTV discovery and bounded HLS segment test."""
import csv
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

SOURCES = [
 "https://iptv-org.github.io/iptv/countries/tr.m3u",
 "https://iptv-org.github.io/iptv/languages/tur.m3u",
 "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
 "https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye-iptv-org.m3u",
 "https://raw.githubusercontent.com/iptv-turk-tr/iptv/main/list.m3u",
 "https://raw.githubusercontent.com/discevisita/iptv/main/tr.m3u",
 "https://raw.githubusercontent.com/sayatsirinoglu/IPTV-List/main/tr.m3u",
]
OUT = Path("YENILER_TARAMA_RAPORU.csv")
LIMIT = 30
HEADERS = {"User-Agent": "Mozilla/5.0 MADSC-TV-Scanner/2.0"}

def fetch(url, timeout=12, limit=4000000):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(limit)

def parse(content):
    meta = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            meta = line
        elif line and not line.startswith("#") and meta:
            name = meta.rsplit(",", 1)[-1].strip()
            if name and line.startswith(("http://", "https://")):
                yield name, line
            meta = None

def norm(name):
    name = name.upper().translate(str.maketrans("İÇŞĞÜÖ", "ICSGUO"))
    name = re.sub(r"\[[^]]*\]|\([^)]*\)", " ", name)
    name = re.sub(r"\b(?:TR|TURKIYE|HD|FHD|UHD|QHD|SD|1080P|720P|576P|480P|360P)\b", " ", name)
    return re.sub(r"[^A-Z0-9]", "", name)

def hls_probe(url, seconds=30):
    """Probe HLS playlist and sample media repeatedly; not a visual/audio identity test."""
    start = time.monotonic()
    segments = 0
    try:
        while time.monotonic() - start < seconds:
            data = fetch(url, timeout=8, limit=250000).decode("utf-8-sig", errors="replace")
            if not data.lstrip().startswith("#EXTM3U"):
                return "DOGRULANAMADI", "HLS listesi degil", segments
            lines = [x.strip() for x in data.splitlines() if x.strip() and not x.startswith("#")]
            if not lines:
                return "DOGRULANAMADI", "Bos HLS listesi", segments
            if "#EXT-X-STREAM-INF" in data:
                url = urllib.parse.urljoin(url, lines[0])
                continue
            if "#EXTINF" not in data:
                return "DOGRULANAMADI", "Medya segmenti yok", segments
            segment = urllib.parse.urljoin(url, lines[-1])
            payload = fetch(segment, timeout=8, limit=65536)
            if not payload:
                return "DOGRULANAMADI", "Bos segment", segments
            segments += 1
            remaining = seconds - (time.monotonic() - start)
            if remaining > 0:
                time.sleep(min(5, remaining))
        return ("TEKNIK_AKIS_VAR" if segments >= 2 else "DOGRULANAMADI",
                "Segmentler indirildi; goruntu/ses/kanal kimligi dogrulanmadi", segments)
    except Exception as error:
        return "DOGRULANAMADI", str(error)[:160], segments

existing = list(parse(Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig")))
names = {norm(name) for name, _ in existing}
urls = {url for _, url in existing}
candidates = {}
source_errors = []
for source in SOURCES:
    try:
        content = fetch(source, timeout=20).decode("utf-8-sig", errors="replace")
        entries = list(parse(content))
        print(f"Kaynak: {source} -> {len(entries)} kayit")
        for name, url in entries:
            if url not in urls and url not in candidates:
                candidates[url] = (name, source)
    except Exception as error:
        source_errors.append((source, str(error)[:180]))
        print(f"Kaynak hatasi: {source}: {error}")

rows = []
# Prioritize genuinely missing names over existing channels' alternative streams.
ordered = sorted(candidates.items(), key=lambda item: (norm(item[1][0]) in names, item[1][0]))
for index, (url, (name, source)) in enumerate(ordered):
    kind = "YENI_KANAL_ADAYI" if norm(name) not in names else "MEVCUT_KANAL_ALTERNATIFI"
    if index < LIMIT and ".m3u8" in urllib.parse.urlsplit(url).path.lower():
        status, detail, segments = hls_probe(url)
    else:
        status, detail, segments = "TEST_EDILMEDI", "Test kotasi veya HLS olmayan URL", 0
    rows.append((name, kind, status, segments, detail, url, source))
with OUT.open("w", newline="", encoding="utf-8-sig") as output:
    writer = csv.writer(output)
    writer.writerow(("KANAL", "ADAY_TURU", "TEKNIK_TEST", "OKUNAN_SEGMENT", "ACIKLAMA", "YAYIN_URL", "KAYNAK"))
    writer.writerows(rows)
Path("YENILER_KAYNAK_HATALARI.txt").write_text(
    "\n".join(f"{source}: {error}" for source, error in source_errors) or "Kaynak hatasi yok",
    encoding="utf-8")
print(f"Toplam {len(candidates)} benzersiz aday; ilk {min(LIMIT, len(ordered))} aday teknik teste secildi.")
print("Ana liste degistirilmedi. Teknik akis, dogru kanal veya ses/goruntu kaniti degildir.")
