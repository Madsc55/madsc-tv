#!/usr/bin/env python3
"""Read-only bounded real ffprobe sampling of general discovered candidates."""
import csv,json,os,subprocess,collections
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
source=Path("YENILER_TARAMA_RAPORU.csv")
with source.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
batch=int(os.environ.get("ADAY_TEST_GRUBU","0"));size=30
rows=sorted(rows,key=lambda r:(r.get("ADAY_TURU")!="YENI_KANAL_ADAYI",r.get("KANAL",""),r.get("YAYIN_URL","")))
selected=rows[batch*size:(batch+1)*size]
def probe(row):
 url=row.get("YAYIN_URL","")
 result={k:row.get(k,"") for k in ("KANAL","ADAY_TURU","YAYIN_URL","KAYNAK","LOGO_ADAY_URL")}
 result.update({"TEKNIK_MEDYA":"DOGRULANAMADI","COZUNURLUK":"","SES_IZI":"False","HATA":""})
 try:
  p=subprocess.run(["ffprobe","-v","error","-rw_timeout","9000000","-analyzeduration","2500000","-probesize","1500000","-show_entries","stream=codec_type,width,height","-of","json",url],capture_output=True,text=True,timeout=16)
  if p.returncode:result["HATA"]=(p.stderr or "ffprobe error")[:120];return result
  streams=json.loads(p.stdout).get("streams",[])
  video=next((x for x in streams if x.get("codec_type")=="video"),None)
  audio=any(x.get("codec_type")=="audio" for x in streams)
  result["TEKNIK_MEDYA"]="VIDEO_SES_VAR" if video and audio else "YALNIZ_VIDEO" if video else "YALNIZ_SES" if audio else "MEDYA_YOK"
  result["SES_IZI"]=str(audio)
  if video:result["COZUNURLUK"]=str(video.get("width",""))+"x"+str(video.get("height",""))
 except Exception as e:result["HATA"]=str(e)[:120]
 return result
results=[]
with ThreadPoolExecutor(max_workers=6) as pool:
 futures=[pool.submit(probe,r) for r in selected]
 for f in as_completed(futures):
  r=f.result();results.append(r);print("ADAY_TEST",r["KANAL"],r["TEKNIK_MEDYA"],flush=True)
results.sort(key=lambda r:r["KANAL"])
fields=["KANAL","ADAY_TURU","YAYIN_URL","KAYNAK","LOGO_ADAY_URL","TEKNIK_MEDYA","COZUNURLUK","SES_IZI","HATA"]
with open("GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv","w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(results)
summary={"grup":batch,"test_edilen":len(results),"sonuclar":dict(collections.Counter(r["TEKNIK_MEDYA"] for r in results)),"uyari":"Teknik video/ses tespiti dogru kanal kimligi veya IBO oynatma onayi degildir. Listeler degistirilmedi."}
Path("GENEL_ADAY_MEDYA_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
