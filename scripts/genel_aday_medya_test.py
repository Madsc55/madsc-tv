#!/usr/bin/env python3
"""Read-only bounded real ffprobe sampling of general discovered candidates."""
import csv,json,os,subprocess,collections,datetime
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
source=Path("YENILER_TARAMA_RAPORU.csv")
with source.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
batch=int(os.environ.get("ADAY_TEST_GRUBU","0"));size=30
if batch < 0:
 raise ValueError("Negatif aday parti numarasi yasak")
rows=sorted(rows,key=lambda r:(r.get("ADAY_TURU")!="YENI_KANAL_ADAYI",r.get("KANAL",""),r.get("YAYIN_URL","")))
selected=rows[batch*size:(batch+1)*size]
if not selected:
 raise ValueError(f"Aday partisi bos veya kapsam disi: {batch}; toplam aday {len(rows)}")
reuse={}
if os.environ.get("MADSC_MEDYA_SKIP_CSV"):
 with Path(os.environ["MADSC_MEDYA_SKIP_CSV"]).open(encoding="utf-8-sig",newline="") as f:
  reuse={row["YAYIN_URL"]:row for row in csv.DictReader(f)}
def probe(row):
 url=row.get("YAYIN_URL","")
 result={k:row.get(k,"") for k in ("KANAL","ADAY_TURU","YAYIN_URL","KAYNAK","LOGO_ADAY_URL")}
 if url in reuse:
  previous=reuse[url]
  for key in ("TEKNIK_MEDYA","COZUNURLUK","SES_IZI","HATA","OLCUM_ZAMANI"):result[key]=previous.get(key,"")
  return result
 result["OLCUM_ZAMANI"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
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
fields=["KANAL","ADAY_TURU","YAYIN_URL","KAYNAK","LOGO_ADAY_URL","TEKNIK_MEDYA","COZUNURLUK","SES_IZI","HATA","OLCUM_ZAMANI"]
with open("GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv","w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(results)
summary={"grup":batch,"test_edilen":sum(r["YAYIN_URL"] not in reuse for r in results),"yeniden_kullanilan":sum(r["YAYIN_URL"] in reuse for r in results),"rapor_satiri":len(results),"sonuclar":dict(collections.Counter(r["TEKNIK_MEDYA"] for r in results)),"uyari":"Teknik video/ses tespiti dogru kanal kimligi veya IBO oynatma onayi degildir. Listeler degistirilmedi."}
Path("GENEL_ADAY_MEDYA_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
