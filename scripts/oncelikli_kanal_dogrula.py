#!/usr/bin/env python3
"""Read-only focused IPTV checks; output artifacts only."""
import csv, json, re, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sources = [
"https://iptv-org.github.io/iptv/countries/tr.m3u",
"https://iptv-org.github.io/iptv/languages/tur.m3u",
"https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
"https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye-iptv-org.m3u",
"https://raw.githubusercontent.com/iptv-turk-tr/iptv/main/list.m3u",
"https://raw.githubusercontent.com/discevisita/iptv/main/tr.m3u",
"https://raw.githubusercontent.com/sayatsirinoglu/IPTV-List/main/tr.m3u",
"https://raw.githubusercontent.com/ilyswch/IPTV-TR/main/box.m3u",
"https://raw.githubusercontent.com/ilyswch/IPTV-TR/main/box2.m3u",
"https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye.m3u",
"https://raw.githubusercontent.com/rideordie16/tv/main/tv2.m3u",
"https://itasli.github.io/TURKTV/index.m3u",
"https://gist.githubusercontent.com/AyGitCi/8c105c9ab143830571ff61cc3883098e/raw/efti.m3u",
"https://gist.githubusercontent.com/ukusgul-a11y/daa167880fc0133fe325f7e6096aac82/raw/umit.m3u",
"https://raw.githubusercontent.com/mahirziyaokan/turkce-iptv/master/tr-00.m3u",
"https://raw.githubusercontent.com/mahirziyaokan/turkce-iptv/master/tr-01.m3u",
"https://raw.githubusercontent.com/mahirziyaokan/turkce-iptv/master/tr-02.m3u",
"https://dearbulut.github.io/iptv/playlists/country/tr.m3u",
"https://dearbulut.github.io/iptv/playlists/language/tur.m3u",
"https://raw.githubusercontent.com/sayatsirinoglu/IPTV-List/main/TURK-IPTV-2024.m3u",
]
def normalize(s):
 s=s.upper().translate(str.maketrans("İÇŞĞÜÖ","ICSGUO"))
 return re.sub("[^A-Z0-9]","",s)
def group(s):
 n=normalize(s)
 for label, patterns in [
 ("TGRT Belgesel",["TGRTBELGESEL"]),
 ("Sözcü TV",["SOZCUTV","SOZCU"]),
 ("Akit TV",["AKITTV"]),
 ("S Sport",["SSPORT"]),
 ("Discovery Science",["DISCOVERYSCIENCE"]),
 ("Tarih TV",["TARIHTV"])]:
  if any(p in n for p in patterns): return label
 return None
def fetch(source):
 try:
  req=urllib.request.Request(source,headers={"User-Agent":"Mozilla/5.0"})
  data=urllib.request.urlopen(req,timeout=16).read(4000000).decode("utf-8-sig","replace")
  meta=None; found=[]
  for line in data.splitlines():
   line=line.strip()
   if line.startswith("#EXTINF:"):meta=line
   elif meta and line.startswith(("http://","https://")):
    name=meta.rsplit(",",1)[-1].strip()
    label=group(name)
    if label:found.append((label,name,line,source))
    meta=None
  return found
 except Exception as e:
  print("SOURCE_ERROR",source,str(e)[:90],flush=True)
  return []
entries={}
with ThreadPoolExecutor(max_workers=10) as pool:
 for found in pool.map(fetch,sources):
  for entry in found: entries.setdefault(entry[2],entry)
print("UNIQUE_PRIORITY_URLS",len(entries),flush=True)
def probe(entry):
 label,name,url,source=entry
 if not url.startswith(("http://","https://")):return (label,name,"GECERSIZ_URL","","","",url,source)
 try:
  p=subprocess.run(["ffprobe","-v","error","-rw_timeout","10000000","-analyzeduration","2500000","-probesize","1500000","-show_entries","stream=codec_type,codec_name,width,height","-of","json",url],capture_output=True,text=True,timeout=18)
  if p.returncode:return (label,name,"DOGRULANAMADI","","","",(p.stderr or "")[:160],url,source)
  streams=json.loads(p.stdout).get("streams",[])
  video=next((x for x in streams if x.get("codec_type")=="video"),None)
  audio=next((x for x in streams if x.get("codec_type")=="audio"),None)
  state="VIDEO_SES_VAR" if video and audio else "YALNIZ_VIDEO" if video else "YALNIZ_SES" if audio else "MEDYA_YOK"
  resolution=("%sx%s"%(video.get("width",""),video.get("height",""))) if video else ""
  return (label,name,state,resolution,str(bool(audio)), "",url,source)
 except Exception as e:return (label,name,"DOGRULANAMADI","","",str(e)[:160],url,source)
rows=[]
with ThreadPoolExecutor(max_workers=6) as pool:
 futures=[pool.submit(probe,e) for e in entries.values()]
 for future in as_completed(futures):
  row=future.result();rows.append(row);print("RESULT",row[0],row[1],row[2],flush=True)
rows.sort()
with open("ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv","w",newline="",encoding="utf-8-sig") as f:
 w=csv.writer(f);w.writerow(["GRUP","KANAL","TEKNIK_MEDYA","COZUNURLUK","SES_IZI","HATA","YAYIN_URL","KAYNAK"]);w.writerows(rows)
counts=dict(__import__("collections").Counter(x[2] for x in rows))
Path("ONCELIKLI_OZET.json").write_text(json.dumps({"toplam":len(rows),"sonuclar":counts,"uyari":"ffprobe codec detection is not verified IBO playback or channel identity"},ensure_ascii=False,indent=2),encoding="utf-8")
print("SUMMARY",json.dumps(counts),flush=True)
