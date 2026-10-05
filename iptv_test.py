import sys
import subprocess
import csv
import re
from pathlib import Path

# =========================================================
# AYARLAR
# =========================================================

EPG_URL = "https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml"

if len(sys.argv) < 2:
    raise SystemExit("Kullanim: python3 iptv_test.py DOSYA.m3u")

src = Path(sys.argv[1])

if not src.exists():
    raise SystemExit(f"Dosya bulunamadi: {src}")

# =========================================================
# GERCEK EPG ID'LERI
# =========================================================

EPG_IDS = {
    "TRT 1": "af0zo9et4xguwsk",
    "KANAL D": "bbwgmhsmhhoatzg",
    "SHOW TV": "pvr08e5grfsebfw",
    "STAR TV": "75tz02ooforewap",
    "ATV": "2zkzbuscxwyjc4k",
    "KANAL 7": "a8t877hb0oandbv",
    "TV8": "w7x32brlcz26ibb",
    "NOW": "m0abaihy7vla6ma",

    "CNN TURK": "ah7mr9ol040kp3b",
    "CNN TÜRK": "ah7mr9ol040kp3b",
    "NTV": "nyz5s8p798n9cqg",
    "TRT HABER": "in3p7jng04mr97m",
    "HABERTURK": "gil1w2erz9l7imc",
    "HABERTÜRK": "gil1w2erz9l7imc",
    "24": "9b7ltozvb9c333g",
    "24 TV": "9b7ltozvb9c333g",
    "A HABER": "ql8qf4vb46o1h7t",
    "TV100": "5i5mds6ap6h7m7w",
    "TV 100": "5i5mds6ap6h7m7w",
    "EKOL TV": "3kluptlla8k8re0",
    "BEYAZ TV": "edf3lp61qexxxhl",
    "TVNET": "njoweqtgl6xngkj",
    "TV NET": "njoweqtgl6xngkj",
    "HABER GLOBAL": "bwmpobxuqn2pz87",
    "360": "cphtdpl9j70cn3a",
    "BLOOMBERG HT": "4nu4fjjhm0y6wqm",
    "TGRT HABER": "qz2fp61itc8xm4g",
    "ULUSAL TV": "rjxdtygyec6mqjz",
    "ULUSAL KANAL": "rjxdtygyec6mqjz",
    "SOZCU TV": "5zoe73avn97ggnt",
    "SÖZCÜ TV": "5zoe73avn97ggnt",
    "SZC TV": "5zoe73avn97ggnt",
    "HALK TV": "d1exl1gxity48nl",
    "TELE1": "2m3k6xyjyek7djr",
    "FLASH HABER": "10bd6fhoe76yplp",

    "TRT SPOR": "v0kvdikxec8nngd",
    "TRT SPOR YILDIZ": "1yyvuttcurbkcnr",
    "A SPOR": "v25znppc6itjprw",
    "HT SPOR": "spgsorunhgejuu2",
    "TJK TV": "jgxiih7f6yhagpj",
    "FB TV": "jemrsooej8d8jku",

    "TRT COCUK": "ybv52n8pldp0lfq",
    "TRT ÇOCUK": "ybv52n8pldp0lfq",
    "MINIKA GO": "phekqx3pyw2wiiq",
    "MİNİKA GO": "phekqx3pyw2wiiq",
    "MINIKA COCUK": "52hjq0o16nwpdnq",
    "MİNİKA ÇOCUK": "52hjq0o16nwpdnq",

    "TRT BELGESEL": "80spas00o3iq47a",

    "TRT 2": "nzdc0yd5xxv43yl",
    "TRT TURK": "xe24vekaidpsql3",
    "TRT TÜRK": "xe24vekaidpsql3",
    "TRT AVAZ": "p6sz5lndgfas2r9",

    "TRT MUZIK": "18ws4yk42js588h",
    "TRT MÜZİK": "18ws4yk42js588h",
    "DREAM TURK": "ttlji9eholru11x",
    "DREAM TÜRK": "ttlji9eholru11x",
    "POWER TURK": "82e4q3ribmz2mt1",
    "POWER TÜRK": "82e4q3ribmz2mt1",

    "DMAX": "6sokobdd9dwe0gl",
    "TLC": "9z32hgan37zhgr6",
    "TV8.5": "pd29xh24glvq4qz",
    "TV 8,5": "pd29xh24glvq4qz",
    "ULKE TV": "kanaalkyymvqcjf",
    "ÜLKE TV": "kanaalkyymvqcjf",
    "A PARA": "8yfvm8ak2t1qoe6",
    "A2": "fc29p3wbp8wkgo4",
    "TEVE2": "6vs4sg9183gdxth",
    "TEVE 2": "6vs4sg9183gdxth",
}

# =========================================================
# LOGOLAR
# Mevcut tvg-logo varsa korunur.
# Buradakiler sadece logo eksikse kullanilir.
# =========================================================

LOGOS = {
    "TRT 1": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/TRT_1_logo.svg/512px-TRT_1_logo.svg.png",
    "TRT 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/TRT_2_logo.svg/512px-TRT_2_logo.svg.png",
    "TV8": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/TV8_logo.svg/512px-TV8_logo.svg.png",
    "ATV": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Atv_logo.svg/512px-Atv_logo.svg.png",
    "SHOW TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Show_TV_logo.svg/512px-Show_TV_logo.svg.png",
    "STAR TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Star_TV_logo.svg/512px-Star_TV_logo.svg.png",
    "KANAL D": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kanal_D_logo.svg/512px-Kanal_D_logo.svg.png",
}

# =========================================================
# YEDEK / ALTERNATIF ACIK YAYIN ADRESLERI
#
# Ana listedeki URL once denenir.
# Calismazsa bu listedeki adresler sirayla denenir.
# =========================================================

FALLBACKS = {
    "TRT 1": [
        "https://tv-trt1.medya.trt.com.tr/master_1080.m3u8",
        "https://tv-trt1.medya.trt.com.tr/master_720.m3u8",
    ],

    "ATV": [
        "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8",
    ],

    "KANAL D": [
        "https://demiroren.daioncdn.net/kanald/kanald.m3u8?app=kanald_web&ce=3",
    ],

    "SHOW TV": [
        "https://ciner-live.daioncdn.net/showtv/showtv_1080p.m3u8",
        "https://ciner-live.daioncdn.net/showtv/showtv_720p.m3u8",
    ],

    "STAR TV": [
        "https://dogus.daioncdn.net/startv/startv_720p.m3u8?app=a20ac41e-bdc3-4aa1-934d-26b484480ac9&ce=3",
    ],

    "TV8": [
        "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/tv8/tv8_1080p.m3u8",
    ],

    "NOW": [
        "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8",
    ],

    "KANAL 7": [
        "https://kanal7-live.daioncdn.net/kanal7/kanal7_1080p.m3u8",
    ],

    "TV100": [
        "https://tv100-live.daioncdn.net/tv100/tv100_1080p.m3u8",
    ],

    "SÖZCÜ TV": [
    "http://5.178.103.239:55/yt1/szctv.m3u8",
    "https://szctvdvr.blutv.com/blutv_szctv_dvr/live_720p4350000kbps/index.m3u8",
],

    "SOZCU TV": [
        "https://szctvdvr.blutv.com/blutv_szctv_dvr/live_720p4350000kbps/index.m3u8",
    ],

    "SZC TV": [
        "https://szctvdvr.blutv.com/blutv_szctv_dvr/live_720p4350000kbps/index.m3u8",
    ],

    "TRT HABER": [
        "https://tv-trthaber.medya.trt.com.tr/master_720.m3u8",
    ],

    "NTV": [
        "https://dogus.daioncdn.net/ntv/ntv_1080p.m3u8",
    ],

    "HABERTÜRK": [
        "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/haberturktv/haberturktv_1080p.m3u8",
    ],

    "CNN TÜRK": [
        "https://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/playlist.m3u8",
    ],

    "HABER GLOBAL": [
        "https://ensonhaber-live.ercdn.net/haberglobal/haberglobal_720p.m3u8",
    ],

    "HALK TV": [
        "https://halktv-live.daioncdn.net/halktv/halktv_1080p.m3u8",
    ],

    "TGRT HABER": [
        "https://canli.tgrthaber.com/tgrt.m3u8",
    ],

    "A HABER": [
        "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/ahaber/ahaber_1080p.m3u8",
    ],

    "24 TV": [
        "https://turkmedya-live.ercdn.net/tv24/tv24_1080p.m3u8",
    ],

    "EKOL TV": [
        "https://ekoltv-live.ercdn.net/ekoltv/ekoltv_1080p.m3u8",
    ],

    "TELE1": [
        "https://tele1-live.ercdn.net/tele1/tele1_1080p.m3u8",
    ],

    "BLOOMBERG HT": [
        "https://ciner-live.daioncdn.net/bloomberght/bloomberght_720p.m3u8",
    ],

    "A PARA": [
        "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/apara/apara_1080p.m3u8",
    ],

    "TRT SPOR": [
        "https://tv-trtspor1.medya.trt.com.tr/master_1080.m3u8",
        "https://tv-trtspor1.medya.trt.com.tr/master_720.m3u8",
    ],

    "A SPOR": [
        "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/aspor/aspor_1080p.m3u8",
    ],

    "TRT ÇOCUK": [
        "https://tv-trtcocuk.medya.trt.com.tr/master_1080.m3u8",
        "https://tv-trtcocuk.medya.trt.com.tr/master_720.m3u8",
    ],

    "TRT BELGESEL": [
        "https://tv-trtbelgesel.medya.trt.com.tr/master_720.m3u8",
    ],

    "TRT 2": [
        "https://tv-trt2.medya.trt.com.tr/master_720.m3u8",
    ],

    "TRT MÜZİK": [
        "https://tv-trtmuzik.medya.trt.com.tr/master_720.m3u8",
    ],
}

# =========================================================
# YARDIMCI FONKSIYONLAR
# =========================================================

def clean_channel_name(name):
    name = re.sub(
        r"\s*[•\-]\s*ALTERNAT[İI]F\s*\d+.*$",
        "",
        name,
        flags=re.IGNORECASE,
    )

    # Ismin sonundaki kalite etiketlerini EPG/fallback eslestirmesi
    # icin temizle. Ekranda gorunen asil isim degistirilmez.
    name = re.sub(
        r"\s+(4K|UHD|FHD|FULL\s*HD|1080P?|720P?|576P?|HD)\s*$",
        "",
        name,
        flags=re.IGNORECASE,
    )

    return name.strip()


def key_for(name):
    return clean_channel_name(name).upper()


def add_logo(info, name):
    # Kaynak listede logo zaten varsa ona dokunma.
    if re.search(r'tvg-logo="[^"]+"', info):
        return info

    logo = LOGOS.get(key_for(name))

    if not logo:
        return info

    if 'tvg-logo="' in info:
        return re.sub(
            r'tvg-logo="[^"]*"',
            f'tvg-logo="{logo}"',
            info
        )

    if "," in info:
        left, right = info.split(",", 1)
        return f'{left} tvg-logo="{logo}",{right}'

    return info


def add_epg_id(info, name):
    epg_id = EPG_IDS.get(key_for(name))

    if not epg_id:
        return info

    if 'tvg-id="' in info:
        return re.sub(
            r'tvg-id="[^"]*"',
            f'tvg-id="{epg_id}"',
            info
        )

    if "," in info:
        left, right = info.split(",", 1)
        return f'{left} tvg-id="{epg_id}",{right}'

    return info


def test_url(url):
    try:
        p = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-rw_timeout", "12000000",
                "-show_entries",
                "stream=codec_type,width,height",
                "-of", "csv=p=0",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        good = p.returncode == 0 and bool(p.stdout.strip())
        detail = (p.stderr or "").strip()[:500]

        return good, detail, p.stdout.strip()

    except Exception as e:
        return False, str(e), ""


def candidate_urls(name, original_url):
    channel = key_for(name)
    fallbacks = FALLBACKS.get(channel, [])

    # Sözcü TV'de güvenilir yedek adresleri önce dene.
    # Ana listedeki üçüncü taraf adres ancak yedekler çalışmazsa denensin.
    if channel in ("SÖZCÜ TV", "SOZCU TV", "SZC TV"):
        result = list(fallbacks)

        if original_url not in result:
            result.append(original_url)

        return result

    # Diğer kanallarda mevcut adres önce denensin.
    result = [original_url]

    for u in fallbacks:
        if u not in result:
            result.append(u)

    return result


# =========================================================
# M3U DOSYASINI OKU
# =========================================================

lines = src.read_text(
    encoding="utf-8-sig",
    errors="ignore"
).splitlines()

items = []
info = None

for line in lines:
    s = line.strip()

    if s.startswith("#EXTINF:"):
        info = s

    elif info and s and not s.startswith("#"):
        name = info.split(",", 1)[-1].strip()
        items.append((info, name, s))
        info = None


# =========================================================
# SOZCU TV LISTEDE HIC YOKSA EKLE
# =========================================================

existing_keys = {key_for(name) for _, name, _ in items}

if not (
    "SÖZCÜ TV" in existing_keys
    or "SOZCU TV" in existing_keys
    or "SZC TV" in existing_keys
):
    sozcu_info = (
        '#EXTINF:-1 '
        'tvg-id="5zoe73avn97ggnt" '
        'group-title="HABER",SÖZCÜ TV HD'
    )

    sozcu_url = (
        "https://szctvdvr.blutv.com/"
        "blutv_szctv_dvr/live_720p4350000kbps/index.m3u8"
    )

    items.append((sozcu_info, "SÖZCÜ TV", sozcu_url))


# =========================================================
# TEST
# =========================================================

ok = []
bad = []
rows = []

for i, (inf, name, original_url) in enumerate(items, 1):

    print(
        f"[{i}/{len(items)}] {name}",
        flush=True
    )

    working_url = None
    last_detail = ""
    probe_info = ""

    urls = candidate_urls(name, original_url)

    for attempt, url in enumerate(urls, 1):

        print(
            f"  -> kaynak {attempt}/{len(urls)}",
            flush=True
        )

        good, detail, probe = test_url(url)

        last_detail = detail

        if good:
            working_url = url
            probe_info = probe
            break

    if working_url:

        fixed_info = add_epg_id(inf, name)
        fixed_info = add_logo(fixed_info, name)

        ok.extend([
            fixed_info,
            working_url
        ])

        durum = "CALISIYOR"

        if working_url != original_url:
            durum = "YEDEK_URL_ILE_CALISIYOR"

        rows.append([
            name,
            durum,
            probe_info,
            working_url,
            original_url,
        ])

    else:

        bad.extend([
            name,
            original_url,
            ""
        ])

        rows.append([
            name,
            "CALISMIYOR",
            last_detail,
            "",
            original_url,
        ])


# =========================================================
# DOSYALARI YAZ
# =========================================================

m3u_header = (
    f'#EXTM3U url-tvg="{EPG_URL}" '
    f'x-tvg-url="{EPG_URL}"'
)

Path("CALISANLAR.m3u").write_text(
    m3u_header + "\n" +
    "\n".join(ok) +
    "\n",
    encoding="utf-8"
)

Path("CALISMAYANLAR.txt").write_text(
    "\n".join(bad),
    encoding="utf-8"
)

with open(
    "TEST_RAPORU.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    w = csv.writer(f)

    w.writerow([
        "Kanal",
        "Durum",
        "FFprobe",
        "Calisan_URL",
        "Orijinal_URL",
    ])

    w.writerows(rows)

print()
print("===================================")
print("IPTV TESTI TAMAMLANDI")
print(f"Toplam kanal : {len(items)}")
print(f"Calisan      : {len(ok) // 2}")
print(f"Calismayan   : {len(bad) // 3}")
print("===================================")
