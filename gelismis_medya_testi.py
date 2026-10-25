#!/usr/bin/env python3
"""Bounded independent video-frame and audio-PCM decode probes; no playlist edits."""
import csv
import json
import os
import subprocess
from pathlib import Path

SOURCE = Path("YENILER_TARAMA_RAPORU.csv")
OUT = Path("aday_bekletme/GELISMIS_MEDYA_TESTI.csv")
FIELDS = ["KANAL","YAYIN_URL","KAYNAK","ON_TEST","VIDEO","SES","DURUM","ACIKLAMA"]
MAX = max(0, min(int(os.getenv("DEEP_TEST_LIMIT", "5")), 10))

def check(row):
    url = row["YAYIN_URL"].strip()
    if not url.lower().startswith(("https://","http://")):
        return ["HAYIR","HAYIR","DOGRULANAMADI","Gecersiz URL"]
    # Separate bounded decodes prove actual output for each media type.
    # A prior CSV flag or stream metadata alone is never accepted as evidence.
    base = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
            "-rw_timeout", "12000000", "-i", url]
    video_cmd = base + ["-map", "0:v:0", "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "mjpeg", "pipe:1"]
    audio_cmd = base + ["-map", "0:a:0", "-t", "2",
                        "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1"]
    try:
        video = subprocess.run(video_cmd, capture_output=True, timeout=65, check=False)
        audio = subprocess.run(audio_cmd, capture_output=True, timeout=65, check=False)
        has_video = video.returncode == 0 and len(video.stdout) > 0
        has_audio = audio.returncode == 0 and len(audio.stdout) > 0
        if has_video and has_audio:
            return ["EVET", "EVET", "MEDYA_ORNEGI_COZULDU_KIMLIK_BEKLIYOR",
                    "Tek video kare ve iki saniyelik ses PCM ornegi cozuldu; sureklilik, kimlik ve yayin hakki dogrulanmadi"]
        details = (video.stderr or b"")[-100:] + b" " + (audio.stderr or b"")[-100:]
        return ["EVET" if has_video else "BELIRSIZ",
                "EVET" if has_audio else "BELIRSIZ",
                "MEDYA_BILESENI_BELIRSIZ",
                details.decode("utf-8", errors="replace").replace("\\n", " ")[:200]]
    except subprocess.TimeoutExpired:
        return ["BELIRSIZ","BELIRSIZ","TEKRAR_TEST_BEKLIYOR","65 saniye zaman asimi; yayin bozuk sayilmadi, sonraki taramada yeniden denenecek"]
    except Exception as exc:
        return ["BELIRSIZ","BELIRSIZ","DOGRULANAMADI",str(exc)[:200]]

def main():
    with SOURCE.open(encoding="utf-8-sig",newline="") as f:
        rows = list(csv.DictReader(f))
    promising = [r for r in rows if r.get("TEKNIK_TEST")=="TEKNIK_AKIS_VAR" and r.get("MEDYA_TEST")=="VIDEO_SES_VAR"]
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(FIELDS)
        for r in promising[:MAX]:
            w.writerow([r.get("KANAL",""),r.get("YAYIN_URL",""),r.get("KAYNAK",""),r.get("MEDYA_TEST",""),*check(r)])
    print(f"Gelismis medya testi: {min(MAX,len(promising))} aday / {len(promising)} uygun; ana liste degismedi")

if __name__=="__main__":
    main()
