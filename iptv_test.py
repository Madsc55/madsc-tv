#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MADSC TV v6
- v4'teki fazla sert HLS segment kontrolu yumusatildi.
- HLS playlist + ffprobe asil karar mekanizmasidir; segment Range hatasi tek basina kanali elemez.
- Bir kanal icin ayni kaynaktaki birden fazla URL test edilebilir.
- Favoriler varsayilan liste + FAVORILER.txt ile kalici tutulur.
- Yerel/yabanci/radyo/premium ve supheli relay filtreleri korunur.
- ALTERNATIF ve ALTERNATIF DIJITAL kanal adina eklenmez; sadece grup adidir.\n- v6: ffprobe 50 saniyeye kadar bekler, kanal basina tum calisan alternatifleri korur.\n- v6: aday limiti 30; gec cevap veren CDN/HLS kaynaklarini aceleyle elemez.
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
    "ALTERNATİF DİJİTAL", "ÇOCUK", "BELGESEL", "DİNİ", "MÜZİK",
    "SİNEMA-DİZİ", "EĞİTİM-KÜLTÜR", "KAMU-TEMATİK", "İNTERNET",
]

DEFAULT_FAVORITES = [
    "TRT 1", "ATV", "KANAL D", "SHOW TV", "STAR TV", "NOW", "TV8",
    "KANAL 7", "SÖZCÜ TV", "TV100", "NTV", "CNN TÜRK", "TRT HABER",
    "HABERTÜRK", "HABER GLOBAL", "TRT SPOR", "A SPOR",
]

POPULARITY = DEFAULT_FAVORITES + [
    "A HABER", "HALK TV", "TGRT HABER", "24 TV", "EKOL TV", "TELE1",
    "TRT SPOR YILDIZ", "HT SPOR", "TJK TV", "FB TV", "TRT ÇOCUK",
    "TRT BELGESEL", "TRT 2", "TRT MÜZİK", "A2", "TEVE 2", "DMAX", "TLC",
]

MAX_WORKERS = 12
HTTP_TIMEOUT = 20
FFPROBE_TIMEOUT = 50
MAX_CANDIDATES_PER_CHANNEL = 30
USER_AGENT = "Mozilla/5.0 (MADSC-TV/6.0)"

BLOCKED_HOST_SUFFIXES = ("helga.iptv2022.com", "siauliairsavlt.pw")

TRUSTED_HOST_HINTS = (
    "trt.com.tr", "daioncdn.net", "ercdn.net", "mncdn.com", "tjk.org",
    "powerapp.com.tr", "tgrthaber.com", "duhnet.tv", "mediatriple.net",
    "netmedya.net", "rocketcdn.com", "blutv.com",
)

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
    "CNN TURK":"CNN TÜRK","HABERTURK":"HABERTÜRK","HABERTURK TV":"HABERTÜRK",
    "HABER TURK":"HABERTÜRK","TV 100":"TV100","TV100 TV":"TV100",
    "TV 8 5":"TV8.5","TV8 5":"TV8.5","TV 8,5":"TV8.5","TEVE2":"TEVE 2",
    "ULUSAL TV":"ULUSAL KANAL","TRT COCUK":"TRT ÇOCUK","TRT MUZIK":"TRT MÜZİK",
    "TRT TURK":"TRT TÜRK","TRT KURDI":"TRT KURDİ","MINIKA GO":"MİNİKA GO",
    "MINIKA COCUK":"MİNİKA ÇOCUK","ULKE TV":"ÜLKE TV","DREAM TURK":"DREAM TÜRK",
    "POWER TURK":"POWER TÜRK","A2TV":"A2","A 2":"A2","TV 4":"TV4",
    "KANAL D TURKIYE":"KANAL D","STAR TV TURKIYE":"STAR TV","TV8 TURKIYE":"TV8",
    "HABER GLOBAL TURKIYE":"HABER GLOBAL",
}

CHANNEL_CATEGORY = {
    "TRT 1":"ULUSAL","ATV":"ULUSAL","KANAL D":"ULUSAL","SHOW TV":"ULUSAL",
    "STAR TV":"ULUSAL","NOW":"ULUSAL","TV8":"ULUSAL","KANAL 7":"ULUSAL","360":"ULUSAL",
    "A2":"ULUSAL","TEVE 2":"ULUSAL","BEYAZ TV":"ULUSAL","DMAX":"ULUSAL","TLC":"ULUSAL","TV8.5":"ULUSAL",
    "TV100":"HABER","SÖZCÜ TV":"HABER","TRT HABER":"HABER","NTV":"HABER","HABERTÜRK":"HABER",
    "CNN TÜRK":"HABER","HABER GLOBAL":"HABER","HALK TV":"HABER","TGRT HABER":"HABER",
    "A HABER":"HABER","24 TV":"HABER","EKOL TV":"HABER","TELE1":"HABER",
    "ULUSAL KANAL":"HABER","BLOOMBERG HT":"HABER","A PARA":"HABER","TVNET":"HABER",
    "ÜLKE TV":"HABER","FLASH HABER":"HABER",
    "TRT SPOR":"SPOR","TRT SPOR YILDIZ":"SPOR","A SPOR":"SPOR","HT SPOR":"SPOR","TJK TV":"SPOR","FB TV":"SPOR",
    "TRT ÇOCUK":"ÇOCUK","TRT DİYANET ÇOCUK":"ÇOCUK","MİNİKA GO":"ÇOCUK","MİNİKA ÇOCUK":"ÇOCUK",
    "TRT BELGESEL":"BELGESEL","DİYANET TV":"DİNİ","SEMERKAND TV":"DİNİ","LALEGÜL TV":"DİNİ","DOST TV":"DİNİ",
    "TRT MÜZİK":"MÜZİK","DREAM TÜRK":"MÜZİK","KRAL POP TV":"MÜZİK","POWER TÜRK":"MÜZİK","NUMBER 1 TV":"MÜZİK",
    "TRT 2":"EĞİTİM-KÜLTÜR","TRT AVAZ":"KAMU-TEMATİK","TRT TÜRK":"KAMU-TEMATİK",
    "TRT KURDİ":"KAMU-TEMATİK","TBMM TV":"KAMU-TEMATİK",
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
"TRT DİYANET ÇOCUK":["https://tv-trtdiyanetcocuk.medya.trt.com.tr/master_720.m3u8"],
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

PREMIUM_PATTERNS = ("BEIN","EXXEN","DISNEY","HBO"," S SPORT","SSPORT","TIVIBU","D-SMART","DIGITURK","NETFLIX","GAIN PREMIUM")
RADIO_PATTERNS = ("RADYO","RADIO"," FM")
FOREIGN_HINTS = ("PERSIANA","ALMAHRIAH","MEKAMELEEN","ELSHARQ","AL-ZAHRA","AL ZAHRA","ARABIC","ARAB ","ARABI","IRAN ","AZERBAIJAN","RUSSIA","GERMANY")
LOCAL_TOKENS = {
    "ADANA","ADIYAMAN","AFYON","AKSARAY","AMASYA","ANTALYA","ALANYA","ARDAHAN","ARTVIN","AYDIN","BALIKESIR","BARTIN",
    "BATMAN","BAYBURT","BILECIK","BINGOL","BITLIS","BOLU","BURDUR","BURSA","CANAKKALE","CANKIRI","CORUM","DENIZLI",
    "DIYARBAKIR","DUZCE","EDIRNE","ELAZIG","ERZINCAN","ERZURUM","ESKISEHIR","GAZIANTEP","GIRESUN","GUMUSHANE",
    "HAKKARI","HATAY","IGDIR","ISPARTA","KAHRAMANMARAS","KARABUK","KARAMAN","KARS","KASTAMONU","KAYSERI","KILIS",
    "KIRIKKALE","KIRKLARELI","KIRSEHIR","KOCAELI","KONYA","KUTAHYA","MALATYA","MANISA","MARDIN","MERSIN","MUGLA",
    "MUS","NEVSEHIR","NIGDE","ORDU","OSMANIYE","RIZE","SAKARYA","SAMSUN","SIIRT","SINOP","SIVAS","SANLIURFA",
    "SIRNAK","TEKIRDAG","TOKAT","TRABZON","TUNCELI","USAK","VAN","YALOVA","YOZGAT","ZONGULDAK",
}

def ascii_text(text):
    tr = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iIsSgGuUoOcC")
    return "".join(c for c in unicodedata.normalize("NFKD", str(text).translate(tr)) if not unicodedata.combining(c))

def clean_name(name):
    name = str(name).strip()
    name = re.sub(r"\s*\[(?:NOT\s*24/7|24/7)\]\s*", " ", name, flags=re.I)
    name = re.sub(r"\s*\((?:TURKIYE|TURKEY)\)\s*", " ", name, flags=re.I)
    name = re.sub(r"\s*[•|]\s*ALTERNAT[İI]F(?:\s*\d+)?(?:.*)?$", "", name, flags=re.I)
    name = re.sub(r"\s*-\s*ALTERNAT[İI]F(?:\s*\d+)?(?:.*)?$", "", name, flags=re.I)
    name = re.sub(r"\s*[\(\[]?(?:2160|1440|1080|720|576|480)P?[\)\]]?\s*(?:4K|UHD|QHD|FHD|FULL\s*HD|HD|SD)?\s*$", "", name, flags=re.I)
    name = re.sub(r"\s+(?:4K\s*UHD|4K|UHD|QHD|FHD|FULL\s*HD|HD|SD)\s*$", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" -|•")

def norm_key_text(name):
    k = ascii_text(clean_name(name)).upper()
    k = re.sub(r"[^A-Z0-9]+", " ", k)
    return re.sub(r"\s+", " ", k).strip()

ALIAS_KEYS = {norm_key_text(a): b for a,b in ALIASES.items()}

def key_for(name):
    k = norm_key_text(name)
    return norm_key_text(ALIAS_KEYS.get(k, k))

KNOWN_NAMES = set(EPG_IDS) | set(CURATED) | set(DEFAULT_FAVORITES) | set(CHANNEL_CATEGORY)
KNOWN_BY_KEY = {key_for(x): x for x in KNOWN_NAMES}

def canonical_name(name): return KNOWN_BY_KEY.get(key_for(name), clean_name(name))
def parse_attrs(info): return {m.group(1):m.group(2) for m in re.finditer(r'([\w-]+)="([^"]*)"',info)}

def parse_m3u(text, source):
    out, info = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#EXTINF:"): info=line; continue
        if info and line.startswith(("http://","https://")):
            a=parse_attrs(info); raw_name=info.split(",",1)[-1].strip()
            out.append({"name":canonical_name(raw_name),"raw_name":raw_name,"url":line,"source":source,
                        "logo":a.get("tvg-logo",""),"tvg_id":a.get("tvg-id",""),"group":a.get("group-title",""),
                        "country":a.get("tvg-country",""),"language":a.get("tvg-language",""),
                        "digital_hint":bool(re.search(r"NOT\s*24/7|DIGITAL|WEB\s*TV",raw_name+" "+a.get("group-title",""),re.I))})
            info=None
    return out

def fetch_bytes(url, timeout=HTTP_TIMEOUT, limit=256000, byte_range=None):
    headers={"User-Agent":USER_AGENT,"Accept":"*/*"}
    if byte_range: headers["Range"]=byte_range
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.read(limit),getattr(r,"status",200)

def fetch_text(url, timeout=HTTP_TIMEOUT, limit=4000000):
    return fetch_bytes(url,timeout,limit)[0].decode("utf-8-sig",errors="ignore")

def host_of(url):
    try: return (urllib.parse.urlparse(url).hostname or "").lower()
    except Exception: return ""

def blocked_url(url):
    host=host_of(url)
    if not host: return True
    if any(host==h or host.endswith("."+h) for h in BLOCKED_HOST_SUFFIXES): return True
    return bool(re.search(r"/iptv/[A-Za-z0-9_-]{18,}/",urllib.parse.urlparse(url).path or "",re.I))

def discovery_allowed(e):
    n=ascii_text(e["name"]).upper(); raw=ascii_text(e.get("raw_name","")).upper(); g=ascii_text(e.get("group","")).upper()
    blob=f"{n} {raw} {g}"
    if any(x in blob for x in PREMIUM_PATTERNS+RADIO_PATTERNS+FOREIGN_HINTS) or blocked_url(e["url"]): return False
    if any(x in n for x in ("TRT WORLD","TRT ARABI")): return False
    if key_for(e["name"]) in KNOWN_BY_KEY: return True
    if set(re.findall(r"[A-Z0-9]+",n)) & LOCAL_TOKENS: return False
    country=ascii_text(e.get("country","")).upper()
    if country and not any(x in country for x in ("TR","TUR","TURKEY","TURKIYE")): return False
    if any(x in g for x in ("LOCAL","REGIONAL")): return False
    return any(x in g for x in ("GENERAL","NEWS","SPORT","KIDS","DOCUMENTARY","MUSIC","RELIGIOUS","EDUCATION","LEGISLATIVE"))

def classify(name, group=""):
    cname=canonical_name(name)
    if cname in CHANNEL_CATEGORY: return CHANNEL_CATEGORY[cname]
    x=ascii_text(f"{cname} {group}").upper()
    if any(w in x for w in ("HABER","NEWS","NTV","CNN","BLOOMBERG","SOZCU","HALK TV","TELE1","TV100","EKOL TV","A PARA","TVNET")): return "HABER"
    if any(w in x for w in ("SPOR","SPORT","TJK","FB TV","FENERBAHCE")): return "SPOR"
    if any(w in x for w in ("COCUK","MINIKA","KIDS")): return "ÇOCUK"
    if any(w in x for w in ("BELGESEL","DOCUMENTARY")): return "BELGESEL"
    if any(w in x for w in ("DIYANET","SEMERKAND","LALEGUL","DOST TV","RELIGIOUS")): return "DİNİ"
    if any(w in x for w in ("MUZIK","MUSIC","DREAM","POWER","KRAL POP","NUMBER 1")): return "MÜZİK"
    if any(w in x for w in ("SINEMA","DIZI","MOVIE","FILM","SERIES")): return "SİNEMA-DİZİ"
    if any(w in x for w in ("EGITIM","KULTUR","EDUCATION")): return "EĞİTİM-KÜLTÜR"
    if any(w in x for w in ("TBMM","LEGISLATIVE","TRT AVAZ","TRT TURK","TRT KURDI")): return "KAMU-TEMATİK"
    if any(w in x for w in ("INTERNET","WEB TV","YOUTUBE")): return "İNTERNET"
    return None

def quality_label(w,h):
    if w>=3840 or h>=2160:return "2160P 4K UHD"
    if h>=1440:return "1440P QHD"
    if h>=1080:return "1080P FHD"
    if h>=720:return "720P HD"
    if h>=576:return "576P SD"
    return f"{h}P SD" if h else "KALİTE BİLİNMİYOR"

def hls_precheck(url):
    if ".m3u8" not in url.lower():
        try:
            data,status=fetch_bytes(url,limit=4096)
            return bool(data) and status<400,"HTTP_OK" if data else "HTTP_BOS"
        except Exception as exc:return False,"HTTP_FAIL:"+str(exc)[:100]
    try:
        master=fetch_text(url,limit=700000)
        if "#EXTM3U" not in master:return False,"HLS_HEADER_YOK"
        refs=[x.strip() for x in master.splitlines() if x.strip() and not x.startswith("#")]
        if not refs:return False,"HLS_REFERANS_YOK"
        media_url,media=url,master
        if "#EXT-X-STREAM-INF" in master:
            media_url=urllib.parse.urljoin(url,refs[-1])
            media=fetch_text(media_url,limit=700000)
            if "#EXTM3U" not in media:return False,"CHILD_HLS_BOZUK"
        segs=[x.strip() for x in media.splitlines() if x.strip() and not x.startswith("#")]
        if not segs:return False,"SEGMENT_YOK"
        # Segment kontrolu bilgi amaclidir. CDN'lerin Range/403 davranisi yuzunden
        # tek basina kanali elemez; asil medya dogrulamasi ffprobe'dur.
        segment_url=urllib.parse.urljoin(media_url,segs[-1])
        try:
            data,status=fetch_bytes(segment_url,limit=4096)
            if status<400 and data:return True,"HLS_SEGMENT_OK"
            return True,"HLS_PLAYLIST_OK_SEGMENT_SINIRLI"
        except Exception:
            return True,"HLS_PLAYLIST_OK_SEGMENT_SINIRLI"
    except Exception as exc:return False,"HLS_FAIL:"+str(exc)[:120]

def ffprobe(url):
    try:
        p=subprocess.run(["ffprobe","-v","error","-rw_timeout","45000000","-analyzeduration","10000000","-probesize","10000000",
                          "-select_streams","v:0","-show_entries","stream=codec_name,width,height","-of","json",url],
                         capture_output=True,text=True,timeout=FFPROBE_TIMEOUT)
        if p.returncode!=0:return False,0,0,"",(p.stderr or "")[:220]
        streams=(json.loads(p.stdout or "{}").get("streams") or [])
        if not streams:return False,0,0,"","VIDEO_YOK"
        s=streams[0]; w,h=int(s.get("width") or 0),int(s.get("height") or 0)
        if not w or not h:return False,w,h,s.get("codec_name",""),"COZUNURLUK_YOK"
        return True,w,h,s.get("codec_name",""),"OK"
    except Exception as exc:return False,0,0,"","FFPROBE:"+str(exc)[:150]

def source_bonus(source,url):
    base={"CURATED":900,"ORIJINAL":650,"ONCEKI_CALISAN":600,"DEARBULUT_TR":500,"IPTV_ORG":475}.get(source,300)
    host=host_of(url)
    if any(h in host for h in TRUSTED_HOST_HINTS):base+=450
    if source=="ONCEKI_CALISAN" and not any(h in host for h in TRUSTED_HOST_HINTS):base-=300
    return base

def test_candidate(c):
    if blocked_url(c["url"]):return {**c,"ok":False,"reason":"BLOCKLIST","width":0,"height":0,"codec":"","score":0}
    h_ok,h_reason=hls_precheck(c["url"])
    if not h_ok:return {**c,"ok":False,"reason":h_reason,"width":0,"height":0,"codec":"","score":0}
    ok,w,h,codec,why=ffprobe(c["url"])
    if not ok:return {**c,"ok":False,"reason":why,"width":w,"height":h,"codec":codec,"score":0}
    return {**c,"ok":True,"reason":h_reason,"width":w,"height":h,"codec":codec,
            "score":w*h+source_bonus(c["source"],c["url"])*1000}

def add_candidate(pool,name,url,source,logo="",tvg_id="",group="",digital_hint=False):
    if not url or blocked_url(url):return
    k=key_for(name)
    if not k:return
    cname=canonical_name(name)
    pool.setdefault(k,{"name":cname,"logo":logo,"tvg_id":EPG_IDS.get(cname,tvg_id),"group":group,"candidates":[]})
    r=pool[k]
    if logo and not r["logo"]:r["logo"]=logo
    if EPG_IDS.get(cname):r["tvg_id"]=EPG_IDS[cname]
    elif tvg_id and not r["tvg_id"]:r["tvg_id"]=tvg_id
    if group and not r["group"]:r["group"]=group
    if not any(x["url"]==url for x in r["candidates"]):
        r["candidates"].append({"url":url,"source":source,"digital_hint":bool(digital_hint)})

def load_favorites():
    names=list(DEFAULT_FAVORITES); f=Path("FAVORILER.txt")
    if f.exists():
        for raw in f.read_text(encoding="utf-8-sig",errors="ignore").splitlines():
            n=raw.strip()
            if n and not n.startswith("#"):names.append(canonical_name(n))
    out=[];seen=set()
    for n in names:
        k=key_for(n)
        if k and k not in seen:seen.add(k);out.append(canonical_name(n))
    return out

def extinf(ch,group):
    display=f'{ch["name"]} {quality_label(ch["width"],ch["height"])}'
    tid=EPG_IDS.get(ch["name"],ch.get("tvg_id",""));logo=ch.get("logo","")
    bits=["#EXTINF:-1"]
    if tid:bits.append(f'tvg-id="{tid}"')
    if logo:bits.append(f'tvg-logo="{logo}"')
    bits.append(f'group-title="{group}",{display}')
    return " ".join(bits)

def main():
    if len(sys.argv)<2:raise SystemExit("Kullanim: python3 iptv_test.py MADSC_TV_47_LISTE_ADAY.m3u")
    src=Path(sys.argv[1])
    if not src.exists():raise SystemExit(f"Dosya bulunamadi: {src}")
    favorites=load_favorites();pool={}

    for e in parse_m3u(src.read_text(encoding="utf-8-sig",errors="ignore"),"ORIJINAL"):
        if not discovery_allowed(e) and key_for(e["name"]) not in KNOWN_BY_KEY:continue
        add_candidate(pool,e["name"],e["url"],"ORIJINAL",e["logo"],e["tvg_id"],e["group"],e["digital_hint"])

    for name,urls in CURATED.items():
        for url in urls:add_candidate(pool,name,url,"CURATED")

    previous=Path("CALISANLAR.m3u")
    if previous.exists():
        for e in parse_m3u(previous.read_text(encoding="utf-8-sig",errors="ignore"),"ONCEKI_CALISAN"):
            add_candidate(pool,e["name"],e["url"],"ONCEKI_CALISAN",e["logo"],e["tvg_id"],e["group"],e["digital_hint"])

    for source,url in DISCOVERY_SOURCES:
        try:
            print(f"Kesif kaynagi: {source}",flush=True);accepted=0
            for e in parse_m3u(fetch_text(url,timeout=30),source):
                if discovery_allowed(e):
                    add_candidate(pool,e["name"],e["url"],source,e["logo"],e["tvg_id"],e["group"],e["digital_hint"]);accepted+=1
            print(f"  -> {accepted} uygun aday",flush=True)
        except Exception as exc:print(f"  -> Kaynak okunamadi: {exc}",flush=True)

    for k in list(pool):
        meta=pool[k]
        if classify(meta["name"],meta.get("group","")) is None and k not in KNOWN_BY_KEY:del pool[k]

    priority={"CURATED":0,"ORIJINAL":1,"ONCEKI_CALISAN":2,"DEARBULUT_TR":3,"IPTV_ORG":4}
    jobs=[]
    for k,r in pool.items():
        # v5: ayni kaynaktan gelen 1080/720 gibi yedekleri de kaybetme.
        r["candidates"].sort(key=lambda x:(priority.get(x["source"],99),x["url"]))
        r["candidates"]=r["candidates"][:MAX_CANDIDATES_PER_CHANNEL]
        jobs.extend((k,c) for c in r["candidates"])

    print(f"\nKanal kimligi: {len(pool)} | URL testi: {len(jobs)}",flush=True)
    results=defaultdict(list)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        fmap={ex.submit(test_candidate,c):(k,c) for k,c in jobs};done=0
        for f in as_completed(fmap):
            k,c=fmap[f];done+=1
            try:r=f.result()
            except Exception as exc:r={**c,"ok":False,"reason":str(exc),"width":0,"height":0,"codec":"","score":0}
            results[k].append(r)
            if done%20==0 or done==len(jobs):print(f"Test ilerleme: {done}/{len(jobs)}",flush=True)

    selected={};alternatives={};digital_alternatives={};report=[]
    for k,meta in pool.items():
        tested=results.get(k,[]);good=sorted((x for x in tested if x["ok"]),key=lambda x:x["score"],reverse=True)
        normal_good=[x for x in good if not x.get("digital_hint")]
        main=normal_good[0] if normal_good else (good[0] if good else None)
        for x in tested:
            report.append([meta["name"],"CALISIYOR" if x["ok"] else "CALISMIYOR",
                quality_label(x["width"],x["height"]) if x["ok"] else "",x["width"],x["height"],x["codec"],x["source"],
                x["reason"],x["url"],"EVET" if main and x["url"]==main["url"] else "HAYIR",
                len(meta["candidates"]),EPG_IDS.get(meta["name"],meta.get("tvg_id","")),"EVET" if x.get("digital_hint") else "HAYIR"])
        if not main:continue
        selected[k]={**meta,**main};alternatives[k]=[];digital_alternatives[k]=[]
        seen_alt_urls=set()
        for x in good:
            if x["url"]==main["url"] or x["url"] in seen_alt_urls:continue
            if x["height"]<360:continue
            seen_alt_urls.add(x["url"])
            target=digital_alternatives if x.get("digital_hint") else alternatives
            target[k].append({**meta,**x})

    pop={key_for(n):i for i,n in enumerate(POPULARITY)};grouped=defaultdict(list)
    for k,ch in selected.items():
        cat=classify(ch["name"],ch.get("group",""))
        if cat:grouped[cat].append((k,ch))
    for g in grouped:grouped[g].sort(key=lambda z:(pop.get(z[0],9999),z[1]["name"]))

    lines=[f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"']
    for n in favorites:
        k=key_for(n)
        if k in selected:lines += [extinf(selected[k],"⭐ FAVORİLER"),selected[k]["url"]]

    for group in CATEGORY_ORDER:
        if group=="⭐ FAVORİLER":continue
        if group=="ALTERNATİF":
            ai=[(k,ch) for k,arr in alternatives.items() for ch in arr];ai.sort(key=lambda z:(pop.get(z[0],9999),z[1]["name"]))
            for _,ch in ai:lines += [extinf(ch,group),ch["url"]]
            continue
        if group=="ALTERNATİF DİJİTAL":
            di=[(k,ch) for k,arr in digital_alternatives.items() for ch in arr];di.sort(key=lambda z:(pop.get(z[0],9999),z[1]["name"]))
            for _,ch in di:lines += [extinf(ch,group),ch["url"]]
            continue
        for _,ch in grouped.get(group,[]):lines += [extinf(ch,group),ch["url"]]

    Path("CALISANLAR.m3u").write_text("\n".join(lines)+"\n",encoding="utf-8")
    failed=[r["name"] for k,r in sorted(pool.items(),key=lambda z:z[1]["name"]) if k not in selected]
    Path("CALISMAYANLAR.txt").write_text("\n".join(failed)+("\n" if failed else ""),encoding="utf-8")
    with open("TEST_RAPORU.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f);w.writerow(["Kanal","Durum","Kalite","Genislik","Yukseklik","Codec","Kaynak","Kontrol","URL","Secildi","Aday_Sayisi","EPG_ID","Dijital_Ipucu"]);w.writerows(report)

    print("\n===================================")
    print("MADSC TV v6 TESTI TAMAMLANDI")
    print(f"Kesfedilen kanal    : {len(pool)}")
    print(f"Final calisan       : {len(selected)}")
    print(f"Calismayan          : {len(failed)}")
    print(f"Alternatif          : {sum(len(x) for x in alternatives.values())}")
    print(f"Alternatif dijital  : {sum(len(x) for x in digital_alternatives.values())}")
    print(f"Favori tanimi       : {len(favorites)}")
    print("===================================")

if __name__=="__main__":
    main()
