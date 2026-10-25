#!/usr/bin/env python3
"""MADSC unified read-only IPTV candidate scanner."""
import csv,json,re,urllib.request,urllib.parse,subprocess,concurrent.futures,datetime,pathlib,os,time
OUT=pathlib.Path("madsc_kesif"); OUT.mkdir(exist_ok=True)
# Discovery target: 155 distinct, verified source endpoints. Never pad with duplicates.
SOURCE_TARGET=155

SOURCES={"iptv-turk-tr-EK-KAYNAK":"https://raw.githubusercontent.com/iptv-turk-tr/iptv/main/list.m3u","iptv-org-TR":"https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u","iptv-org-TURKIYE":"https://iptv-org.github.io/iptv/countries/tr.m3u","iptv-org-TURKCE":"https://iptv-org.github.io/iptv/languages/tur.m3u","iptv-org-AZERBAYCAN":"https://iptv-org.github.io/iptv/countries/az.m3u","omerdenizhan-TR":"https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye.m3u","ilyswch-TR":"https://raw.githubusercontent.com/ilyswch/turk-iptv/main/index.m3u","itasli-TR":"https://itasli.github.io/TURKTV/index.m3u","gkhncksn-TR":"https://raw.githubusercontent.com/gkhncksn/m3u8_lists/main/TURK_KANALLARI.m3u","Lunedor-TR":"https://raw.githubusercontent.com/Lunedor/iptvTR/main/iptv_tum_kanallar.m3u","dearbulut-TR":"https://dearbulut.github.io/iptv/playlists/country/tr.m3u","dearbulut-TURKCE":"https://dearbulut.github.io/iptv/playlists/language/tur.m3u","dearbulut-AZERBAYCAN":"https://dearbulut.github.io/iptv/playlists/country/az.m3u","dearbulut-KURTCE":"https://dearbulut.github.io/iptv/playlists/language/kur.m3u","dearbulut-AZERICE":"https://dearbulut.github.io/iptv/playlists/language/aze.m3u","dearbulut-TURKMENCE":"https://dearbulut.github.io/iptv/playlists/language/tuk.m3u","dearbulut-KIBRIS":"https://dearbulut.github.io/iptv/playlists/country/cy.m3u","dearbulut-TURKMENISTAN":"https://dearbulut.github.io/iptv/playlists/country/tm.m3u","dearbulut-ALMANYA":"https://dearbulut.github.io/iptv/playlists/country/de.m3u","dearbulut-ISVEC":"https://dearbulut.github.io/iptv/playlists/country/se.m3u","dearbulut-HOLLANDA":"https://dearbulut.github.io/iptv/playlists/country/nl.m3u","dearbulut-BELCIKA":"https://dearbulut.github.io/iptv/playlists/country/be.m3u","dearbulut-AVUSTURYA":"https://dearbulut.github.io/iptv/playlists/country/at.m3u","dearbulut-HABER":"https://dearbulut.github.io/iptv/playlists/category/news.m3u","dearbulut-SPOR":"https://dearbulut.github.io/iptv/playlists/category/sports.m3u","dearbulut-BELGESEL":"https://dearbulut.github.io/iptv/playlists/category/documentary.m3u","dearbulut-COCUK":"https://dearbulut.github.io/iptv/playlists/category/kids.m3u","dearbulut-MUZIK":"https://dearbulut.github.io/iptv/playlists/category/music.m3u","dearbulut-KULTUR":"https://dearbulut.github.io/iptv/playlists/category/culture.m3u","dearbulut-BILIM":"https://dearbulut.github.io/iptv/playlists/category/science.m3u","dearbulut-EGITIM":"https://dearbulut.github.io/iptv/playlists/category/education.m3u","dearbulut-ISVEC_DILI":"https://dearbulut.github.io/iptv/playlists/language/swe.m3u","dearbulut-ARAPCA":"https://dearbulut.github.io/iptv/playlists/language/ara.m3u","dearbulut-country-us":"https://dearbulut.github.io/iptv/playlists/country/us.m3u","dearbulut-country-in":"https://dearbulut.github.io/iptv/playlists/country/in.m3u","dearbulut-country-ru":"https://dearbulut.github.io/iptv/playlists/country/ru.m3u","dearbulut-country-br":"https://dearbulut.github.io/iptv/playlists/country/br.m3u","dearbulut-country-it":"https://dearbulut.github.io/iptv/playlists/country/it.m3u","dearbulut-country-es":"https://dearbulut.github.io/iptv/playlists/country/es.m3u","dearbulut-country-do":"https://dearbulut.github.io/iptv/playlists/country/do.m3u","dearbulut-country-cl":"https://dearbulut.github.io/iptv/playlists/country/cl.m3u","dearbulut-country-uk":"https://dearbulut.github.io/iptv/playlists/country/uk.m3u","dearbulut-country-fr":"https://dearbulut.github.io/iptv/playlists/country/fr.m3u","dearbulut-country-ua":"https://dearbulut.github.io/iptv/playlists/country/ua.m3u","dearbulut-country-ar":"https://dearbulut.github.io/iptv/playlists/country/ar.m3u","dearbulut-country-mx":"https://dearbulut.github.io/iptv/playlists/country/mx.m3u","dearbulut-country-pe":"https://dearbulut.github.io/iptv/playlists/country/pe.m3u","dearbulut-country-cn":"https://dearbulut.github.io/iptv/playlists/country/cn.m3u","dearbulut-country-ro":"https://dearbulut.github.io/iptv/playlists/country/ro.m3u","dearbulut-country-hu":"https://dearbulut.github.io/iptv/playlists/country/hu.m3u","dearbulut-country-ca":"https://dearbulut.github.io/iptv/playlists/country/ca.m3u","dearbulut-country-id":"https://dearbulut.github.io/iptv/playlists/country/id.m3u","dearbulut-country-pl":"https://dearbulut.github.io/iptv/playlists/country/pl.m3u","dearbulut-country-ir":"https://dearbulut.github.io/iptv/playlists/country/ir.m3u","dearbulut-country-co":"https://dearbulut.github.io/iptv/playlists/country/co.m3u","dearbulut-country-pk":"https://dearbulut.github.io/iptv/playlists/country/pk.m3u","dearbulut-country-ec":"https://dearbulut.github.io/iptv/playlists/country/ec.m3u","dearbulut-country-vn":"https://dearbulut.github.io/iptv/playlists/country/vn.m3u","dearbulut-country-hn":"https://dearbulut.github.io/iptv/playlists/country/hn.m3u","dearbulut-country-th":"https://dearbulut.github.io/iptv/playlists/country/th.m3u","dearbulut-country-kr":"https://dearbulut.github.io/iptv/playlists/country/kr.m3u","dearbulut-country-gr":"https://dearbulut.github.io/iptv/playlists/country/gr.m3u","dearbulut-country-ve":"https://dearbulut.github.io/iptv/playlists/country/ve.m3u","dearbulut-country-bo":"https://dearbulut.github.io/iptv/playlists/country/bo.m3u","dearbulut-country-cz":"https://dearbulut.github.io/iptv/playlists/country/cz.m3u","dearbulut-country-cr":"https://dearbulut.github.io/iptv/playlists/country/cr.m3u","dearbulut-country-gt":"https://dearbulut.github.io/iptv/playlists/country/gt.m3u","dearbulut-country-bg":"https://dearbulut.github.io/iptv/playlists/country/bg.m3u","dearbulut-country-py":"https://dearbulut.github.io/iptv/playlists/country/py.m3u","dearbulut-country-sk":"https://dearbulut.github.io/iptv/playlists/country/sk.m3u","dearbulut-country-pt":"https://dearbulut.github.io/iptv/playlists/country/pt.m3u","dearbulut-country-il":"https://dearbulut.github.io/iptv/playlists/country/il.m3u","dearbulut-country-sa":"https://dearbulut.github.io/iptv/playlists/country/sa.m3u","dearbulut-country-iq":"https://dearbulut.github.io/iptv/playlists/country/iq.m3u","dearbulut-country-ng":"https://dearbulut.github.io/iptv/playlists/country/ng.m3u","dearbulut-country-rs":"https://dearbulut.github.io/iptv/playlists/country/rs.m3u","dearbulut-country-kz":"https://dearbulut.github.io/iptv/playlists/country/kz.m3u","dearbulut-country-sv":"https://dearbulut.github.io/iptv/playlists/country/sv.m3u","dearbulut-country-au":"https://dearbulut.github.io/iptv/playlists/country/au.m3u","dearbulut-country-ke":"https://dearbulut.github.io/iptv/playlists/country/ke.m3u","dearbulut-country-ae":"https://dearbulut.github.io/iptv/playlists/country/ae.m3u","dearbulut-country-mn":"https://dearbulut.github.io/iptv/playlists/country/mn.m3u","dearbulut-country-uz":"https://dearbulut.github.io/iptv/playlists/country/uz.m3u","dearbulut-country-lb":"https://dearbulut.github.io/iptv/playlists/country/lb.m3u","dearbulut-country-ch":"https://dearbulut.github.io/iptv/playlists/country/ch.m3u","dearbulut-country-pr":"https://dearbulut.github.io/iptv/playlists/country/pr.m3u","dearbulut-country-bd":"https://dearbulut.github.io/iptv/playlists/country/bd.m3u","dearbulut-country-kh":"https://dearbulut.github.io/iptv/playlists/country/kh.m3u","dearbulut-country-tw":"https://dearbulut.github.io/iptv/playlists/country/tw.m3u","dearbulut-country-mk":"https://dearbulut.github.io/iptv/playlists/country/mk.m3u","dearbulut-country-sg":"https://dearbulut.github.io/iptv/playlists/country/sg.m3u","dearbulut-country-fi":"https://dearbulut.github.io/iptv/playlists/country/fi.m3u","dearbulut-country-za":"https://dearbulut.github.io/iptv/playlists/country/za.m3u","dearbulut-country-pa":"https://dearbulut.github.io/iptv/playlists/country/pa.m3u","dearbulut-country-hr":"https://dearbulut.github.io/iptv/playlists/country/hr.m3u","dearbulut-country-my":"https://dearbulut.github.io/iptv/playlists/country/my.m3u","dearbulut-country-md":"https://dearbulut.github.io/iptv/playlists/country/md.m3u","dearbulut-country-ge":"https://dearbulut.github.io/iptv/playlists/country/ge.m3u","dearbulut-country-ug":"https://dearbulut.github.io/iptv/playlists/country/ug.m3u","dearbulut-country-al":"https://dearbulut.github.io/iptv/playlists/country/al.m3u","dearbulut-country-hk":"https://dearbulut.github.io/iptv/playlists/country/hk.m3u","dearbulut-country-ee":"https://dearbulut.github.io/iptv/playlists/country/ee.m3u","dearbulut-country-ps":"https://dearbulut.github.io/iptv/playlists/country/ps.m3u","dearbulut-country-jo":"https://dearbulut.github.io/iptv/playlists/country/jo.m3u","dearbulut-country-ni":"https://dearbulut.github.io/iptv/playlists/country/ni.m3u","dearbulut-country-mm":"https://dearbulut.github.io/iptv/playlists/country/mm.m3u","dearbulut-country-ci":"https://dearbulut.github.io/iptv/playlists/country/ci.m3u","dearbulut-country-si":"https://dearbulut.github.io/iptv/playlists/country/si.m3u","dearbulut-country-by":"https://dearbulut.github.io/iptv/playlists/country/by.m3u","dearbulut-country-eg":"https://dearbulut.github.io/iptv/playlists/country/eg.m3u","dearbulut-country-qa":"https://dearbulut.github.io/iptv/playlists/country/qa.m3u","dearbulut-country-cd":"https://dearbulut.github.io/iptv/playlists/country/cd.m3u","dearbulut-country-lt":"https://dearbulut.github.io/iptv/playlists/country/lt.m3u","dearbulut-country-ba":"https://dearbulut.github.io/iptv/playlists/country/ba.m3u","dearbulut-country-sn":"https://dearbulut.github.io/iptv/playlists/country/sn.m3u","dearbulut-country-cm":"https://dearbulut.github.io/iptv/playlists/country/cm.m3u","dearbulut-country-lk":"https://dearbulut.github.io/iptv/playlists/country/lk.m3u","dearbulut-country-af":"https://dearbulut.github.io/iptv/playlists/country/af.m3u","dearbulut-country-tj":"https://dearbulut.github.io/iptv/playlists/country/tj.m3u","dearbulut-country-ph":"https://dearbulut.github.io/iptv/playlists/country/ph.m3u","dearbulut-country-ht":"https://dearbulut.github.io/iptv/playlists/country/ht.m3u","dearbulut-country-kg":"https://dearbulut.github.io/iptv/playlists/country/kg.m3u","dearbulut-country-dk":"https://dearbulut.github.io/iptv/playlists/country/dk.m3u","dearbulut-country-lv":"https://dearbulut.github.io/iptv/playlists/country/lv.m3u","dearbulut-country-tg":"https://dearbulut.github.io/iptv/playlists/country/tg.m3u","dearbulut-country-lu":"https://dearbulut.github.io/iptv/playlists/country/lu.m3u","dearbulut-country-aw":"https://dearbulut.github.io/iptv/playlists/country/aw.m3u","dearbulut-country-kw":"https://dearbulut.github.io/iptv/playlists/country/kw.m3u","dearbulut-country-nz":"https://dearbulut.github.io/iptv/playlists/country/nz.m3u","dearbulut-country-ie":"https://dearbulut.github.io/iptv/playlists/country/ie.m3u","dearbulut-country-xk":"https://dearbulut.github.io/iptv/playlists/country/xk.m3u","dearbulut-country-gh":"https://dearbulut.github.io/iptv/playlists/country/gh.m3u","dearbulut-country-bj":"https://dearbulut.github.io/iptv/playlists/country/bj.m3u","dearbulut-country-sy":"https://dearbulut.github.io/iptv/playlists/country/sy.m3u","dearbulut-country-mv":"https://dearbulut.github.io/iptv/playlists/country/mv.m3u","dearbulut-language-eng":"https://dearbulut.github.io/iptv/playlists/language/eng.m3u","dearbulut-language-spa":"https://dearbulut.github.io/iptv/playlists/language/spa.m3u","dearbulut-language-rus":"https://dearbulut.github.io/iptv/playlists/language/rus.m3u","dearbulut-language-por":"https://dearbulut.github.io/iptv/playlists/language/por.m3u","dearbulut-language-fra":"https://dearbulut.github.io/iptv/playlists/language/fra.m3u","dearbulut-language-hin":"https://dearbulut.github.io/iptv/playlists/language/hin.m3u","dearbulut-language-ita":"https://dearbulut.github.io/iptv/playlists/language/ita.m3u","dearbulut-language-deu":"https://dearbulut.github.io/iptv/playlists/language/deu.m3u","dearbulut-language-zho":"https://dearbulut.github.io/iptv/playlists/language/zho.m3u","dearbulut-language-fas":"https://dearbulut.github.io/iptv/playlists/language/fas.m3u","dearbulut-language-nld":"https://dearbulut.github.io/iptv/playlists/language/nld.m3u","dearbulut-language-ukr":"https://dearbulut.github.io/iptv/playlists/language/ukr.m3u","dearbulut-language-ron":"https://dearbulut.github.io/iptv/playlists/language/ron.m3u","dearbulut-language-dan":"https://dearbulut.github.io/iptv/playlists/language/dan.m3u","dearbulut-language-hun":"https://dearbulut.github.io/iptv/playlists/language/hun.m3u","dearbulut-language-ind":"https://dearbulut.github.io/iptv/playlists/language/ind.m3u","dearbulut-language-tam":"https://dearbulut.github.io/iptv/playlists/language/tam.m3u","dearbulut-language-pol":"https://dearbulut.github.io/iptv/playlists/language/pol.m3u","dearbulut-language-nor":"https://dearbulut.github.io/iptv/playlists/language/nor.m3u","dearbulut-language-ben":"https://dearbulut.github.io/iptv/playlists/language/ben.m3u","dearbulut-language-vie":"https://dearbulut.github.io/iptv/playlists/language/vie.m3u"}

# Only explicitly approved sources may be scanned. The registry is checked again
# here so invoking the script outside Actions cannot bypass the approval gate.
def approved_sources():
    registry_path = pathlib.Path(__file__).resolve().with_name("k2_kaynak_onaylari.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("schema_version") != 1 or not isinstance(registry.get("sources"), dict):
        raise RuntimeError("Invalid K2 source approval registry")
    selected = {}
    for source_id, entry in registry["sources"].items():
        if source_id not in SOURCES or not isinstance(entry, dict):
            raise RuntimeError("Unknown K2 approval entry")
        if entry.get("url") != SOURCES[source_id]:
            raise RuntimeError("K2 approval URL mismatch")
        if entry.get("status") == "ONAYLI":
            if not all(isinstance(entry.get(k), str) and entry[k].strip()
                       for k in ("approved_by", "approved_at", "evidence")):
                raise RuntimeError("K2 source approval evidence missing")
            selected[source_id] = SOURCES[source_id]
        elif entry.get("status") != "BEKLIYOR":
            raise RuntimeError("Invalid K2 source status")
    if any(not isinstance(url, str) or urllib.parse.urlsplit(url).scheme not in ("https", "http") or not urllib.parse.urlsplit(url).hostname for url in SOURCES.values()):
        raise RuntimeError("Invalid K2 discovery source URL")
    if len(set(SOURCES.values())) != len(SOURCES):
        raise RuntimeError("Duplicate K2 discovery source URLs")
    if not selected:
        raise RuntimeError("No approved K2 discovery sources")
    return selected

SOURCES = approved_sources()

RESEARCH_SOURCES={"uydufrekans-TURKSAT-SIFRESIZ":"https://www.uydufrekans.com.tr/turksat-sifresiz-kanallar.html"}
def research_report():
 rows=[]
 for src,url in RESEARCH_SOURCES.items():
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=18) as response:
    body=response.read(3000000).decode("utf-8",errors="replace")
   rows.append(dict(kaynak=src,url=url,durum="ERISILDI",tur="KANAL_ADI_VE_UYDU_FREKANSI",hata="",notlar="IPTV akis kaniti degildir; frekanslar yayin URLsi sayilmaz."))
  except Exception as e:
   rows.append(dict(kaynak=src,url=url,durum="ERISILEMEDI",tur="KANAL_ADI_VE_UYDU_FREKANSI",hata=str(e)[:120],notlar="IPTV akis kaniti degildir."))
 write("arastirma_kaynaklari.csv",rows,["kaynak","url","durum","tur","hata","notlar"])
def source_freshness(url):
 """GitHub source-file commit date, not stream uptime or verified channel freshness."""
 p=urllib.parse.urlsplit(url); parts=p.path.strip("/").split("/")
 if p.netloc!="raw.githubusercontent.com" or len(parts)<4:return ("BILINMIYOR","",99999)
 owner,repo,branch=parts[:3];path="/".join(parts[3:])
 api="https://api.github.com/repos/"+owner+"/"+repo+"/commits?path="+urllib.parse.quote(path)+"&per_page=1"
 try:
  req=urllib.request.Request(api,headers={"User-Agent":"MADSC-TV","Accept":"application/vnd.github+json"})
  with urllib.request.urlopen(req,timeout=8) as r:data=json.load(r)
  stamp=data[0]["commit"]["committer"]["date"]
  days=max(0,(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(stamp.replace("Z","+00:00"))).days)
  return ("SON_1_GUN" if days<=1 else "SON_7_GUN" if days<=7 else "SON_15_GUN" if days<=15 else "SON_30_GUN" if days<=30 else "ESKI",stamp,days)
 except Exception:return ("BILINMIYOR","",99999)
def parse(s):
 lines=s.splitlines(); out=[]
 for i,line in enumerate(lines):
  if not line.startswith("#EXTINF"): continue
  for nextline in lines[i+1:i+4]:
   if nextline.startswith("#EXTINF"):break
   if nextline.startswith(("http://","https://")):
    def attr(k):
     m=re.search(k+'="([^"]*)"',line);return m.group(1) if m else ""
    out.append(dict(name=line.rsplit(",",1)[-1].strip(),url=nextline.strip(),logo=attr("tvg-logo"),id=attr("tvg-id"),group=attr("group-title")))
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
 research_report()
 master=pathlib.Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig");base=parse(master)
 for f in ("YENILER.m3u","MADSC_TV_47_LISTE_ADAY.m3u"):
  if pathlib.Path(f).exists():base+=parse(pathlib.Path(f).read_text(encoding="utf-8-sig"))
 known={key(x["url"]) for x in base};ids={x["id"].lower() for x in base if x["id"]};names={name(x["name"]) for x in base}
 state=OUT/"gecmis.json"
 # Never forget previous tests when history is unreadable.
 history=json.loads(state.read_text(encoding="utf-8")).get("history")
 if not isinstance(history,dict):raise RuntimeError("Invalid discovery history; scanning stopped")
 # Only unfinished main-playlist checks, at least six hours apart.
 # Independent state: three successful checks >=6 hours apart.
 audit_state=OUT/"ana_liste_test_gecmisi.json"
 try:audit=json.loads(audit_state.read_text(encoding="utf-8")).get("channels",{})
 except Exception:audit={}
 if not isinstance(audit,dict):audit={}
 audit_now=datetime.datetime.now(datetime.timezone.utc)
 unique={}
 for idx,ch in enumerate(parse(master)):
  uid=str(idx+1)+"|"+key(ch["url"])
  unique[uid]=ch
 audit={k:v for k,v in audit.items() if k in unique}
 def health_check_due(previous):
  if int(previous.get("successful_runs",0))>=3:return False
  last=previous.get("last_test")
  if not last:return True
  try:return (audit_now-datetime.datetime.fromisoformat(last)).total_seconds()>=6*3600
  except (ValueError,TypeError):return False
 due=sorted((uid for uid in unique if health_check_due(audit.get(uid,{}))),key=lambda k:(audit.get(k,{}).get("last_test",""),k))

 def audit_one(uid):
  ch=unique[uid];v,a,res=probe(ch["url"]);return uid,bool(v and a),res
 with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
  checks=list(ex.map(audit_one,due))
 for uid,ok,res in checks:
  prev=audit.get(uid,{})
  last=prev.get("last_success")
  try:gap=(audit_now-datetime.datetime.fromisoformat(last)).total_seconds()/3600 if last else None
  except Exception:gap=None
  streak=int(prev.get("successful_runs",0))
  if ok and (gap is None or gap>=6):streak+=1;prev["last_success"]=audit_now.isoformat()
  if not ok:streak=0;prev["last_success"]=None
  prev.update(last_test=audit_now.isoformat(),successful_runs=streak,last_result="TEKNIK_GECTI" if ok else "TEKNIK_GECEMEDI",resolution=res)
  audit[uid]=prev
 audit_rows=[]
 for uid,ch in unique.items():
  a=audit.get(uid,{})
  status=("UC_TEST_GECTI" if a.get("successful_runs",0)>=3 else "TEKRAR_TEST_BEKLIYOR") if a.get("last_result")=="TEKNIK_GECTI" else ("TEKNIK_GECEMEDI_YENIDEN_BAKILACAK" if a.get("last_result") else "HENUZ_TEST_EDILMEDI")
  audit_rows.append(dict(sira=uid.split("|",1)[0],kanal=ch["name"],kategori=ch.get("group",""),url=ch["url"],durum=status,basarili_ayri_test=a.get("successful_runs",0),son_test=a.get("last_test",""),cozunurluk=a.get("resolution",""),kullanici_karari="DEGISTIRILMEDI"))
 write("ana_liste_saglik_raporu.csv",audit_rows,["sira","kanal","kategori","url","durum","basarili_ayri_test","son_test","cozunurluk","kullanici_karari"])
 write("ana_liste_calismayanlar.csv",[x for x in audit_rows if x["durum"]=="TEKNIK_GECEMEDI_YENIDEN_BAKILACAK"],["sira","kanal","kategori","url","durum","basarili_ayri_test","son_test","cozunurluk","kullanici_karari"])
 print(json.dumps({"ana_liste_toplam":len(audit_rows),"kontrol_edilen":len(checks),"teknik_gecemeyen":sum(x["durum"]=="TEKNIK_GECEMEDI_YENIDEN_BAKILACAK" for x in audit_rows)},ensure_ascii=False))
 audit_state.write_text(json.dumps({"channels":audit},ensure_ascii=False,indent=2),encoding="utf-8")
 # Previously failing URLs remain eligible for periodic recovery checks.
 failed_archive=OUT/"eski_bozuk_linkler.csv"
 found=[];errors=[]
 freshness={src:source_freshness(url) for src,url in SOURCES.items()}
 write("kaynak_guncelligi.csv",[dict(kaynak=k,url=SOURCES[k],guncellik=v[0],son_guncelleme=v[1],gun=v[2] if v[2]!=99999 else "") for k,v in freshness.items()],["kaynak","url","guncellik","son_guncelleme","gun"])
 # Check source reachability concurrently; never treat a configured URL as a verified source.
 def fetch_source(item):
  src,url=item
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"MADSC-TV"}),timeout=18) as r:
    body=r.read(3000000).decode("utf-8-sig",errors="replace")
   channels=parse(body)
   return src,channels,"" if body.lstrip().startswith("#EXTM3U") else "M3U_BASLIGI_YOK"
  except Exception as e:return src,[],str(e)[:120]
 # Daily discovery: retain all configured sources for audit. A bounded set
 # of foreign feeds is eligible for candidate review, never direct playlist insertion.
 # Diaspora stations may be hosted abroad; source hostname is not station identity.
 def turkish_feed(src):
  # Turkish feeds plus three approved foreign candidate feeds. Other sources
  # remain configured, but are not automatically ingested.
  return src in {
   "iptv-turk-tr-EK-KAYNAK", "iptv-org-TR", "iptv-org-TURKIYE",
   "iptv-org-TURKCE", "omerdenizhan-TR", "ilyswch-TR",
   "itasli-TR", "gkhncksn-TR", "Lunedor-TR",
   "dearbulut-TR", "dearbulut-TURKCE",
   # Ayrik yabanci aday kesfi: kaynak ulkesi kimlik kaniti degildir.
   "dearbulut-ISVEC", "dearbulut-ALMANYA",
   "dearbulut-language-eng"
  }
 ordered=sorted(((k,v) for k,v in SOURCES.items() if turkish_feed(k)),key=lambda item:freshness[item[0]][2])
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
  source_results=list(ex.map(fetch_source,ordered))
 source_rows=[]
 for src,channels,error in source_results:
  status="ERISILEMEDI" if error and not channels else "BOS_VEYA_GECERSIZ" if not channels else "ERISILDI"
  source_rows.append(dict(kaynak=src,url=SOURCES[src],durum=status,kanal_sayisi=len(channels),hata=error))
  if error:errors.append(src+": "+error)
  for x in channels:x["source"]=src;found.append(x)
 write("kaynak_erisim_raporu.csv",source_rows,["kaynak","url","durum","kanal_sayisi","hata"])
 # Include historical failed URLs even if discovery sources stop listing them.
 for old_url,old in history.items():
  if int(old.get("runs",0))>0 and int(old.get("successful_runs",0))==0 and old.get("url"):
   found.append(dict(name=old.get("channel","Bilinmeyen"),url=old["url"],logo="",id="",source="GECMIS_BASARISIZ_YENIDEN_TEST"))
 pending=[];duplicates=[];seen=set()
 for x in found:
  k=key(x["url"])
  why="AYNI_URL" if k in known and x["source"]!="GECMIS_BASARISIZ_YENIDEN_TEST" else "AYNI_TARAMA" if k in seen else ""
  if why:duplicates.append(dict(kanal=x["name"],url=x["url"],neden=why))
  else:seen.add(k);pending.append(x)
 # Her otomatik turda daha fazla, daha once denenmemis adayi test et.
 limit=240
 pending.sort(key=lambda x:(int(history.get(key(x["url"]),{}).get("runs",0)) > 0, freshness.get(x["source"],("","",99999))[2], history.get(key(x["url"]),{}).get("last_test",""), x["name"]))
 # Never repeat a previously tested URL while untested candidates remain.
 untested=[x for x in pending if int(history.get(key(x["url"]),{}).get("runs",0)) == 0]
 tested=[x for x in pending if int(history.get(key(x["url"]),{}).get("runs",0)) > 0]
 pending=untested  # Discovery never retests historical candidates.
 # Keep public artwork metadata separate from stream URLs and playlist writes.
 from scripts.candidate_logo_report import public_artwork_url
 artwork=[]
 for x in pending:
  logo_url=x.get("logo", "")
  allowed=public_artwork_url(logo_url)
  artwork.append(dict(channel=x["name"],stream_sha256=__import__("hashlib").sha256(key(x["url"]).encode()).hexdigest(),source=x["source"],channel_id=x.get("id",""),logo_url=logo_url if allowed else "",logo_source_review_required=bool(logo_url and not allowed)))
 (OUT/"logo_candidates.json").write_text(json.dumps(artwork,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 # Prepare candidate PNG artwork in the same discovery run, without changing playlists.
 # Source artwork is not proof of channel identity; all matches remain review-pending.
 try:
  from scripts.candidate_logo_report import prepare as prepare_candidate_artwork
  previous_path=OUT/"candidate_logos.json"
  previous=json.loads(previous_path.read_text(encoding="utf-8")).get("results",[]) if previous_path.exists() else []
  prepared=prepare_candidate_artwork(artwork,previous,limit=40)
  previous_path.write_text(json.dumps({"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":prepared,"limits":"PNG preparation only; visual identity and IBO approval required. No playlist edits."},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"candidate_logos_review":len(prepared),"png_ready":sum(x.get("status")=="PNG_READY_REVIEW_PENDING" for x in prepared)},ensure_ascii=False))
 except Exception as exc:
  (OUT/"logo_hazirlama_hatasi.txt").write_text(type(exc).__name__+": "+str(exc)[:300]+"\n",encoding="utf-8")
  print("Candidate logo preparation failed; discovery and channel tests continue.")
 # A PNG conversion error must not suppress the missing-logo inventory.
 from scripts.candidate_logo_missing_report import build as build_missing_logo_report
 prepared_for_inventory=locals().get("prepared",[])
 missing_report=build_missing_logo_report(artwork,prepared_for_inventory)
 (OUT/"candidate_logo_missing_report.json").write_text(json.dumps(missing_report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"logo_aday_sayisi":missing_report["total_candidates"],"logo_durumlari":missing_report["category_counts"]},ensure_ascii=False))
 print(json.dumps({"yeni_bekleyen":len(untested),"onceki_testli":len(tested),"bu_tur_yeni":min(limit,len(untested))},ensure_ascii=False))
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:rows=list(ex.map(test,pending[:limit]))
 for x in pending[limit:]:rows.append(dict(kanal=x["name"],url=x["url"],kaynak=x["source"],durum="SONRAKI_TEST_BEKLIYOR",puan=0,video="",ses="",cozunurluk="",logo="",ulke="ISVEC_DOGRULANMADI",test1="",test2=""))
 rows.sort(key=lambda r:(-r["puan"],r["kanal"]))
 write("adaylar.csv",rows,["kanal","url","kaynak","durum","puan","video","ses","cozunurluk","logo","ulke","test1","test2"])
 write("tekrarlar.csv",duplicates,["kanal","url","neden"])
 write("eski_bozuk_linkler.csv",[dict(kanal=v.get("channel",""),url=v.get("url",k),durum="YENIDEN_TEST_ARSIVI") for k,v in history.items() if int(v.get("runs",0))>0 and int(v.get("successful_runs",0))==0],["kanal","url","durum"])
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
  # Source provenance is not station identity proof.
  prev.setdefault("source_history", [])
  if row["kaynak"] not in prev["source_history"]:
   prev["source_history"].append(row["kaynak"])
  # A retry label is not the original feed. Preserve provenance across retries.
  if row["kaynak"]!="GECMIS_BASARISIZ_YENIDEN_TEST":
   prev["source_id"]=row["kaynak"]
  if row["kaynak"] in {"iptv-org-TURKCE","dearbulut-TURKCE"}:
   prev["source_language_hint"]="tur"
  elif row["kaynak"] in {"dearbulut-ISVEC","dearbulut-ALMANYA","dearbulut-language-eng"}:
   prev["source_language_hint"]="FOREIGN_SOURCE_UNVERIFIED"
  else:
   prev.setdefault("source_language_hint","UNKNOWN")
  # ffprobe basarisizligi IBO/alternatif oynaticida acilmayacagi anlamina gelmez.
  # Bu otomasyon IBO testi yapmaz; basarisizlari kesin calismiyor saymaz.
  row["durum"]=("UC_AYRI_ZAMAN_TESTI_GECTI_ONAY_BEKLIYOR" if prev["successful_runs"]>=3 else "FARKLI_SAATTE_TEKRAR_TEST_BEKLIYOR") if passed else "FFPROBE_GECMEDI_PLAYER_UYUMLULUGU_BELIRSIZ"
  history[k]=prev
 write("adaylar.csv",rows,["kanal","url","kaynak","durum","puan","video","ses","cozunurluk","logo","ulke","test1","test2"])
 write("player_uyumlulugu_belirsiz.csv",
       [dict(kanal=row["kanal"],url=row["url"],kaynak=row["kaynak"],durum=row["durum"],notlar="ffprobe sonucu IBO oynatma kaniti veya kesin basarisizlik degildir; cihaz testi bu otomasyonda yapilmaz")
        for row in rows if row["durum"]=="FFPROBE_GECMEDI_PLAYER_UYUMLULUGU_BELIRSIZ"],
       ["kanal","url","kaynak","durum","notlar"])
 # High-resolution alternatives are only reported, never inserted into playlists.
 def quality(res):
  try:w,h=map(int,res.split("x"))
  except Exception:return "BELIRSIZ"
  return "4K_UHD" if w>=3840 and h>=2160 else "QHD" if w>=2560 and h>=1440 else "FHD" if w>=1920 and h>=1080 else "HD" if w>=1280 and h>=720 else "SD"
 quality_rows=[]
 for row in rows:
  if row["durum"]=="SONRAKI_TEST_BEKLIYOR":continue
  q=quality(row["cozunurluk"])
  if q in ("FHD","QHD","4K_UHD"):
   quality_rows.append(dict(kanal=row["kanal"],url=row["url"],cozunurluk=row["cozunurluk"],kalite=q,durum=row["durum"],islem="MEVCUT_KANAL_ALTERNATIFI" if name(row["kanal"]) in names else "YENI_KANAL_ADAYI"))
 write("yuksek_kalite_alternatifleri.csv",quality_rows,["kanal","url","cozunurluk","kalite","durum","islem"])
 state.write_text(json.dumps({"history":history},ensure_ascii=False,indent=2))
 summary=dict(yeni_bekleyen_sonraki=max(0,len(untested)-min(limit,len(untested))),zaman=datetime.datetime.now(datetime.timezone.utc).isoformat(),ana_liste=len(parse(master)),kaynaklar=SOURCES,kaynak_hedefi=SOURCE_TARGET,tanimli_kaynak_sayisi=len(SOURCES),kaynak_hedef_farki=len(SOURCES)-SOURCE_TARGET,taranan_turkce_kaynak_sayisi=len(ordered),kaynak_guncelligi={k:v[0] for k,v in freshness.items()},bulunan=len(found),tekrar=len(duplicates),aday=len(pending),test_edilen=min(limit,len(pending)),teknik_gecen=sum(x["durum"]=="UC_AYRI_ZAMAN_TESTI_GECTI_ONAY_BEKLIYOR" for x in rows),alternatif=len(alternatives),hatalar=errors,notlar="Ana liste degismedi. Farkli gun testleri ve Isvec erisimi bu kosuda dogrulanamaz. Kimlik onayi gerekir.")
 (OUT/"ozet.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()

# Initial integrated discovery validation trigger
# Manual continuation requested: main-list health audit next batch

# Manual unified channel discovery requested 2026-10-11

# User requested unified discovery scan on 2026-10-11 at 02:40 Europe/Stockholm; playlist unchanged.

# User requested 155-source scan on 2026-10-11; triggers discovery workflow via push.

# Re-run 155-source discovery after report-save checkout fix (2026-10-11).

# Continue candidate stream verification, 2026-10-11.

# Continue staged 155-source candidate verification on 2026-10-11; no playlist changes.

# Yeni 155 kaynak aday test turu - 2026-10-11 10:26 Europe/Stockholm.

# Trigger next candidate verification run after workflow syntax fix, 2026-10-11.

# User-requested new candidate discovery scan, 2026-10-12; preserve playlist and prior test history.
