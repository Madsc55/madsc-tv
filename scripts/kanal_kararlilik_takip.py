#!/usr/bin/env python3
"""Read-only longitudinal IPTV evidence tracker. Requires observations >=24h apart."""
import csv,json,os,datetime,collections
from pathlib import Path
NOW=datetime.datetime.now(datetime.timezone.utc)
SRC=Path("ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv")
HISTORY=Path("KARARLILIK_GECMISI.json")
OUT=Path("KARARLILIK_RAPORU.csv")
history={}
if HISTORY.exists():
 try: history=json.loads(HISTORY.read_text(encoding="utf-8"))
 except (ValueError,OSError): history={}
with SRC.open(encoding="utf-8-sig",newline="") as f: current=list(csv.DictReader(f))
report=[]
for row in current:
 url=row.get("YAYIN_URL","").strip()
 if not url: continue
 state=row.get("TEKNIK_MEDYA","")
 old=history.get(url,[])
 if not isinstance(old,list):old=[]
 old=[x for x in old if isinstance(x,dict) and x.get("at") and x.get("state")]
 old=[x for x in old if (NOW-datetime.datetime.fromisoformat(x["at"])).total_seconds()<=7*86400]
 old.append({"at":NOW.isoformat(),"state":state})
 history[url]=old[-40:]
 good=[datetime.datetime.fromisoformat(x["at"]) for x in old if x["state"]=="VIDEO_SES_VAR"]
 span=(max(good)-min(good)).total_seconds()/3600 if len(good)>=2 else 0
 # Any intervening failures invalidate a claim of stable playback.
 stable=len(good)>=2 and span>=24 and all(x["state"]=="VIDEO_SES_VAR" for x in old)
 report.append({"KANAL":row.get("KANAL",""),"GRUP":row.get("GRUP",""),"YAYIN_URL":url,"SON_DURUM":state,"GOZLEM_SAYISI":len(old),"BASARILI_VIDEO_SES_GOZLEMI":len(good),"BASARILI_ARALIK_SAAT":round(span,1),"24_SAAT_KARARLI":"EVET" if stable else "HAYIR","IBO_ONAYI":"YOK","ANA_LISTEYE_EKLENEBILIR":"HAYIR"})
HISTORY.write_text(json.dumps(history,ensure_ascii=False,indent=2),encoding="utf-8")
fields=["KANAL","GRUP","YAYIN_URL","SON_DURUM","GOZLEM_SAYISI","BASARILI_VIDEO_SES_GOZLEMI","BASARILI_ARALIK_SAAT","24_SAAT_KARARLI","IBO_ONAYI","ANA_LISTEYE_EKLENEBILIR"]
with OUT.open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(report)
summary={"aday":len(report),"24_saat_kararli":sum(r["24_SAAT_KARARLI"]=="EVET" for r in report),"not":"Yalniz teknik gozlemler; IBO oynatma veya kanal kimligi onayi degildir. Otomatik liste degisikligi yapilmaz."}
Path("KARARLILIK_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
