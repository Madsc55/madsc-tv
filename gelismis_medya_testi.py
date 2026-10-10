#!/usr/bin/env python3
"""Independent bounded 20-second decode test of promising HLS candidates; no playlist edits."""
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
    # -t bounds media duration, subprocess timeout bounds stalled network.
    cmd = ["ffmpeg","-nostdin","-hide_banner","-loglevel","error",
           "-rw_timeout","12000000","-i",url,"-t","20",
           "-map","0:v:0?","-map","0:a:0?","-f","null","-"]
    try:
        p = subprocess.run(cmd,capture_output=True,text=True,timeout=65,check=False)
        if p.returncode:
            return ["BELIRSIZ","BELIRSIZ","DOGRULANAMADI",(p.stderr or "ffmpeg hata")[-200:].replace("\n"," ")]
        # Decode success is not proof of BOTH streams. Require prior ffprobe video+audio metadata.
        both = row.get("MEDYA_TEST") == "VIDEO_SES_VAR"
        return ["EVET" if both else "BELIRSIZ","EVET" if both else "BELIRSIZ",
                "20SN_MEDYA_COZUMLEME_GECTI_KIMLIK_BEKLIYOR" if both else "MEDYA_BILESENI_BELIRSIZ",
                "20 saniyelik cozumleme tamamlandi; kanal kimligi ve yayin hakki dogrulanmadi"]
    except subprocess.TimeoutExpired:
        return ["BELIRSIZ","BELIRSIZ","ZAMAN_ASIMI","65 saniye zaman asimi"]
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
