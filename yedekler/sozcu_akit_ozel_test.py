#!/usr/bin/env python3
import csv, subprocess, concurrent.futures
from pathlib import Path
source=Path("yedekler/YENILER_TARAMA_RAPORU_2026-10-09.csv")
with source.open(encoding="utf-8-sig",newline="") as f:
    candidates=[(r["KANAL"],r["YAYIN_URL"],r["KAYNAK"]) for r in csv.DictReader(f) if r["KANAL"].upper().startswith(("AKIT","SÖZCÜ","SOZCU"))]
candidates += [
 ("AKIT TV","http://185.234.111.229:8000/play/a05m","GitHub Yusiff0 IPTV"),
 ("AKIT TV","http://stream.tvcdn.net/haber/akit-tv.m3u8","GitHub oldstuffs IPTV"),
 ("SÖZCÜ TV","http://stream.tvcdn.net/haber/sozcu-tv.m3u8","GitHub oldstuffs IPTV")]
seen=set(); candidates=[x for x in candidates if not (x[1] in seen or seen.add(x[1]))]
def check(item):
    name,url,source=item
    try:
        p=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type","-of","csv=p=0",url],capture_output=True,text=True,timeout=20)
        codecs=p.stdout.splitlines()
        status="VIDEO_SES_VAR" if "video" in codecs and "audio" in codecs else "VIDEO_VAR" if "video" in codecs else "SES_VAR" if "audio" in codecs else "DOGRULANAMADI"
        return name,status,(p.stderr or "")[:200],url,source
    except subprocess.TimeoutExpired:
        return name,"ZAMAN_ASIMI","20 saniye",url,source
    except Exception as e:
        return name,"HATA",str(e)[:200],url,source
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(check,candidates))
out=Path("yedekler/SOZCU_AKIT_OZEL_TEST_2026-10-09.csv")
with out.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f);w.writerow(["KANAL","TEKNIK_DURUM","ACIKLAMA","YAYIN_URL","KAYNAK"]);w.writerows(rows)
print("Toplam:",len(rows),"video ve ses:",sum(x[1]=="VIDEO_SES_VAR" for x in rows))
print("Teknik sonuc kanal kimligi veya IBO Player dogrulamasi degildir")
