#!/usr/bin/env python3
"""Read-only independent video/audio checks for YEDEKLER and YENILER categories."""
import csv,json,re,subprocess,collections
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
source=Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig").splitlines()
entries=[]
for i,line in enumerate(source):
 if not line.startswith("#EXTINF"):continue
 match=re.search(r'group-title="([^"]+)"',line)
 group=match.group(1) if match else ""
 if "YEDEKLER" not in group and "YENİLER" not in group:continue
 if i+1>=len(source):continue
 url=source[i+1].strip()
 if not url.startswith(("https://","http://")):continue
 entries.append({"KATEGORI":"YEDEKLER" if "YEDEKLER" in group else "YENILER","SIRA":str(sum(x["KATEGORI"]==("YEDEKLER" if "YEDEKLER" in group else "YENILER") for x in entries)+1),"KANAL":line.rsplit(",",1)[-1],"YAYIN_URL":url})
def probe(e):
 r=dict(e);r.update({"SONUC":"DOGRULANAMADI","COZUNURLUK":"","HATA":""})
 try:
  p=subprocess.run(["ffprobe","-v","error","-rw_timeout","9000000","-analyzeduration","2500000","-probesize","1500000","-show_entries","stream=codec_type,width,height","-of","json",e["YAYIN_URL"]],capture_output=True,text=True,timeout=16)
  if p.returncode:r["HATA"]=(p.stderr or "ffprobe hatasi")[:150];return r
  streams=json.loads(p.stdout).get("streams",[])
  v=next((x for x in streams if x.get("codec_type")=="video"),None)
  a=any(x.get("codec_type")=="audio" for x in streams)
  r["SONUC"]="VIDEO_SES_VAR" if v and a else "YALNIZ_VIDEO" if v else "YALNIZ_SES" if a else "MEDYA_YOK"
  if v:r["COZUNURLUK"]=str(v.get("width",""))+"x"+str(v.get("height",""))
 except Exception as ex:r["HATA"]=str(ex)[:150]
 return r
results=[]
with ThreadPoolExecutor(max_workers=8) as pool:
 for f in as_completed([pool.submit(probe,e) for e in entries]):
  r=f.result();results.append(r);print("KONTROL",r["KATEGORI"],r["SIRA"],r["KANAL"],r["SONUC"],flush=True)
results.sort(key=lambda x:(x["KATEGORI"],int(x["SIRA"])))
fields=["KATEGORI","SIRA","KANAL","YAYIN_URL","SONUC","COZUNURLUK","HATA"]
with open("YEDEKLER_YENILER_MEDYA_TEST.csv","w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(results)
summary={g:dict(collections.Counter(x["SONUC"] for x in results if x["KATEGORI"]==g)) for g in ("YEDEKLER","YENILER")}
summary["toplam"]=len(results)
summary["uyari"]="VIDEO_SES_VAR sadece teknik tespittir. DOGRULANAMADI silme gerekcesi degildir. Ana liste, yedekler ve yeniler degistirilmedi."
Path("YEDEKLER_YENILER_MEDYA_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print("SONUC_OZETI",json.dumps(summary,ensure_ascii=False))
