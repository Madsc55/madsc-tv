#!/usr/bin/env python3
"""Recheck backed-up streams. Never modify CALISANLAR.m3u.\nGitHub Actions push trigger: 2026-10-09.\n"""
import concurrent.futures, csv, os, re, subprocess
from pathlib import Path

SOURCE = Path("yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u")
REPORT = Path("yedekler/TEKRAR_TEST_2026-10-09.csv")
PASSED = Path("yedekler/TEKNIK_DOGRULANANLAR_2026-10-09.m3u")
entries = []
meta = None
for line in SOURCE.read_text(encoding="utf-8-sig").splitlines():
    line = line.strip()
    if line.startswith("#EXTINF:"):
        meta = line
    elif meta and line.startswith(("https://", "http://")):
        entries.append((meta, line))
        meta = None

def test(item):
    meta, url = item
    name = meta.rsplit(",", 1)[-1]
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-rw_timeout", "12000000",
             "-analyzeduration", "4000000", "-show_entries",
             "stream=codec_type", "-of", "csv=p=0", url],
            capture_output=True, text=True, timeout=22)
        codecs = probe.stdout.lower().splitlines()
        has_video = any("video" in x for x in codecs)
        has_audio = any("audio" in x for x in codecs)
        if probe.returncode or not (has_video and has_audio):
            return meta, url, name, "DOGRULANAMADI", "Video ve ses birlikte dogrulanamadi"
        sample = subprocess.run(
            ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
             "-rw_timeout", "12000000", "-i", url, "-t", "20",
             "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"],
            capture_output=True, text=True, timeout=45)
        if sample.returncode == 0:
            return meta, url, name, "TEKNIK_VIDEO_SES_20SN", "20 saniye medya cozumleme basarili; kanal kimligi dogrulanmadi"
        return meta, url, name, "DOGRULANAMADI", sample.stderr[-180:].replace("\n", " ")
    except (subprocess.TimeoutExpired, Exception) as exc:
        return meta, url, name, "DOGRULANAMADI", str(exc)[:180]

workers = max(1, min(12, int(os.environ.get("TEST_WORKERS", "10"))))
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
    results = list(pool.map(test, entries))
with REPORT.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["KANAL", "DURUM", "ACIKLAMA", "URL"])
    writer.writerows((name, status, detail, url) for _, url, name, status, detail in results)
lines = ["#EXTM3U"]
for meta, url, name, status, detail in results:
    if status == "TEKNIK_VIDEO_SES_20SN":
        lines.extend([meta, url])
PASSED.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("TOPLAM", len(results), "TEKNIK_VIDEO_SES_20SN", (len(lines)-1)//2)
print("Kanal kimligi otomatik dogrulanmadi. CALISANLAR.m3u degistirilmedi.")
