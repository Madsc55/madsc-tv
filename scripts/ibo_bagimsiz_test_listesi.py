#!/usr/bin/env python3
"""Create isolated IBO review M3U from proven video+audio candidates; never edit protected lists."""
import csv,json,collections,re
from pathlib import Path
with open("GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv",encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
passed=[r for r in rows if r.get("TEKNIK_MEDYA")=="VIDEO_SES_VAR" and r.get("YAYIN_URL","").startswith(("http://","https://"))]
unique={r["YAYIN_URL"]:r for r in passed}
lines=["#EXTM3U"]
for r in sorted(unique.values(),key=lambda x:x.get("KANAL","")):
 name=re.sub(r"[\r\n]"," ",r.get("KANAL","Test adayi")).replace('"',"'")
 logo=r.get("LOGO_ADAY_URL","")
 if not logo.startswith(("https://","http://")):logo=""
 lines.append('#EXTINF:-1 tvg-logo="%s" group-title="IBO TEST ADAYLARI",%s'%(logo,name))
 lines.append(r["YAYIN_URL"])
Path("IBO_BAGIMSIZ_TEST_ADAYLARI.m3u").write_text("\n".join(lines)+"\n",encoding="utf-8")
with open("IBO_TEST_ADAYLARI.csv","w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=["KANAL","YAYIN_URL","COZUNURLUK","SES_IZI","IBO_KULLANICI_ONAYI"])
 w.writeheader()
 for r in sorted(unique.values(),key=lambda x:x.get("KANAL","")):w.writerow({"KANAL":r.get("KANAL",""),"YAYIN_URL":r["YAYIN_URL"],"COZUNURLUK":r.get("COZUNURLUK",""),"SES_IZI":r.get("SES_IZI",""),"IBO_KULLANICI_ONAYI":"BEKLIYOR"})
summary={"ibo_test_adayi":len(unique),"ana_listeye_eklenen":0,"uyari":"Teknik video+ses tespiti kanal kimligini, yayin haklarini veya IBO oynatmayi garanti etmez. Bu dosya yalniz bagimsiz kullanici testidir."}
Path("IBO_TEST_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
