#!/usr/bin/env python3
"""Read-only multi-source IPTV discovery and bounded HLS segment test. Scan requested 2026-10-09."""
import csv
import os
import subprocess
import json
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
 "https://raw.githubusercontent.com/ilyswch/IPTV-TR/main/box.m3u",
 "https://raw.githubusercontent.com/ilyswch/IPTV-TR/main/box2.m3u",
 "https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye.m3u",
 "https://raw.githubusercontent.com/rideordie16/tv/main/tv2.m3u",
 "https://raw.githubusercontent.com/rideordie16/tv/main/tjk.m3u",
 "https://itasli.github.io/TURKTV/index.m3u",
 "https://stream.tvcdn.net/lists/tr.m3u",
 "https://stream.tvcdn.net/lists/tr-alt.m3u",
 "https://gist.githubusercontent.com/AyGitCi/8c105c9ab143830571ff61cc3883098e/raw/efti.m3u",
 "https://gist.githubusercontent.com/ukusgul-a11y/daa167880fc0133fe325f7e6096aac82/raw/umit.m3u",
 "https://raw.githubusercontent.com/mahirziyaokan/turkce-iptv/master/tr-00.m3u",
 "https://raw.githubusercontent.com/mahirziyaokan/turkce-iptv/master/tr-01.m3u",
 "https://raw.githubusercontent.com/mahirziyaokan/turkce-iptv/master/tr-02.m3u",
 "https://dearbulut.github.io/iptv/playlists/country/tr.m3u",
 "https://dearbulut.github.io/iptv/playlists/language/tur.m3u",
 "https://dearbulut.github.io/iptv/playlists/language/kur.m3u",
 "https://raw.githubusercontent.com/sayatsirinoglu/IPTV-List/main/TURK-IPTV-2024.m3u",
 "https://iptv-org.github.io/iptv/languages/kur.m3u",
]
# Discovered sources are recommendations, never trusted playlist modifications.
DISCOVERY = Path("YENI_KAYNAK_ONERILERI.csv")
if DISCOVERY.exists():
    with DISCOVERY.open(encoding="utf-8-sig", newline="") as source_file:
        for item in csv.DictReader(source_file):
            url = (item.get("KAYNAK_URL") or "").strip()
            if item.get("DURUM") == "ONERI_KONTROL_GEREKLI" and url.startswith("https://") and url not in SOURCES:
                SOURCES.append(url)
OUT = Path("YENILER_TARAMA_RAPORU.csv")
LIMIT = 30
BATCH = int(os.getenv('SCAN_BATCH', '0'))
PRIORITY = ("SOZCU", "TRT3", "AKIT", "GZT", "TV5", "SHOWMAX", "KANALDDRAMA", "HABER61", "LIFETV", "TGR T BELGESEL".replace(" ", ""), "TGRTBELGESEL")

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

def ffprobe_stream(url):
    """Check whether decodable video/audio stream metadata is exposed."""
    try:
        proc = subprocess.run(
            ["ffprobe", "-v", "error", "-rw_timeout", "12000000",
             "-analyzeduration", "5000000", "-probesize", "5000000",
             "-show_entries", "stream=codec_type,codec_name,width,height",
             "-of", "json", url],
            capture_output=True, text=True, timeout=22, check=False)
        if proc.returncode:
            return "FFPROBE_HATA", (proc.stderr or "ffprobe hata").strip()[:160]
        streams = json.loads(proc.stdout).get("streams", [])
        video = any(x.get("codec_type") == "video" for x in streams)
        audio = any(x.get("codec_type") == "audio" for x in streams)
        return ("VIDEO_SES_VAR" if video and audio else
                "YALNIZ_VIDEO" if video else "YALNIZ_SES" if audio else "MEDYA_YOK",
                "ffprobe: video=%s ses=%s; kanal kimligi kontrol edilmedi" % (video, audio))
    except Exception as error:
        return "FFPROBE_HATA", str(error)[:160]

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
ordered = sorted(candidates.items(), key=lambda item: (0 if any(norm(item[1][0]).startswith(p) for p in PRIORITY) else 1, norm(item[1][0]) in names, item[1][0]))
for index, (url, (name, source)) in enumerate(ordered):
    kind = "YENI_KANAL_ADAYI" if norm(name) not in names else "MEVCUT_KANAL_ALTERNATIFI"
    if BATCH * LIMIT <= index < (BATCH + 1) * LIMIT and (".m3u8" in url.lower()):
        status, detail, segments = hls_probe(url)
        media, media_detail = ffprobe_stream(url) if status == "TEKNIK_AKIS_VAR" else ("TEST_EDILMEDI", "HLS teknik akis dogrulanamadi")
    else:
        status, detail, segments = "TEST_EDILMEDI", "Test kotasi veya HLS olmayan URL", 0
        media, media_detail = "TEST_EDILMEDI", "Test uygulanmadi"
    rows.append((name, kind, status, segments, detail, media, media_detail, url, source))
with OUT.open("w", newline="", encoding="utf-8-sig") as output:
    writer = csv.writer(output)
    writer.writerow(("KANAL", "ADAY_TURU", "TEKNIK_TEST", "OKUNAN_SEGMENT", "ACIKLAMA", "MEDYA_TEST", "MEDYA_ACIKLAMA", "YAYIN_URL", "KAYNAK"))
    writer.writerows(rows)
Path("YENILER_KAYNAK_HATALARI.txt").write_text(
    "\n".join(f"{source}: {error}" for source, error in source_errors) or "Kaynak hatasi yok",
    encoding="utf-8")
print(f"Toplam {len(candidates)} benzersiz aday; test grubu {BATCH}, sira {BATCH * LIMIT + 1}-{min((BATCH + 1) * LIMIT, len(ordered))}.")
print("Ana liste degistirilmedi. Teknik akis, dogru kanal veya ses/goruntu kaniti degildir.")
