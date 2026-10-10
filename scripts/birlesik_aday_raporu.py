#!/usr/bin/env python3
"""Read-only unified IPTV review report. Never auto-approve a channel."""
import csv,json,collections
from pathlib import Path
def read(path):
 with open(path,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
scores=read("AKILLI_ADAY_PUANLARI.csv")
stability={r["YAYIN_URL"]:r for r in read("KARARLILIK_RAPORU.csv")}
rows=[]
for r in scores:
 s=stability.get(r["YAYIN_URL"],{})
 stable=s.get("24_SAAT_KARARLI")=="EVET"
 technical=r.get("TEKNIK_KANIT")=="VIDEO_SES_VAR"
 # Do not add score twice; stability points are awarded only for independently verified 24h history.
 base=int(r.get("PUAN") or 0)
 points=min(100,base+(30 if stable else 0))
 if stable and technical:status="IBO_VE_KIMLIK_ONAYI_BEKLIYOR"
 elif technical:status="KARARLILIK_BEKLIYOR"
 else:status="TEKNIK_DOGRULAMA_BEKLIYOR"
 rows.append({"KANAL":r.get("KANAL",""),"PUAN":points,"TEKNIK_DURUM":r.get("TEKNIK_KANIT",""),"24_SAAT_KARARLI":"EVET" if stable else "HAYIR","DURUM":status,"IBO_ONAYI":"YOK","KULLANICI_ONAYI":"YOK","ANA_LISTEYE_EKLE":"HAYIR","YAYIN_URL":r["YAYIN_URL"],"KAYNAK":r.get("KAYNAK","")})
rows.sort(key=lambda x:(-x["PUAN"],x["KANAL"]))
with open("BIRLESIK_ADAY_ONAY_RAPORU.csv","w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["KANAL","PUAN","TEKNIK_DURUM","24_SAAT_KARARLI","DURUM","IBO_ONAYI","KULLANICI_ONAYI","ANA_LISTEYE_EKLE","YAYIN_URL","KAYNAK"]);w.writeheader();w.writerows(rows)
summary={"toplam_aday":len(rows),"durumlar":dict(collections.Counter(x["DURUM"] for x in rows)),"kullanici_onayi_olmadan_eklenen":0,"uyari":"Teknik puanlama kimlik veya IBO oynatma onayi degildir. Bu is akisinin liste yazma izni yoktur."}
Path("BIRLESIK_ADAY_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
