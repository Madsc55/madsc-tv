#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MADSC TV v3
- Onur Eroz YOK.
- Mevcut aday liste + onceki CALISANLAR + IPTV-org + Dearbulut + bilinen acik yayin adaylari.
- URL'ler paralel test edilir.
- HLS playlist + ffprobe video/gercek cozunurluk kontrolu.
- Helga ve premium/yerel/radyo filtreleri.
- En iyi yayin ana kategoride; faydali ikinci yayin ALTERNATIF kategorisinde.
- Kalite gorunen kanal adina eklenir, tvg-id sabit kalir.
- FAVORILER ilk yazilir.
"""

import csv
import json
import re
import subprocess
import sys
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

EPG_URL = "https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml"

DISCOVERY_SOURCES = [
    ("IPTV_ORG", "https://iptv-org.github.io/iptv/countries/tr.m3u"),
    ("DEARBULUT_TR", "https://dearbulut.github.io/iptv/playlists/country/tr.m3u"),
]

CATEGORY_ORDER = [
    "⭐ FAVORİLER", "ULUSAL", "HABER", "SPOR", "ALTERNATİF",
    "ÇOCUK", "BELGESEL", "DİNİ", "MÜZİK", "SİNEMA-DİZİ",
    "EĞİTİM-KÜLTÜR", "KAMU-TEMATİK", "İNTERNET",
]

FAVORITES = [
    "TRT 1", "ATV", "KANAL D", "SHOW TV", "STAR TV", "NOW", "TV8",
    "KANAL 7", "SÖZCÜ TV", "TV100", "NTV", "CNN TÜRK", "TRT HABER",
    "HABERTÜRK", "HABER GLOBAL", "TRT SPOR", "A SPOR",
]

POPULARITY = FAVORITES + [
    "HALK TV", "A HABER", "TGRT HABER", "24 TV", "EKOL TV", "TELE1",
    "TRT SPOR YILDIZ", "HT SPOR", "TJK TV", "FB TV", "TRT ÇOCUK",
    "TRT BELGESEL", "TRT 2", "TRT MÜZİK",
]

MAX_WORKERS = 10
HTTP_TIMEOUT = 7
FFPROBE_TIMEOUT = 11
MAX_CANDIDATES_PER_CHANNEL = 8
USER_AGENT = "Mozilla/5.0 (MADSC-TV/3.0)"
BLOCKED_HOSTS = {"helga.iptv2022.com"}

EPG_IDS = {
    "TRT 1":"af0zo9et4xguwsk","KANAL D":"bbwgmhsmhhoatzg","SHOW TV":"pvr08e5grfsebfw",
    "STAR TV":"75tz02ooforewap","ATV":"2zkzbuscxwyjc4k","KANAL 7":"a8t877hb0oandbv",
    "TV8":"w7x32brlcz26ibb","NOW":"m0abaihy7vla6ma","CNN TÜRK":"ah7mr9ol040kp3b",
    "NTV":"nyz5s8p798n9cqg","TRT HABER":"in3p7jng04mr97m","HABERTÜRK":"gil1w2erz9l7imc",
    "24 TV":"9b7ltozvb9c333g","A HABER":"ql8qf4vb46o1h7t","TLC":"9z32hgan37zhgr6",
    "TV100":"5i5mds6ap6h7m7w","EKOL TV":"3kluptlla8k8re0","BEYAZ TV":"edf3lp61qexxxhl",
    "TVNET":"njoweqtgl6xngkj","HABER GLOBAL":"bwmpobxuqn2pz87","360":"cphtdpl9j70cn3a",
    "BLOOMBERG HT":"4nu4fjjhm0y6wqm","TGRT HABER":"qz2fp61itc8xm4g","DMAX":"6sokobdd9dwe0gl",
    "TV8.5":"pd29xh24glvq4qz","ÜLKE TV":"kanaalkyymvqcjf","A PARA":"8yfvm8ak2t1qoe6",
    "TRT BELGESEL":"80spas00o3iq47a","TJK TV":"jgxiih7f6yhagpj","HT SPOR":"spgsorunhgejuu2",
    "A SPOR":"v25znppc6itjprw","FB TV":"jemrsooej8d8jku","TRT SPOR":"v0kvdikxec8nngd",
    "TRT SPOR YILDIZ":"1yyvuttcurbkcnr","ULUSAL KANAL":"rjxdtygyec6mqjz",
    "SÖZCÜ TV":"5zoe73avn97ggnt","TRT 2":"nzdc0yd5xxv43yl","TRT TÜRK":"xe24vekaidpsql3",
    "TRT MÜZİK":"18ws4yk42js588h","DREAM TÜRK":"ttlji9eholru11x","POWER TÜRK":"82e4q3ribmz2mt1",
    "TRT ÇOCUK":"ybv52n8pldp0lfq","MİNİKA GO":"phekqx3pyw2wiiq",
    "MİNİKA ÇOCUK":"52hjq0o16nwpdnq","HALK TV":"d1exl1gxity48nl",
    "TELE1":"2m3k6xyjyek7djr","FLASH HABER":"10bd6fhoe76yplp","A2":"fc29p3wbp8wkgo4",
    "TRT WORLD":"j1x67766q1lr7r6","TRT KURDİ":"u552n6w4dkv49wz","TRT AVAZ":"p6sz5lndgfas2r9",
    "TEVE 2":"6vs4sg9183gdxth",
}

ALIASES = {
    "SZC TV":"SÖZCÜ TV","SOZCU TV":"SÖZCÜ TV","SOZCU":"SÖZCÜ TV",
    "CNN TURK":"CNN TÜRK","HABERTURK":"HABERTÜRK","TV 100":"TV100",
    "TV 8 5":"TV8.5","TV8 5":"TV8.5","TV 8,5":"TV8.5","TEVE2":"TEVE 2",
    "ULUSAL TV":"ULUSAL KANAL","TRT COCUK":"TRT ÇOCUK","TRT MUZIK":"TRT MÜZİK",
    "TRT TURK":"TRT TÜRK","MINIKA GO":"MİNİKA GO","MINIKA COCUK":"MİNİKA ÇOCUK",
    "ULKE TV":"ÜLKE TV","DREAM TURK":"DREAM TÜRK","POWER TURK":"POWER TÜRK",
}

CURATED = {
"TRT 1":["https://tv-trt1.medya.trt.com.tr/master_1080.m3u8","https://tv-trt1.medya.trt.com.tr/master_720.m3u8"],
"ATV":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8"],
"KANAL D":["https://demiroren.daioncdn.net/kanald/kanald.m3u8?app=kanald_web&ce=3"],
"SHOW TV":["https://ciner-live.daioncdn.net/showtv/showtv_1080p.m3u8","https://ciner-live.daioncdn.net/showtv/showtv_720p.m3u8"],
"STAR TV":["https://dogus.daioncdn.net/startv/startv_720p.m3u8?app=a20ac41e-bdc3-4aa1-934d-26b484480ac9&ce=3"],
"TV8":["https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/tv8/tv8_1080p.m3u8"],
"NOW":["https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8"],
"KANAL 7":["https://kanal7-live.daioncdn.net/kanal7/kanal7_1080p.m3u8"],
"360":["https://turkmedya-live.ercdn.net/tv360/tv360_1080p.m3u8"],
"A2":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/a2tv/a2tv_1080p.m3u8"],
"TEVE 2":["https://demiroren-live.daioncdn.net/teve2/teve2_1080p.m3u8"],
"BEYAZ TV":["https://beyaztv-live.daioncdn.net/beyaztv/beyaztv_1080p.m3u8"],
"TRT 2":["https://tv-trt2.medya.trt.com.tr/master.m3u8"],
"DMAX":["https://dogus-live.daioncdn.net/dmax/dmax_720p.m3u8"],
"TLC":["https://dogus-live.daioncdn.net/tlc/tlc_720p.m3u8"],
"TV8.5":["https://tv8.daioncdn.net/tv8bucuk/tv8bucuk_1080p.m3u8?app=tv8bucuk_web&ce=3"],
"TV100":["https://tv100-live.daioncdn.net/tv100/tv100_1080p.m3u8"],
"SÖZCÜ TV":["https://szctvdvr.blutv.com/blutv_szctv_dvr/live_720p4350000kbps/index.m3u8"],
"TRT HABER":["https://tv-trthaber.medya.trt.com.tr/master_720.m3u8"],
"NTV":["https://dogus.daioncdn.net/ntv/ntv_1080p.m3u8"],
"HABERTÜRK":["https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/haberturktv/haberturktv_1080p.m3u8"],
"CNN TÜRK":["https://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/playlist.m3u8"],
"HABER GLOBAL":["https://ensonhaber-live.ercdn.net/haberglobal/haberglobal_720p.m3u8"],
"HALK TV":["https://halktv-live.daioncdn.net/halktv/halktv_1080p.m3u8"],
"TGRT HABER":["https://canli.tgrthaber.com/tgrt.m3u8"],
"A HABER":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/ahaber/ahaber_1080p.m3u8"],
"24 TV":["https://turkmedya-live.ercdn.net/tv24/tv24_1080p.m3u8"],
"EKOL TV":["https://ekoltv-live.ercdn.net/ekoltv/ekoltv_1080p.m3u8"],
"TELE1":["https://tele1-live.ercdn.net/tele1/tele1_1080p.m3u8"],
"ULUSAL KANAL":["https://ulusal-live.ercdn.net/ulusaltv/ulusaltv.m3u8"],
"BLOOMBERG HT":["https://ciner-live.daioncdn.net/bloomberght/bloomberght_720p.m3u8"],
"A PARA":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/apara/apara_1080p.m3u8"],
"TVNET":["https://tvnet-live.lg.mncdn.com/tvnet/tvnet/playlist.m3u8"],
"ÜLKE TV":["https://livetv.radyotvonline.net/kanal7live/ulketv/playlist.m3u8"],
"FLASH HABER":["https://flashhaber-live.ercdn.net/flashhaber/flashhaber.m3u8"],
"TRT SPOR":["https://tv-trtspor1.medya.trt.com.tr/master_1080.m3u8","https://tv-trtspor1.medya.trt.com.tr/master_720.m3u8"],
"TRT SPOR YILDIZ":["https://trt.daioncdn.net/trtspor-yildiz/master_1080p.m3u8?app=web&platform=trtspor"],
"A SPOR":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/aspor/aspor_1080p.m3u8"],
"HT SPOR":["https://ciner.daioncdn.net/ht-spor/ht-spor.m3u8?app=web"],
"TJK TV":["https://tjktv-live.tjk.org/tjktv_1080p.m3u8"],
"FB TV":["https://1hskrdto.rocketcdn.com/fenerbahcetv.smil/playlist.m3u8"],
"TRT ÇOCUK":["https://tv-trtcocuk.medya.trt.com.tr/master_1080.m3u8","https://tv-trtcocuk.medya.trt.com.tr/master_720.m3u8"],
"MİNİKA GO":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/minikago/minikago.m3u8"],
"MİNİKA ÇOCUK":["https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/minikago_cocuk/minikago_cocuk.m3u8"],
"TRT BELGESEL":["https://tv-trtbelgesel.medya.trt.com.tr/master_720.m3u8"],
"DİYANET TV":["https://eustr73.mediatriple.net/videoonlylive/mtikoimxnztxlive/broadcast_5e3bf95a47e07.smil/playlist.m3u8"],
"SEMERKAND TV":["https://b01c02nl.mediatriple.net/videoonlylive/mtisvwurbfcyslive/broadcast_58d915bd40efc.smil/playlist.m3u8"],
"LALEGÜL TV":["https://lbl.netmedya.net/hls/lalegultv.m3u8"],
"DOST TV":["https://dost.stream.emsal.im/tv/live.m3u8"],
"TRT AVAZ":["https://tv-trtavaz.medya.trt.com.tr/master_720.m3u8"],
"TRT TÜRK":["https://tv-trtturk.medya.trt.com.tr/master_720.m3u8"],
"TRT MÜZİK":["https://tv-trtmuzik.medya.trt.com.tr/master_720.m3u8"],
"DREAM TÜRK":["https://live.duhnet.tv/S2/HLS_LIVE/dreamturknp/playlist.m3u8"],
"KRAL POP TV":["https://dogus-live.daioncdn.net/kralpoptv/playlist.m3u8"],
"POWER TÜRK":["https://livetv.powerapp.com.tr/powerturkTV/powerturkhd.smil/playlist.m3u8"],
"NUMBER 1 TV":["https://b01c02nl.mediatriple.net/videoonlylive/mtkgeuihrlfwlive/broadcast_5c9e17cd59e8b.smil/playlist.m3u8"],
"TBMM TV":["https://meclistv-live.ercdn.net/meclistv/meclistv.m3u8"],
}

# Otomatik kesifte bunlar kesinlikle alinmaz.
PREMIUM_PATTERNS = (
    "BEIN", "EXXEN", "DISNEY", "HBO", " S SPORT", "SSPORT",
    "TIVIBU", "D-SMART", "DIGITURK", "NETFLIX",
)
RADIO_PATTERNS = ("RADYO", "RADIO", "FM ")
LOCAL_TOKENS = {
    "ADANA","ADIYAMAN","AFYON","AKSARAY","AMASYA","ANTALYA","ARDAHAN","ARTVIN","AYDIN",
    "BALIKESIR","BARTIN","BATMAN","BAYBURT","BILECIK","BINGOL","BITLIS","BOLU","BURDUR",
    "BURSA","CANAKKALE","CANKIRI","CORUM","DENIZLI","DIYARBAKIR","DUZCE","EDIRNE","ELAZIG",
    "ERZINCAN","ERZURUM","ESKISEHIR","GAZIANTEP","GIRESUN","GUMUSHANE","HAKKARI","HATAY",
    "IGDIR","ISPARTA","KAHRAMANMARAS","KARABUK","KARAMAN","KARS","KASTAMONU","KAYSERI",
    "KILIS","KIRIKKALE","KIRKLARELI","KIRSEHIR","KOCAELI","KONYA","KUTAHYA","MALATYA",
    "MANISA","MARDIN","MERSIN","MUGLA","MUS","NEVSEHIR","NIGDE","ORDU","OSMANIYE","RIZE",
    "SAKARYA","SAMSUN","SIIRT","SINOP","SIVAS","SANLIURFA","SIRNAK","TEKIRDAG","TOKAT",
    "TRABZON","TUNCELI","USAK","VAN","YALOVA","YOZGAT","ZONGULDAK",
}

def ascii_text(text):
    tr = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iIsSgGuUoOcC")
    text = text.translate(tr)
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))

def clean_name(name):
    name = name.strip()
    name = re.sub(r"\s*[•|\-]?\s*ALTERNAT[İI]F(?:\s*\d+)?(?:.*)?$", "", name, flags=re.I)
    name = re.sub(r"\s*[\(\[]?(?:2160|1440|1080|720|576|480)P?[\)\]]?\s*(?:4K|UHD|FHD|FULL\s*HD|HD|SD)?\s*$", "", name, flags=re.I)
    name = re.sub(r"\s+(?:4K\s*UHD|4K|UHD|FHD|FULL\s*HD|HD|SD)\s*$", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" -|•")

def key_for(name):
    k = ascii_text(clean_name(name)).upper()
    k = re.sub(r"[^A-Z0-9]+", " ", k)
    k = re.sub(r"\s+", " ", k).strip()
    alias_map = {ascii_text(a).upper(): b for a,b in ALIASES.items()}
    return ascii_text(alias_map.get(k, k)).upper()

KNOWN_NAMES = set(EPG_IDS) | set(CURATED) | set(FAVORITES) | set(POPULARITY)
KNOWN_BY_KEY = {key_for(x): x for x in KNOWN_NAMES}

def canonical_name(name):
    return KNOWN_BY_KEY.get(key_for(name), clean_name(name))

def parse_attrs(info):
    return {m.group(1): m.group(2) for m in re.finditer(r'([\w-]+)="([^"]*)"', info)}

def parse_m3u(text, source):
    out, info = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#EXTINF:"):
            info = line
            continue
        if info and line.startswith(("http://","https://")):
            a = parse_attrs(info)
            raw_name = info.split(",",1)[-1].strip()
            out.append({
                "name": canonical_name(raw_name), "raw_name": raw_name, "url": line,
                "source": source, "logo": a.get("tvg-logo",""),
                "tvg_id": a.get("tvg-id",""), "group": a.get("group-title",""),
                "country": a.get("tvg-country",""), "language": a.get("tvg-language",""),
            })
            info = None
    return out

def fetch_text(url, timeout=HTTP_TIMEOUT, limit=4_000_000):
    req = urllib.request.Request(url, headers={"User-Agent":USER_AGENT,"Accept":"*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(limit).decode("utf-8-sig", errors="ignore")

def blocked_url(url):
    try:
        host = (urllib.parse.urlparse(url).hostname or "").lower()
    except Exception:
        return True
    return any(host == h or host.endswith("." + h) for h in BLOCKED_HOSTS)

def is_discovery_allowed(e):
    n = ascii_text(e["name"]).upper()
    g = ascii_text(e.get("group","")).upper()
    if any(x in n or x in g for x in PREMIUM_PATTERNS): return False
    if any(x in n or x in g for x in RADIO_PATTERNS): return False

    # Bilinen ulusal kanal ise sehir kelimesi filtresini atla.
    if key_for(e["name"]) in KNOWN_BY_KEY:
        return True

    words = set(re.findall(r"[A-Z0-9]+", n))
    if words & LOCAL_TOKENS:
        return False

    # IPTV-org/Dearbulut ulke listelerinde bulunan ama metadata'si acikca yabanciysa alma.
    country = ascii_text(e.get("country","")).upper()
    if country and not any(x in country for x in ("TR","TUR","TURKEY","TURKIYE")):
        return False

    return True

def classify(name, group=""):
    x = ascii_text(f"{name} {group}").upper()
    if any(w in x for w in ("HABER","NEWS","NTV","CNN","BLOOMBERG","SOZCU","HALK TV","TELE1","TV100","EKOL TV","A PARA","ULUSAL KANAL","TVNET","ULKE TV","FLASH")): return "HABER"
    if any(w in x for w in ("SPOR","SPORT","TJK","FB TV","FENERBAHCE")): return "SPOR"
    if any(w in x for w in ("COCUK","MINIKA","KIDS")): return "ÇOCUK"
    if any(w in x for w in ("BELGESEL","DOCUMENTARY")): return "BELGESEL"
    if any(w in x for w in ("DIYANET","SEMERKAND","LALEGUL","DOST TV")): return "DİNİ"
    if any(w in x for w in ("MUZIK","MUSIC","DREAM","POWER","KRAL POP","NUMBER 1")): return "MÜZİK"
    if any(w in x for w in ("SINEMA","DIZI","MOVIE","FILM","SERIES")): return "SİNEMA-DİZİ"
    if any(w in x for w in ("EGITIM","KULTUR","TRT 2")): return "EĞİTİM-KÜLTÜR"
    if any(w in x for w in ("TBMM","TRT AVAZ","TRT TURK","TRT KURDI")): return "KAMU-TEMATİK"
    if any(w in x for w in ("INTERNET","WEB TV","YOUTUBE")): return "İNTERNET"
    return "ULUSAL"

def quality_label(w,h):
    if w >= 3840 or h >= 2160: return "2160P 4K UHD"
    if h >= 1440: return "1440P QHD"
    if h >= 1080: return "1080P FHD"
    if h >= 720: return "720P HD"
    if h >= 576: return "576P SD"
    return f"{h}P SD" if h else "KALİTE BİLİNMİYOR"

def hls_precheck(url):
    if ".m3u8" not in url.lower():
        return True, "NON_HLS"
    try:
        text = fetch_text(url, limit=700_000)
        if "#EXTM3U" not in text:
            return False, "HLS_HEADER_YOK"
        refs = [x.strip() for x in text.splitlines() if x.strip() and not x.startswith("#")]
        if not refs:
            return False, "HLS_REFERANS_YOK"
        if "#EXT-X-STREAM-INF" in text:
            child = urllib.parse.urljoin(url, refs[0])
            ct = fetch_text(child, limit=700_000)
            if "#EXTM3U" not in ct:
                return False, "CHILD_HLS_BOZUK"
            media_refs = [x.strip() for x in ct.splitlines() if x.strip() and not x.startswith("#")]
            if not media_refs:
                return False, "CHILD_SEGMENT_YOK"
        return True, "HLS_OK"
    except Exception as exc:
        return False, "HLS_FAIL:" + str(exc)[:120]

def ffprobe(url):
    try:
        p = subprocess.run([
            "ffprobe","-v","error","-rw_timeout","7000000",
            "-select_streams","v:0",
            "-show_entries","stream=codec_name,width,height",
            "-of","json",url
        ], capture_output=True, text=True, timeout=FFPROBE_TIMEOUT)
        if p.returncode != 0:
            return False,0,0,"",(p.stderr or "")[:220]
        data = json.loads(p.stdout or "{}")
        streams = data.get("streams") or []
        if not streams:
            return False,0,0,"","VIDEO_YOK"
        s = streams[0]
        w,h = int(s.get("width") or 0), int(s.get("height") or 0)
        if not w or not h:
            return False,w,h,s.get("codec_name",""),"COZUNURLUK_YOK"
        return True,w,h,s.get("codec_name",""),"OK"
    except Exception as exc:
        return False,0,0,"","FFPROBE:" + str(exc)[:150]

def source_bonus(source,url):
    b = {
        "ONCEKI_CALISAN":700, "ORIJINAL":650, "CURATED":625,
        "DEARBULUT_TR":525, "IPTV_ORG":475
    }.get(source,300)
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    if any(x in host for x in ("trt.com.tr","daioncdn.net","ercdn.net","mncdn.com","tjk.org","powerapp.com.tr","tgrthaber.com","duhnet.tv")):
        b += 250
    return b

def test_candidate(c):
    if blocked_url(c["url"]):
        return {**c,"ok":False,"reason":"BLOCKLIST","width":0,"height":0,"codec":"","score":0}
    h_ok,h_reason = hls_precheck(c["url"])
    if not h_ok:
        return {**c,"ok":False,"reason":h_reason,"width":0,"height":0,"codec":"","score":0}
    ok,w,h,codec,why = ffprobe(c["url"])
    if not ok:
        return {**c,"ok":False,"reason":why,"width":w,"height":h,"codec":codec,"score":0}
    # Cozunurluk ana kriter; ayni/similar kalitede stabil kaynak one cikar.
    score = w*h + source_bonus(c["source"],c["url"])*1000
    return {**c,"ok":True,"reason":h_reason,"width":w,"height":h,"codec":codec,"score":score}

def add_candidate(pool,name,url,source,logo="",tvg_id="",group=""):
    if not url or blocked_url(url): return
    k = key_for(name)
    if not k: return
    pool.setdefault(k,{
        "name":canonical_name(name),"logo":logo,"tvg_id":tvg_id,
        "group":group,"candidates":[]
    })
    r = pool[k]
    if logo and not r["logo"]: r["logo"] = logo
    if tvg_id and not r["tvg_id"]: r["tvg_id"] = tvg_id
    if group and not r["group"]: r["group"] = group
    if not any(x["url"] == url for x in r["candidates"]):
        r["candidates"].append({"url":url,"source":source})

def extinf(ch,group):
    display = f'{ch["name"]} {quality_label(ch["width"],ch["height"])}'
    tid = EPG_IDS.get(ch["name"], ch.get("tvg_id",""))
    logo = ch.get("logo","")
    bits = ["#EXTINF:-1"]
    if tid: bits.append(f'tvg-id="{tid}"')
    if logo: bits.append(f'tvg-logo="{logo}"')
    bits.append(f'group-title="{group}",{display}')
    return " ".join(bits)

def main():
    if len(sys.argv) < 2:
        raise SystemExit("Kullanim: python3 iptv_test.py MADSC_TV_47_LISTE_ADAY.m3u")
    src = Path(sys.argv[1])
    if not src.exists():
        raise SystemExit(f"Dosya bulunamadi: {src}")

    pool = {}

    # 1. Mevcut aday liste
    for e in parse_m3u(src.read_text(encoding="utf-8-sig",errors="ignore"),"ORIJINAL"):
        add_candidate(pool,e["name"],e["url"],"ORIJINAL",e["logo"],e["tvg_id"],e["group"])

    # 2. Onceki iyi CALISANLAR - iyi URL ertesi gun unutulmaz
    previous = Path("CALISANLAR.m3u")
    if previous.exists():
        for e in parse_m3u(previous.read_text(encoding="utf-8-sig",errors="ignore"),"ONCEKI_CALISAN"):
            add_candidate(pool,e["name"],e["url"],"ONCEKI_CALISAN",e["logo"],e["tvg_id"],e["group"])

    # 3. Bilinen acik adaylar
    for name,urls in CURATED.items():
        for url in urls:
            add_candidate(pool,name,url,"CURATED")

    # 4. Kesif kaynaklari
    for source,url in DISCOVERY_SOURCES:
        try:
            print(f"Kesif kaynagi: {source}",flush=True)
            entries = parse_m3u(fetch_text(url,timeout=15),source)
            accepted = 0
            for e in entries:
                if is_discovery_allowed(e):
                    add_candidate(pool,e["name"],e["url"],source,e["logo"],e["tvg_id"],e["group"])
                    accepted += 1
            print(f"  -> {accepted} uygun aday",flush=True)
        except Exception as exc:
            print(f"  -> Kaynak okunamadi: {exc}",flush=True)

    priority = {"ONCEKI_CALISAN":0,"ORIJINAL":1,"CURATED":2,"DEARBULUT_TR":3,"IPTV_ORG":4}
    jobs = []
    for k,r in pool.items():
        r["candidates"].sort(key=lambda x:priority.get(x["source"],99))
        # Kaynak cesitliligini koru, ama sonsuz URL test etme
        chosen, seen_sources = [], set()
        for c in r["candidates"]:
            if c["source"] not in seen_sources:
                chosen.append(c); seen_sources.add(c["source"])
        for c in r["candidates"]:
            if c not in chosen and len(chosen) < MAX_CANDIDATES_PER_CHANNEL:
                chosen.append(c)
        r["candidates"] = chosen[:MAX_CANDIDATES_PER_CHANNEL]
        jobs.extend((k,c) for c in r["candidates"])

    print(f"\nKanal kimligi: {len(pool)} | URL testi: {len(jobs)}",flush=True)

    results = defaultdict(list)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        fmap = {ex.submit(test_candidate,c):(k,c) for k,c in jobs}
        done = 0
        for f in as_completed(fmap):
            k,c = fmap[f]
            done += 1
            try: r = f.result()
            except Exception as exc:
                r = {**c,"ok":False,"reason":str(exc),"width":0,"height":0,"codec":"","score":0}
            results[k].append(r)
            if done % 20 == 0 or done == len(jobs):
                print(f"Test ilerleme: {done}/{len(jobs)}",flush=True)

    selected, alternatives, report = {}, {}, []
    for k,meta in pool.items():
        tested = results.get(k,[])
        good = sorted((x for x in tested if x["ok"]),key=lambda x:x["score"],reverse=True)
        for x in tested:
            report.append([
                meta["name"],"CALISIYOR" if x["ok"] else "CALISMIYOR",
                quality_label(x["width"],x["height"]) if x["ok"] else "",
                x["width"],x["height"],x["codec"],x["source"],x["reason"],x["url"],
                "EVET" if good and x["url"] == good[0]["url"] else "HAYIR",
                len(meta["candidates"]), EPG_IDS.get(meta["name"],meta.get("tvg_id",""))
            ])
        if not good: continue
        selected[k] = {**meta,**good[0]}
        alternatives[k] = []
        # Sadece farkli kaynak/URL ve makul kalite olan TEK yedek
        for x in good[1:]:
            if x["url"] == good[0]["url"]: continue
            if x["height"] >= max(576, int(good[0]["height"]*0.65)):
                alternatives[k] = [{**meta,**x}]
                break

    pop = {key_for(n):i for i,n in enumerate(POPULARITY)}
    grouped = defaultdict(list)
    for k,ch in selected.items():
        grouped[classify(ch["name"],ch.get("group",""))].append((k,ch))
    for g in grouped:
        grouped[g].sort(key=lambda z:(pop.get(z[0],9999),z[1]["name"]))

    lines = [f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"']

    # FAVORILER her zaman ilk
    for n in FAVORITES:
        k = key_for(n)
        if k in selected:
            ch = selected[k]
            lines += [extinf(ch,"⭐ FAVORİLER"),ch["url"]]

    for group in CATEGORY_ORDER:
        if group == "⭐ FAVORİLER":
            continue
        if group == "ALTERNATİF":
            ai = [(k,ch) for k,arr in alternatives.items() for ch in arr]
            ai.sort(key=lambda z:(pop.get(z[0],9999),z[1]["name"]))
            for _,ch in ai:
                lines += [extinf(ch,"ALTERNATİF"),ch["url"]]
            continue
        for _,ch in grouped.get(group,[]):
            lines += [extinf(ch,group),ch["url"]]

    Path("CALISANLAR.m3u").write_text("\n".join(lines)+"\n",encoding="utf-8")

    failed = [r["name"] for k,r in sorted(pool.items(),key=lambda z:z[1]["name"]) if k not in selected]
    Path("CALISMAYANLAR.txt").write_text("\n".join(failed)+"\n",encoding="utf-8")

    with open("TEST_RAPORU.csv","w",newline="",encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Kanal","Durum","Kalite","Genislik","Yukseklik","Codec","Kaynak","Kontrol","URL","Secildi","Aday_Sayisi","EPG_ID"])
        w.writerows(report)

    print("\n===================================")
    print("MADSC TV TESTI TAMAMLANDI")
    print(f"Kesfedilen kanal : {len(pool)}")
    print(f"Final calisan    : {len(selected)}")
    print(f"Calismayan       : {len(failed)}")
    print(f"Alternatif       : {sum(len(x) for x in alternatives.values())}")
    print("===================================")

if __name__ == "__main__":
    main()
