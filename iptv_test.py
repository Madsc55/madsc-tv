#!/usr/bin/env python3
import csv
import json
import re
import subprocess
import sys
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

EPG_URL = "https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HTTP_TIMEOUT = 7
PROBE_TIMEOUT = 15
MAX_WORKERS = 10
MAX_CANDIDATES = 10
DISCOVERY_SOURCES = [
    ("IPTV_ORG", "https://iptv-org.github.io/iptv/countries/tr.m3u"),
]
BLOCKED_URL_PARTS = ("helga.iptv2022.com", "onureroz.com")
GROUP_ORDER = ["⭐ FAVORİLER", "ULUSAL", "HABER", "SPOR", "ALTERNATİF", "ÇOCUK", "BELGESEL", "DİNİ", "MÜZİK", "SİNEMA-DİZİ", "EĞİTİM-KÜLTÜR", "KAMU-TEMATİK", "İNTERNET"]
DEFAULT_FAVORITES = ["TRT 1", "ATV", "KANAL D", "SHOW TV", "STAR TV", "NOW", "TV8", "KANAL 7", "SÖZCÜ TV", "TV100", "NTV", "CNN TÜRK", "TRT HABER", "HABERTÜRK", "HABER GLOBAL", "TRT SPOR", "A SPOR"]

# Yalnızca ücretsiz/açık ve ülke çapında kullanılmasını istediğimiz kanallar.
# urls alanı başlangıç adaylarıdır; başlangıç listesi, dünkü CALISANLAR ve keşif kaynağı da eklenir.
CHANNELS = {
"TRT 1": ("ULUSAL", "af0zo9et4xguwsk", ["https://tv-trt1.medya.trt.com.tr/master_1080.m3u8", "https://tv-trt1.medya.trt.com.tr/master_720.m3u8", "https://tv-trt1.medya.trt.com.tr/master.m3u8"]),
"ATV": ("ULUSAL", "2zkzbuscxwyjc4k", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8", "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv.m3u8"]),
"KANAL D": ("ULUSAL", "bbwgmhsmhhoatzg", ["https://demiroren.daioncdn.net/kanald/kanald.m3u8?app=kanald_web&ce=3", "https://demiroren-live.daioncdn.net/kanald/kanald_1080p.m3u8"]),
"SHOW TV": ("ULUSAL", "pvr08e5grfsebfw", ["https://ciner-live.daioncdn.net/showtv/showtv_1080p.m3u8", "https://ciner-live.daioncdn.net/showtv/showtv_720p.m3u8", "https://ciner-live.daioncdn.net/showtv/showtv.m3u8"]),
"STAR TV": ("ULUSAL", "75tz02ooforewap", ["https://dogus-live.daioncdn.net/startv/startv_720p.m3u8", "https://dogus-live.daioncdn.net/startv/startv.m3u8"]),
"NOW": ("ULUSAL", "m0abaihy7vla6ma", ["https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8", "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv_720p.m3u8"]),
"TV8": ("ULUSAL", "w7x32brlcz26ibb", ["https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/tv8/tv8_1080p.m3u8", "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/tv8/tv8.m3u8"]),
"KANAL 7": ("ULUSAL", "a8t877hb0oandbv", ["https://kanal7-live.daioncdn.net/kanal7/kanal7_1080p.m3u8"]),
"BEYAZ TV": ("ULUSAL", "edf3lp61qexxxhl", ["https://beyaztv-live.daioncdn.net/beyaztv/beyaztv_1080p.m3u8", "https://beyaztv-live.daioncdn.net/beyaztv/beyaztv.m3u8"]),
"360": ("ULUSAL", "cphtdpl9j70cn3a", ["https://turkmedya-live.ercdn.net/tv360/tv360_1080p.m3u8", "https://turkmedya-live.ercdn.net/tv360/tv360.m3u8"]),
"A2": ("ULUSAL", "fc29p3wbp8wkgo4", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/a2tv/a2tv_1080p.m3u8"]),
"TEVE2": ("ULUSAL", "6vs4sg9183gdxth", ["https://demiroren-live.daioncdn.net/teve2/teve2_1080p.m3u8"]),
"DMAX": ("ULUSAL", "6sokobdd9dwe0gl", ["https://dogus-live.daioncdn.net/dmax/dmax_720p.m3u8"]),
"TLC": ("ULUSAL", "9z32hgan37zhgr6", ["https://dogus-live.daioncdn.net/tlc/tlc_720p.m3u8"]),
"TV8.5": ("ULUSAL", "pd29xh24glvq4qz", ["https://tv8.daioncdn.net/tv8bucuk/tv8bucuk_1080p.m3u8?app=tv8bucuk_web&ce=3"]),
"TRT 2": ("ULUSAL", "nzdc0yd5xxv43yl", ["https://tv-trt2.medya.trt.com.tr/master.m3u8", "https://tv-trt2.medya.trt.com.tr/master_720.m3u8"]),
"SÖZCÜ TV": ("HABER", "5zoe73avn97ggnt", ["https://szctvdvr.blutv.com/blutv_szctv_dvr/live_720p4350000kbps/index.m3u8", "http://5.178.103.239:55/yt1/szctv.m3u8"]),
"TV100": ("HABER", "5i5mds6ap6h7m7w", ["https://tv100-live.daioncdn.net/tv100/tv100_1080p.m3u8"]),
"NTV": ("HABER", "nyz5s8p798n9cqg", ["https://dogus.daioncdn.net/ntv/ntv_1080p.m3u8"]),
"CNN TÜRK": ("HABER", "ah7mr9ol040kp3b", ["https://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/playlist.m3u8"]),
"TRT HABER": ("HABER", "in3p7jng04mr97m", ["https://tv-trthaber.medya.trt.com.tr/master_720p.m3u8"]),
"HABERTÜRK": ("HABER", "gil1w2erz9l7imc", ["https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/haberturktv/haberturktv_1080p.m3u8"]),
"HABER GLOBAL": ("HABER", "bwmpobxuqn2pz87", ["https://ensonhaber-live.ercdn.net/haberglobal/haberglobal_720p.m3u8"]),
"HALK TV": ("HABER", "d1exl1gxity48nl", ["https://halktv-live.daioncdn.net/halktv/halktv_1080p.m3u8"]),
"TGRT HABER": ("HABER", "qz2fp61itc8xm4g", ["https://canli.tgrthaber.com/tgrt.m3u8", "https://tgrthaber-live.daioncdn.net/tgrthaber/tgrthaber_1080p.m3u8"]),
"A HABER": ("HABER", "ql8qf4vb46o1h7t", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/ahaber/ahaber_1080p.m3u8"]),
"24": ("HABER", "9b7ltozvb9c333g", ["https://turkmedya-live.ercdn.net/tv24/tv24_1080p.m3u8"]),
"EKOL TV": ("HABER", "3kluptlla8k8re0", ["https://ekoltv-live.ercdn.net/ekoltv/ekoltv_1080p.m3u8"]),
"TELE1": ("HABER", "2m3k6xyjyek7djr", ["https://tele1-live.ercdn.net/tele1/tele1_1080p.m3u8"]),
"ULUSAL TV": ("HABER", "rjxdtygyec6mqjz", ["https://ulusal-live.ercdn.net/ulusaltv/ulusaltv.m3u8"]),
"BLOOMBERG HT": ("HABER", "4nu4fjjhm0y6wqm", ["https://ciner-live.daioncdn.net/bloomberght/bloomberght_720p.m3u8"]),
"A PARA": ("HABER", "8yfvm8ak2t1qoe6", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/apara/apara_1080p.m3u8"]),
"TVNET": ("HABER", "njoweqtgl6xngkj", ["https://tvnet-live.lg.mncdn.com/tvnet/tvnet/playlist.m3u8"]),
"ÜLKE TV": ("HABER", "kanaalkyymvqcjf", ["https://livetv.radyotvonline.net/kanal7live/ulketv/playlist.m3u8"]),
"FLASH HABER": ("HABER", "10bd6fhoe76yplp", ["https://flashhaber-live.ercdn.net/flashhaber/flashhaber.m3u8"]),
"BENGÜTÜRK": ("HABER", "", ["https://tv.ensonhaber.com/benguturk/benguturk_720p.m3u8"]),
"TRT SPOR": ("SPOR", "v0kvdikxec8nngd", ["https://tv-trtspor1.medya.trt.com.tr/master_1080.m3u8", "https://tv-trtspor1.medya.trt.com.tr/master_720.m3u8"]),
"TRT SPOR YILDIZ": ("SPOR", "1yyvuttcurbkcnr", ["https://trt.daioncdn.net/trtspor-yildiz/master_1080p.m3u8?app=web&platform=trtspor"]),
"A SPOR": ("SPOR", "v25znppc6itjprw", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/aspor/aspor_1080p.m3u8"]),
"HT SPOR": ("SPOR", "spgsorunhgejuu2", ["https://ciner.daioncdn.net/ht-spor/ht-spor.m3u8?app=web"]),
"TJK TV": ("SPOR", "jgxiih7f6yhagpj", ["https://tjktv-live.tjk.org/tjktv_1080p.m3u8"]),
"FB TV": ("SPOR", "jemrsooej8d8jku", ["https://1hskrdto.rocketcdn.com/fenerbahcetv.smil/playlist.m3u8"]),
"EKOL SPORTS": ("SPOR", "", ["https://ekoltv-live.ercdn.net/ekolsport/ekolsport_1080p.m3u8"]),
"TRT ÇOCUK": ("ÇOCUK", "ybv52n8pldp0lfq", ["https://tv-trtcocuk.medya.trt.com.tr/master_1080.m3u8", "https://tv-trtcocuk.medya.trt.com.tr/master_720.m3u8"]),
"TRT DİYANET ÇOCUK": ("ÇOCUK", "TRTDiyanetCocuk.tr@SD", ["https://tv-trtdiyanetcocuk.medya.trt.com.tr/master_720.m3u8"]),
"MİNİKA GO": ("ÇOCUK", "phekqx3pyw2wiiq", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/minikago/minikago.m3u8"]),
"MİNİKA ÇOCUK": ("ÇOCUK", "52hjq0o16nwpdnq", ["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/minikago_cocuk/minikago_cocuk.m3u8"]),
"TRT BELGESEL": ("BELGESEL", "80spas00o3iq47a", ["https://tv-trtbelgesel.medya.trt.com.tr/master_720.m3u8"]),
"DİYANET TV": ("DİNİ", "DiyanetTV.tr@SD", ["https://eustr73.mediatriple.net/videoonlylive/mtikoimxnztxlive/broadcast_5e3bf95a47e07.smil/playlist.m3u8"]),
"SEMERKAND TV": ("DİNİ", "SemerkandTV.tr", ["https://b01c02nl.mediatriple.net/videoonlylive/mtisvwurbfcyslive/broadcast_58d915bd40efc.smil/playlist.m3u8"]),
"LALEGÜL TV": ("DİNİ", "LalegulTV.tr@SD", ["https://lbl.netmedya.net/hls/lalegultv.m3u8"]),
"DOST TV": ("DİNİ", "DostTV.tr@SD", ["https://dost.stream.emsal.im/tv/live.m3u8"]),
"TRT MÜZİK": ("MÜZİK", "18ws4yk42js588h", ["https://tv-trtmuzik.medya.trt.com.tr/master_720.m3u8"]),
"DREAM TÜRK": ("MÜZİK", "ttlji9eholru11x", ["https://live.duhnet.tv/S2/HLS_LIVE/dreamturknp/playlist.m3u8"]),
"KRAL POP TV": ("MÜZİK", "KralPopTV.tr@SD", ["https://dogus-live.daioncdn.net/kralpoptv/playlist.m3u8"]),
"POWER TÜRK": ("MÜZİK", "82e4q3ribmz2mt1", ["https://livetv.powerapp.com.tr/powerturkTV/powerturkhd.smil/playlist.m3u8"]),
"NUMBER1 TV": ("MÜZİK", "Number1TV.tr@SD", ["https://b01c02nl.mediatriple.net/videoonlylive/mtkgeuihrlfwlive/broadcast_5c9e17cd59e8b.smil/playlist.m3u8"]),
"TRT EBA": ("EĞİTİM-KÜLTÜR", "TRTEBA.tr@SD", []),
"TBMM TV": ("KAMU-TEMATİK", "TBMMTV.tr@SD", ["https://meclistv-live.ercdn.net/meclistv/meclistv.m3u8"]),
"TRT AVAZ": ("KAMU-TEMATİK", "p6sz5lndgfas2r9", ["https://tv-trtavaz.medya.trt.com.tr/master_720.m3u8"]),
"TRT TÜRK": ("KAMU-TEMATİK", "xe24vekaidpsql3", ["https://tv-trtturk.medya.trt.com.tr/master_720.m3u8"]),
}

ALIASES = {
"TRT1":"TRT 1", "TRT 1":"TRT 1", "TRT2":"TRT 2", "TRT 2":"TRT 2",
"SHOW":"SHOW TV", "SHOW TV":"SHOW TV", "STAR":"STAR TV", "STAR TV":"STAR TV",
"KANALD":"KANAL D", "KANAL D":"KANAL D", "KANAL7":"KANAL 7", "KANAL 7":"KANAL 7",
"FOX":"NOW", "FOX TV":"NOW", "NOW TV":"NOW", "NOW":"NOW", "TV 100":"TV100", "TV100":"TV100",
"SZC TV":"SÖZCÜ TV", "SOZCU TV":"SÖZCÜ TV", "SOZCU":"SÖZCÜ TV", "SÖZCÜ":"SÖZCÜ TV",
"HABER TURK":"HABERTÜRK", "HABERTURK":"HABERTÜRK", "CNN TURK":"CNN TÜRK",
"TV8 5":"TV8.5", "TV8.5":"TV8.5", "TEVE 2":"TEVE2", "A 2":"A2",
"TRT COCUK":"TRT ÇOCUK", "MINIKA GO":"MİNİKA GO", "MINIKA COCUK":"MİNİKA ÇOCUK",
"TRT MUZIK":"TRT MÜZİK", "DREAM TURK":"DREAM TÜRK", "POWER TURK":"POWER TÜRK",
"ULKE TV":"ÜLKE TV", "DIYANET TV":"DİYANET TV", "LALEGUL TV":"LALEGÜL TV",
"BENGUTURK":"BENGÜTÜRK", "TRT DIYANET COCUK":"TRT DİYANET ÇOCUK",
}

def ascii_key(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.upper().replace("&", " ")
    s = re.sub(r"\b(?:2160P|1440P|1080P|720P|576P|480P|360P|4K|UHD|QHD|FHD|HD|SD)\b", " ", s)
    s = re.sub(r"\bALTERNATIF(?:\s+\d+)?\b", " ", s)
    s = re.sub(r"\[[^]]*\]", " ", s)
    s = re.sub(r"[^A-Z0-9.]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

ALIAS_ASCII = {ascii_key(k): v for k, v in ALIASES.items()}
for c in CHANNELS: ALIAS_ASCII[ascii_key(c)] = c

def canonical(name):
    return ALIAS_ASCII.get(ascii_key(name))

def attrs(line):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', line))

def parse_m3u(text):
    out=[]; info=None
    for raw in text.splitlines():
        line=raw.strip()
        if line.startswith("#EXTINF:"): info=line
        elif info and line.startswith(("http://","https://")):
            meta=attrs(info); visible=info.split(",",1)[-1].strip()
            name=meta.get("tvg-name") or visible
            out.append({"name":name,"visible":visible,"url":line,"logo":meta.get("tvg-logo", ""),"tvg_id":meta.get("tvg-id", "")})
            info=None
    return out

def fetch(url, limit=2_000_000, timeout=HTTP_TIMEOUT, headers=None):
    h={"User-Agent":USER_AGENT,"Accept":"*/*"}; h.update(headers or {})
    req=urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r: return r.read(limit), r.geturl()

def download_text(url): return fetch(url)[0].decode("utf-8-sig", "ignore")

def hls_check(url):
    try:
        data, final=fetch(url, 1_000_000)
        text=data.decode("utf-8", "ignore")
        if "#EXTM3U" not in text: return False, url, "not-hls"
        base=final
        if "#EXT-X-STREAM-INF" in text:
            lines=text.splitlines(); variants=[]
            for i,line in enumerate(lines):
                if line.startswith("#EXT-X-STREAM-INF"):
                    m=re.search(r"RESOLUTION=(\d+)x(\d+)",line); score=int(m.group(1))*int(m.group(2)) if m else 0
                    for nxt in lines[i+1:]:
                        nxt=nxt.strip()
                        if nxt and not nxt.startswith("#"):
                            variants.append((score, urllib.parse.urljoin(base,nxt))); break
            if not variants: return False,url,"master-no-variant"
            _, media=max(variants); data, final=fetch(media,1_000_000); text=data.decode("utf-8","ignore"); base=final
        seg=None
        for line in text.splitlines():
            line=line.strip()
            if line and not line.startswith("#"):
                seg=urllib.parse.urljoin(base,line); break
        if not seg: return False,url,"no-segment"
        chunk,_=fetch(seg,65536,headers={"Range":"bytes=0-65535"})
        return (len(chunk)>512), (media if 'media' in locals() else url), f"segment={len(chunk)}"
    except Exception as e: return False,url,str(e)[:180]

def ffprobe(url):
    try:
        p=subprocess.run(["ffprobe","-v","error","-rw_timeout","12000000","-user_agent",USER_AGENT,"-select_streams","v:0","-show_entries","stream=width,height,codec_name","-of","json",url],capture_output=True,text=True,timeout=PROBE_TIMEOUT)
        if p.returncode: return 0,0,"",(p.stderr or "")[:180]
        j=json.loads(p.stdout or "{}"); streams=j.get("streams") or []
        if not streams: return 0,0,"","no-video"
        s=streams[0]; return int(s.get("width") or 0),int(s.get("height") or 0),s.get("codec_name") or "","ok"
    except Exception as e: return 0,0,"",str(e)[:180]

def test_url(url):
    if any(x in url.lower() for x in BLOCKED_URL_PARTS): return {"ok":False,"url":url,"detail":"blocked"}
    hls_ok, probe_url, detail=hls_check(url)
    if not hls_ok: return {"ok":False,"url":url,"detail":detail}
    w,h,codec,pdetail=ffprobe(probe_url)
    return {"ok":bool(w and h),"url":url,"probe_url":probe_url,"width":w,"height":h,"codec":codec,"detail":detail+";"+pdetail}

def quality(w,h):
    if w>=3840 or h>=2160:return "2160P 4K UHD"
    if h>=1440:return "1440P QHD"
    if h>=1080:return "1080P FHD"
    if h>=720:return "720P HD"
    if h>=576:return "576P SD"
    return f"{h}P SD" if h else "SD"

def host(url): return (urllib.parse.urlparse(url).hostname or "").lower()

def score(r, sources):
    source_bonus=max(({"CURATED":40,"PREVIOUS":35,"SOURCE":25,"IPTV_ORG":15}.get(x,5) for x in sources), default=0)
    return r.get("width",0)*r.get("height",0)*100 + source_bonus

def epg_ids():
    try:
        data,_=fetch(EPG_URL,8_000_000,10); root=ET.fromstring(data)
        return {x.attrib.get("id","") for x in root.findall("channel")}
    except Exception as e:
        print("EPG okunamadi:",e); return set()

def main():
    src=Path(sys.argv[1] if len(sys.argv)>1 else "MADSC_TV_47_LISTE_ADAY.m3u")
    if not src.exists(): raise SystemExit(f"Dosya bulunamadi: {src}")
    pools=defaultdict(dict); logos={}
    def add(ch,url,source,logo=""):
        if ch not in CHANNELS or not url or any(x in url.lower() for x in BLOCKED_URL_PARTS): return
        rec=pools[ch].setdefault(url,set()); rec.add(source)
        if logo and not logos.get(ch): logos[ch]=logo
    for e in parse_m3u(src.read_text(encoding="utf-8-sig",errors="ignore")):
        ch=canonical(e["name"]); add(ch,e["url"],"SOURCE",e["logo"])
    prev=Path("CALISANLAR.m3u")
    if prev.exists():
        for e in parse_m3u(prev.read_text(encoding="utf-8-sig",errors="ignore")):
            ch=canonical(e["name"]); add(ch,e["url"],"PREVIOUS",e["logo"])
    for ch,(_,_,urls) in CHANNELS.items():
        for u in urls:add(ch,u,"CURATED")
    for source,url in DISCOVERY_SOURCES:
        try:
            for e in parse_m3u(download_text(url)):
                ch=canonical(e["name"]); add(ch,e["url"],source,e["logo"])
        except Exception as e: print("Kesif kaynagi okunamadi",source,e)
    # Her kanal için aday sayısını sınırla; bilinen adaylar önce gelir.
    selected={}
    for ch,items in pools.items():
        ordered=sorted(items.items(), key=lambda kv: max(({"CURATED":4,"PREVIOUS":3,"SOURCE":2,"IPTV_ORG":1}.get(s,0) for s in kv[1]),default=0), reverse=True)
        selected[ch]=ordered[:MAX_CANDIDATES]
    unique={u for items in selected.values() for u,_ in items}
    print(f"Kanal: {len(CHANNELS)} | Benzersiz aday URL: {len(unique)}")
    results={}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        fut={ex.submit(test_url,u):u for u in unique}
        for i,f in enumerate(as_completed(fut),1):
            u=fut[f]
            try: results[u]=f.result()
            except Exception as e: results[u]={"ok":False,"url":u,"detail":str(e)}
            print(f"[{i}/{len(unique)}] {'OK' if results[u].get('ok') else 'X'} {u[:90]}",flush=True)
    valid_epg=epg_ids(); favorites={canonical(x) for x in DEFAULT_FAVORITES}
    rows=[]; main_entries=[]; alt_entries=[]; failures=[]
    for ch,(group,epg,_) in CHANNELS.items():
        tested=[]
        for u,sources in selected.get(ch,[]):
            r=results.get(u,{"ok":False,"url":u,"detail":"not-tested"}); rr=dict(r); rr["sources"]=sources
            rows.append([ch,"CALISIYOR" if r.get("ok") else "CALISMIYOR",quality(r.get("width",0),r.get("height",0)) if r.get("ok") else "",r.get("width",0),r.get("height",0),"+".join(sorted(sources)),host(u),r.get("codec",""),r.get("detail",""),u,epg,"VAR" if epg and (not valid_epg or epg in valid_epg) else "YOK"])
            if r.get("ok"): tested.append(rr)
        if not tested:
            failures.append(f"{ch}\nCALISAN KAYNAK BULUNAMADI\n"); continue
        tested.sort(key=lambda r:score(r,r["sources"]),reverse=True); best=tested[0]
        main_entries.append((group,ch,best,epg,logos.get(ch,"")))
        # Yalnızca farklı hosttaki, makul kalitedeki en iyi bir yedeği ALTERNATİF'e al.
        for alt in tested[1:]:
            if host(alt["url"])!=host(best["url"]) and alt["height"]>=min(720,best["height"]):
                alt_entries.append(("ALTERNATİF",ch,alt,epg,logos.get(ch,""))); break
    priority={canonical(n):i for i,n in enumerate(DEFAULT_FAVORITES)}
    def sortkey(x): return (GROUP_ORDER.index(x[0]),priority.get(x[1],999),x[1])
    main_entries.sort(key=sortkey); alt_entries.sort(key=sortkey)
    fav=[("⭐ FAVORİLER",ch,r,e,l) for g,ch,r,e,l in main_entries if ch in favorites]
    all_entries=fav+main_entries+alt_entries; all_entries.sort(key=sortkey)
    lines=[f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"']
    for group,ch,r,epg,logo in all_entries:
        # Görünen adda ALTERNATİF kelimesi yoktur; kalite ölçülen çözünürlüktür.
        a=[f'tvg-name="{ch}"',f'group-title="{group}"']
        if epg:a.insert(0,f'tvg-id="{epg}"')
        if logo:a.append(f'tvg-logo="{logo}"')
        lines.append(f'#EXTINF:-1 {" ".join(a)},{ch} {quality(r["width"],r["height"])}')
        lines.append(r["url"])
    Path("CALISANLAR.m3u").write_text("\n".join(lines)+"\n",encoding="utf-8")
    Path("CALISMAYANLAR.txt").write_text("\n".join(failures),encoding="utf-8")
    with open("TEST_RAPORU.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["Kanal","Durum","Kalite","Genislik","Yukseklik","Kaynak","Host","Codec","Uyumluluk","URL","EPG_ID","EPG_Durumu"]); w.writerows(rows)
    print("="*50); print("MADSC TV TESTI TAMAMLANDI"); print("Ana calisan:",len(main_entries)); print("Alternatif:",len(alt_entries)); print("Calismayan:",len(failures)); print("="*50)

if __name__=="__main__": main()
