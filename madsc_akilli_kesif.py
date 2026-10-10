#!/usr/bin/env python3
"""MADSC unified read-only IPTV candidate scanner."""
import csv,json,re,urllib.request,urllib.parse,subprocess,concurrent.futures,datetime,pathlib,os,time
OUT=pathlib.Path("madsc_kesif"); OUT.mkdir(exist_ok=True)
SOURCES={"iptv-org-TR":"https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u","iptv-org-TURKIYE":"https://iptv-org.github.io/iptv/countries/tr.m3u"}
def parse(s):
 lines=s.splitlines(); out=[]
 for i,line in enumerate(lines):
  if not line.startswith("#EXTINF"): continue
  for nextline in lines[i+1:i+4]:
   if nextline.startswith("#EXTINF"):break
   if nextline.startswith(("http://","https://")):
    def attr(k):
     m=re.search(k+'="([^"]*)"',line);return m.group(1) if m else ""
    out.append(dict(name=line.rsplit(",",1)[-1].strip(),url=nextline.strip(),logo=attr("tvg-logo"),id=attr("tvg-id")))
    break
 return out
def key(u):
 p=urllib.parse.urlsplit(u)
 q=[(k,v) for k,v in urllib.parse.parse_qsl(p.query) if k.lower() not in ("token","auth","expires","signature","sig","hash")]
 return urllib.parse.urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urllib.parse.urlencode(sorted(q)),""))
def name(s):
 s=re.sub(r'\[[^]]*\]|\([^)]*\)',' ',s.casefold())
 return re.sub(r'[^a-z0-9çğıöşü]','',re.sub(r'\b(1080p|720p|hd|fhd|sd|live|canli)\b',' ',s))
def probe(u):
 try:
  p=subprocess.run(["ffprobe","-v","error","-rw_timeout","9000000","-show_entries","stream=codec_type,width,height","-of","json",u],capture_output=True,text=True,timeout=22)
  st=json.loads(p.stdout).get("streams",[]) if p.returncode==0 else []
  v=next((x for x in st if x.get("codec_type")=="video"),{})
  return bool(v),any(x.get("codec_type")=="audio" for x in st),str(v.get("width",""))+"x"+str(v.get("height","")) if v else ""
 except Exception:return False,False,""
def logo(u):
 if not u:return "YOK"
 try:
  with urllib.request.urlopen(urllib.request.Request(u,method="HEAD",headers={"User-Agent":"Mozilla/5.0"}),timeout=7) as r:
   return "VAR" if r.status<400 and r.headers.get("Content-Type","").startswith("image/") else "BELIRSIZ"
 except Exception:return "DOGRULANAMADI"
def test(x):
 a=probe(x["url"]);time.sleep(3);b=probe(x["url"]);l=logo(x["logo"]);ok=all(a[:2]) and all(b[:2])
 return dict(kanal=x["name"],url=x["url"],kaynak=x["source"],durum="TEKNIK_GECTI_ONAY_BEKLIYOR" if ok else "TEKRAR_TEST_BEKLIYOR",puan=30+int(ok)*40+int(l=="VAR")*15+int(bool(x["id"]))*15,video=bool(a[0] and b[0]),ses=bool(a[1] and b[1]),cozunurluk=b[2],logo=l,ulke="ISVEC_DOGRULANMADI",test1=str(a),test2=str(b))
def write(file,rows,fields):
 with (OUT/file).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def main():
 master=pathlib.Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig");base=parse(master)
 for f in ("YENILER.m3u","MADSC_TV_47_LISTE_ADAY.m3u"):
  if pathlib.Path(f).exists():base+=parse(pathlib.Path(f).read_text(encoding="utf-8-sig"))
 known={key(x["url"]) for x in base};ids={x["id"].lower() for x in base if x["id"]};names={name(x["name"]) for x in base}
 state=OUT/"gecmis.json"
 try:history=json.loads(state.read_text()).get("history",{})
 except Exception:history={}
 if not isinstance(history,dict):history={}
 found=[];errors=[]
 for src,url in SOURCES.items():
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"MADSC-TV"}),timeout=18) as r:s=r.read(3000000).decode("utf-8-sig",errors="replace")
   for x in parse(s):x["source"]=src;found.append(x)
  except Exception as e:errors.append(src+": "+str(e)[:120])
 pending=[];duplicates=[];seen=set()
 for x in found:
  k=key(x["url"])
  why="AYNI_URL" if k in known else "AYNI_TARAMA" if k in seen else "AYNI_KANAL_KIMLIGI" if x["id"] and x["id"].lower() in ids else ""
  if why:duplicates.append(dict(kanal=x["name"],url=x["url"],neden=why))
  else:seen.add(k);pending.append(x)
 limit=30
 pending.sort(key=lambda x:(history.get(key(x["url"]),{}).get("last_test",""),x["name"]))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(test,pending[:limit]))
 for x in pending[limit:]:rows.append(dict(kanal=x["name"],url=x["url"],kaynak=x["source"],durum="SONRAKI_TEST_BEKLIYOR",puan=0,video="",ses="",cozunurluk="",logo="",ulke="ISVEC_DOGRULANMADI",test1="",test2=""))
 rows.sort(key=lambda r:(-r["puan"],r["kanal"]))
 write("adaylar.csv",rows,["kanal","url","kaynak","durum","puan","video","ses","cozunurluk","logo","ulke","test1","test2"])
 write("tekrarlar.csv",duplicates,["kanal","url","neden"])
 alternatives=[dict(kanal=x["name"],url=x["url"],kaynak=x["source"],durum="MEVCUT_KANAL_ICIN_ALTERNATIF_ONAY_BEKLIYOR") for x in pending if name(x["name"]) in names]
 write("alternatifler.csv",alternatives,["kanal","url","kaynak","durum"])
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for row in rows:
  if row["durum"]=="SONRAKI_TEST_BEKLIYOR":continue
  k=key(row["url"]);prev=history.get(k,{})
  prev["first_seen"]=prev.get("first_seen",now);prev["last_test"]=now
  prev["runs"]=int(prev.get("runs",0))+1
  passed=row["durum"]=="TEKNIK_GECTI_ONAY_BEKLIYOR"
  last_success=prev.get("last_success")
  hours=(datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(last_success)).total_seconds()/3600 if last_success else None
  distinct=passed and (last_success is None or hours>=6)
  prev["successful_runs"]=int(prev.get("successful_runs",0))+int(distinct)
  if passed and distinct:prev["last_success"]=now
  if not passed:prev["successful_runs"]=0;prev["last_success"]=None
  prev["channel"]=row["kanal"];prev["url"]=row["url"]
  row["durum"]=("UC_AYRI_ZAMAN_TESTI_GECTI_ONAY_BEKLIYOR" if prev["successful_runs"]>=3 else "FARKLI_SAATTE_TEKRAR_TEST_BEKLIYOR") if passed else "TEKRAR_TEST_BEKLIYOR"
  history[k]=prev
 write("adaylar.csv",rows,["kanal","url","kaynak","durum","puan","video","ses","cozunurluk","logo","ulke","test1","test2"])
 state.write_text(json.dumps({"history":history},ensure_ascii=False,indent=2))
 summary=dict(zaman=datetime.datetime.now(datetime.timezone.utc).isoformat(),ana_liste=len(parse(master)),kaynaklar=SOURCES,bulunan=len(found),tekrar=len(duplicates),aday=len(pending),test_edilen=min(limit,len(pending)),teknik_gecen=sum(x["durum"]=="UC_AYRI_ZAMAN_TESTI_GECTI_ONAY_BEKLIYOR" for x in rows),alternatif=len(alternatives),hatalar=errors,notlar="Ana liste degismedi. Farkli gun testleri ve Isvec erisimi bu kosuda dogrulanamaz. Kimlik onayi gerekir.")
 (OUT/"ozet.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()

# Initial integrated discovery validation trigger
