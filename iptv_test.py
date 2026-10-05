import sys
import subprocess
import csv
import re
import urllib.request
import unicodedata
from pathlib import Path


# ============================================================
# AYARLAR
# ============================================================

EPG_URL = (
    "https://raw.githubusercontent.com/"
    "ahmethascelik/epghost/main/xmltv.xml"
)

# Kaynaklardan biri çalışmazsa diğerleri yine kullanılacak.
DISCOVERY_SOURCES = [
    (
        "ONUR_EROZ",
        "https://onureroz.com/indirmeler/turk/index.m3u",
    ),
    (
        "IPTV_ORG",
        "https://iptv-org.github.io/iptv/countries/tr.m3u",
    ),
]

# Aynı URL'nin gereksiz yere tekrar test edilmesini engeller.
MAX_DISCOVERED_PER_CHANNEL = 12


# ============================================================
# EPG ID
# ============================================================

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

    "SÖZCÜ TV": "5zoe73avn97ggnt",
    "SOZCU TV": "5zoe73avn97ggnt",
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

    "TRT ÇOCUK": "ybv52n8pldp0lfq",
    "TRT COCUK": "ybv52n8pldp0lfq",
    "MİNİKA GO": "phekqx3pyw2wiiq",
    "MINIKA GO": "phekqx3pyw2wiiq",
    "MİNİKA ÇOCUK": "52hjq0o16nwpdnq",
    "MINIKA COCUK": "52hjq0o16nwpdnq",

    "TRT BELGESEL": "80spas00o3iq47a",

    "TRT 2": "nzdc0yd5xxv43yl",
    "TRT TÜRK": "xe24vekaidpsql3",
    "TRT TURK": "xe24vekaidpsql3",
    "TRT AVAZ": "p6sz5lndgfas2r9",

    "TRT MÜZİK": "18ws4yk42js588h",
    "TRT MUZIK": "18ws4yk42js588h",
    "DREAM TÜRK": "ttlji9eholru11x",
    "DREAM TURK": "ttlji9eholru11x",
    "POWER TÜRK": "82e4q3ribmz2mt1",
    "POWER TURK": "82e4q3ribmz2mt1",

    "DMAX": "6sokobdd9dwe0gl",
    "TLC": "9z32hgan37zhgr6",
    "TV8.5": "pd29xh24glvq4qz",
    "TV 8,5": "pd29xh24glvq4qz",
    "ÜLKE TV": "kanaalkyymvqcjf",
    "ULKE TV": "kanaalkyymvqcjf",
    "A PARA": "8yfvm8ak2t1qoe6",
    "A2": "fc29p3wbp8wkgo4",
    "TEVE 2": "6vs4sg9183gdxth",
    "TEVE2": "6vs4sg9183gdxth",
}


# ============================================================
# LOGOLAR
# M3U'da mevcut logo varsa ona dokunulmaz.
# ============================================================

LOGOS = {
    "TRT 1": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/3/3e/TRT_1_logo.svg/512px-TRT_1_logo.svg.png"
    ),
    "TRT 2": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/1/11/TRT_2_logo.svg/512px-TRT_2_logo.svg.png"
    ),
    "TV8": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/7/7c/TV8_logo.svg/512px-TV8_logo.svg.png"
    ),
    "ATV": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/5/5e/Atv_logo.svg/512px-Atv_logo.svg.png"
    ),
    "SHOW TV": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/5/5c/Show_TV_logo.svg/512px-Show_TV_logo.svg.png"
    ),
    "STAR TV": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/4/41/Star_TV_logo.svg/512px-Star_TV_logo.svg.png"
    ),
    "KANAL D": (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/4/4c/Kanal_D_logo.svg/512px-Kanal_D_logo.svg.png"
    ),
}


# ============================================================
# BİZİM BİLDİĞİMİZ YEDEKLER
# ============================================================

FALLBACKS = {
    "TRT 1": [
        "https://tv-trt1.medya.trt.com.tr/master_1080.m3u8",
        "https://tv-trt1.medya.trt.com.tr/master_720.m3u8",
    ],

    "ATV": [
        "https://rnttwmjcin.turknet.ercdn.net/"
        "lcpmvefbyo/atv/atv_1080p.m3u8",
    ],

    "KANAL D": [
        "https://demiroren.daioncdn.net/kanald/"
        "kanald.m3u8?app=kanald_web&ce=3",
    ],

    "SHOW TV": [
        "https://ciner-live.daioncdn.net/showtv/showtv_1080p.m3u8",
        "https://ciner-live.daioncdn.net/showtv/showtv_720p.m3u8",
    ],

    "STAR TV": [
        "https://dogus.daioncdn.net/startv/"
        "startv_720p.m3u8?"
        "app=a20ac41e-bdc3-4aa1-934d-26b484480ac9&ce=3",
    ],

    "TV8": [
        "https://rkhubpaomb.turknet.ercdn.net/"
        "fwjkgpasof/tv8/tv8_1080p.m3u8",
    ],

    "NOW": [
        "https://uycyyuuzyh.turknet.ercdn.net/"
        "nphindgytw/nowtv/nowtv.m3u8",
    ],

    "KANAL 7": [
        "https://kanal7-live.daioncdn.net/"
        "kanal7/kanal7_1080p.m3u8",
    ],

    "TV100": [
        "https://tv100-live.daioncdn.net/"
        "tv100/tv100_1080p.m3u8",
    ],

    "SÖZCÜ TV": [
        "http://5.178.103.239:55/yt1/szctv.m3u8",
        (
            "https://szctvdvr.blutv.com/"
            "blutv_szctv_dvr/"
            "live_720p4350000kbps/index.m3u8"
        ),
    ],

    "TRT HABER": [
        "https://tv-trthaber.medya.trt.com.tr/master_720.m3u8",
    ],

    "NTV": [
        "https://dogus.daioncdn.net/ntv/ntv_1080p.m3u8",
    ],

    "HABERTÜRK": [
        "https://rmtftbjlne.turknet.ercdn.net/"
        "bpeytmnqyp/haberturktv/"
        "haberturktv_1080p.m3u8",
    ],

    "CNN TÜRK": [
        "https://live.duhnet.tv/S2/HLS_LIVE/"
        "cnnturknp/playlist.m3u8",
    ],

    "HABER GLOBAL": [
        "https://ensonhaber-live.ercdn.net/"
        "haberglobal/haberglobal_720p.m3u8",
    ],

    "HALK TV": [
        "https://halktv-live.daioncdn.net/"
        "halktv/halktv_1080p.m3u8",
    ],

    "TGRT HABER": [
        "https://canli.tgrthaber.com/tgrt.m3u8",
    ],

    "A HABER": [
        "https://rnttwmjcin.turknet.ercdn.net/"
        "lcpmvefbyo/ahaber/ahaber_1080p.m3u8",
    ],

    "24 TV": [
        "https://turkmedya-live.ercdn.net/"
        "tv24/tv24_1080p.m3u8",
    ],

    "EKOL TV": [
        "https://ekoltv-live.ercdn.net/"
        "ekoltv/ekoltv_1080p.m3u8",
    ],

    "TELE1": [
        "https://tele1-live.ercdn.net/"
        "tele1/tele1_1080p.m3u8",
    ],

    "BLOOMBERG HT": [
        "https://ciner-live.daioncdn.net/"
        "bloomberght/bloomberght_720p.m3u8",
    ],

    "A PARA": [
        "https://rnttwmjcin.turknet.ercdn.net/"
        "lcpmvefbyo/apara/apara_1080p.m3u8",
    ],

    "TRT SPOR": [
        "https://tv-trtspor1.medya.trt.com.tr/master_1080.m3u8",
        "https://tv-trtspor1.medya.trt.com.tr/master_720.m3u8",
    ],

    "A SPOR": [
        "https://rnttwmjcin.turknet.ercdn.net/"
        "lcpmvefbyo/aspor/aspor_1080p.m3u8",
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


# ============================================================
# İSİM NORMALLEŞTİRME
# ============================================================

ALIASES = {
    "SZC TV": "SOZCU TV",
    "SOZCU": "SOZCU TV",

    "CNN TURK": "CNN TURK",
    "HABERTURK": "HABERTURK",

    "TV 100": "TV100",

    "TV 8 5": "TV8.5",
    "TV8 5": "TV8.5",

    "TEVE2": "TEVE 2",

    "ULUSAL TV": "ULUSAL KANAL",
}


def ascii_text(text):
    replacements = str.maketrans({
        "ı": "i",
        "İ": "I",
        "ş": "s",
        "Ş": "S",
        "ğ": "g",
        "Ğ": "G",
        "ü": "u",
        "Ü": "U",
        "ö": "o",
        "Ö": "O",
        "ç": "c",
        "Ç": "C",
    })

    text = text.translate(replacements)

    return "".join(
        c
        for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )


def clean_channel_name(name):
    name = name.strip()

    # ALTERNATIF 1, ALTERNATIF 2 vb.
    name = re.sub(
        r"\s*[•\-]?\s*ALTERNAT[İI]F\s*\d+.*$",
        "",
        name,
        flags=re.IGNORECASE,
    )

    # Sondaki kalite etiketleri
    name = re.sub(
        r"\s*[\-\|•]?\s*"
        r"(4K|UHD|FHD|FULL\s*HD|"
        r"2160P?|1440P?|1080P?|720P?|576P?|HD)"
        r"\s*$",
        "",
        name,
        flags=re.IGNORECASE,
    )

    return name.strip()


def key_for(name):
    key = clean_channel_name(name)

    key = ascii_text(key).upper()

    key = re.sub(
        r"[^A-Z0-9]+",
        " ",
        key,
    )

    key = re.sub(
        r"\s+",
        " ",
        key,
    ).strip()

    key = ALIASES.get(key, key)

    return key


# Normalize dictionaries once.
NORMALIZED_EPG_IDS = {
    key_for(k): v
    for k, v in EPG_IDS.items()
}

NORMALIZED_LOGOS = {
    key_for(k): v
    for k, v in LOGOS.items()
}

NORMALIZED_FALLBACKS = {}

for channel_name, urls in FALLBACKS.items():
    channel_key = key_for(channel_name)

    NORMALIZED_FALLBACKS.setdefault(
        channel_key,
        []
    )

    for url in urls:
        if url not in NORMALIZED_FALLBACKS[channel_key]:
            NORMALIZED_FALLBACKS[channel_key].append(url)


# ============================================================
# EPG / LOGO
# ============================================================

def add_epg_id(info, name):
    epg_id = NORMALIZED_EPG_IDS.get(
        key_for(name)
    )

    if not epg_id:
        return info

    if 'tvg-id="' in info:
        return re.sub(
            r'tvg-id="[^"]*"',
            f'tvg-id="{epg_id}"',
            info,
        )

    if "," in info:
        left, right = info.split(",", 1)

        return (
            f'{left} tvg-id="{epg_id}",'
            f'{right}'
        )

    return info


def add_logo(info, name):
    # Var olan gerçek logo korunur.
    match = re.search(
        r'tvg-logo="([^"]*)"',
        info,
    )

    if match and match.group(1).strip():
        return info

    logo = NORMALIZED_LOGOS.get(
        key_for(name)
    )

    if not logo:
        return info

    if 'tvg-logo="' in info:
        return re.sub(
            r'tvg-logo="[^"]*"',
            f'tvg-logo="{logo}"',
            info,
        )

    if "," in info:
        left, right = info.split(",", 1)

        return (
            f'{left} tvg-logo="{logo}",'
            f'{right}'
        )

    return info


# ============================================================
# M3U PARSER
# ============================================================

def parse_m3u(text):
    entries = []

    info = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#EXTINF:"):
            info = line
            continue

        if (
            info
            and not line.startswith("#")
            and (
                line.startswith("http://")
                or line.startswith("https://")
            )
        ):
            name = info.split(",", 1)[-1].strip()

            entries.append(
                (
                    info,
                    name,
                    line,
                )
            )

            info = None

    return entries


# ============================================================
# KAYNAK KEŞFİ
# ============================================================

def download_text(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "Chrome/120 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=20,
    ) as response:
        return response.read().decode(
            "utf-8-sig",
            errors="ignore",
        )


def load_discovery_sources():
    by_channel = {}

    total = 0

    for source_name, source_url in DISCOVERY_SOURCES:
        try:
            print(
                f"Kesif kaynagi okunuyor: "
                f"{source_name}",
                flush=True,
            )

            text = download_text(source_url)

            entries = parse_m3u(text)

            print(
                f"  -> {len(entries)} yayin bulundu",
                flush=True,
            )

            for _, name, url in entries:
                channel = key_for(name)

                if not channel:
                    continue

                by_channel.setdefault(
                    channel,
                    []
                )

                record = (
                    url,
                    source_name,
                )

                if record not in by_channel[channel]:
                    by_channel[channel].append(
                        record
                    )

                total += 1

        except Exception as exc:
            # Bir kaynak bozulursa bütün test durmaz.
            print(
                f"  -> Kaynak okunamadi: "
                f"{source_name}: {exc}",
                flush=True,
            )

    print(
        f"Kesif tamamlandi. "
        f"Toplam aday kaydi: {total}",
        flush=True,
    )

    return by_channel


DISCOVERED_STREAMS = load_discovery_sources()


# ============================================================
# YAYIN TESTİ
# ============================================================

def test_url(url):
    try:
        process = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-rw_timeout",
                "12000000",
                "-show_entries",
                "stream=codec_type,width,height",
                "-of",
                "csv=p=0",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        probe = process.stdout.strip()

        good = (
            process.returncode == 0
            and bool(probe)
        )

        detail = (
            process.stderr or ""
        ).strip()[:500]

        width = 0
        height = 0

        if good:
            for line in probe.splitlines():
                parts = [
                    part.strip()
                    for part in line.split(",")
                ]

                if "video" not in parts:
                    continue

                numbers = []

                for part in parts:
                    if part.isdigit():
                        numbers.append(
                            int(part)
                        )

                if len(numbers) >= 2:
                    width = numbers[0]
                    height = numbers[1]
                    break

        return (
            good,
            detail,
            probe,
            width,
            height,
        )

    except Exception as exc:
        return (
            False,
            str(exc),
            "",
            0,
            0,
        )


# ============================================================
# ADAY HAVUZU
# ============================================================

def candidate_urls(name, original_url):
    channel = key_for(name)

    result = []

    def add(url, source):
        if not url:
            return

        for existing_url, _ in result:
            if existing_url == url:
                return

        result.append(
            (
                url,
                source,
            )
        )

    # Bizim tanımladığımız yedekler.
    for url in NORMALIZED_FALLBACKS.get(
        channel,
        []
    ):
        add(
            url,
            "FALLBACK",
        )

    # Onur Eröz + IPTV-org.
    discovery_count = 0

    for url, source_name in DISCOVERED_STREAMS.get(
        channel,
        []
    ):
        if discovery_count >= MAX_DISCOVERED_PER_CHANNEL:
            break

        old_length = len(result)

        add(
            url,
            source_name,
        )

        if len(result) > old_length:
            discovery_count += 1

    # Dünkü / ana listedeki URL ASLA unutulmaz.
    add(
        original_url,
        "ORIJINAL",
    )

    return result


# ============================================================
# KALİTE
# ============================================================

def quality_label(width, height):
    if width >= 3840 or height >= 2160:
        return "4K"

    if height >= 1440:
        return "1440P"

    if height >= 1080:
        return "1080P"

    if height >= 720:
        return "720P"

    if height >= 576:
        return "576P"

    if height > 0:
        return f"{height}P"

    return "BILINMIYOR"


def stream_score(width, height, source):
    # En önemli kriter gerçek çözünürlük.
    pixels = width * height

    if pixels <= 0:
        pixels = 1

    # Aynı çözünürlükte bizim bilinen fallback
    # ve mevcut çalışan kaynak biraz daha güvenli kabul edilir.
    source_bonus = {
        "FALLBACK": 30,
        "ORIJINAL": 20,
        "IPTV_ORG": 10,
        "ONUR_EROZ": 10,
    }.get(
        source,
        0,
    )

    return (
        pixels,
        source_bonus,
    )


# ============================================================
# ANA DOSYAYI OKU
# ============================================================

if len(sys.argv) < 2:
    raise SystemExit(
        "Kullanim: "
        "python3 iptv_test.py DOSYA.m3u"
    )

src = Path(
    sys.argv[1]
)

if not src.exists():
    raise SystemExit(
        f"Dosya bulunamadi: {src}"
    )

source_text = src.read_text(
    encoding="utf-8-sig",
    errors="ignore",
)

items = parse_m3u(
    source_text
)


# ============================================================
# SÖZCÜ ANA LİSTEDE YOKSA EKLE
# ============================================================

existing_keys = {
    key_for(name)
    for _, name, _ in items
}

if key_for("SÖZCÜ TV") not in existing_keys:
    sozcu_info = (
        '#EXTINF:-1 '
        'tvg-id="5zoe73avn97ggnt" '
        'group-title="HABER",'
        'SÖZCÜ TV'
    )

    # Sadece başlangıç adayıdır.
    # Keşif sistemi diğer Sözcü adreslerini de ekler.
    sozcu_url = (
        "http://5.178.103.239:55/"
        "yt1/szctv.m3u8"
    )

    items.append(
        (
            sozcu_info,
            "SÖZCÜ TV",
            sozcu_url,
        )
    )


# ============================================================
# TEST
# ============================================================

working_lines = []
bad_lines = []
report_rows = []

for index, (
    info,
    name,
    original_url,
) in enumerate(
    items,
    1,
):
    print()
    print(
        f"[{index}/{len(items)}] {name}",
        flush=True,
    )

    candidates = candidate_urls(
        name,
        original_url,
    )

    print(
        f"  Aday sayisi: {len(candidates)}",
        flush=True,
    )

    best = None

    last_detail = ""

    for attempt, (
        url,
        source_name,
    ) in enumerate(
        candidates,
        1,
    ):
        print(
            f"  -> {attempt}/{len(candidates)} "
            f"[{source_name}]",
            flush=True,
        )

        (
            good,
            detail,
            probe,
            width,
            height,
        ) = test_url(url)

        last_detail = detail

        if not good:
            continue

        score = stream_score(
            width,
            height,
            source_name,
        )

        candidate = {
            "url": url,
            "source": source_name,
            "probe": probe,
            "width": width,
            "height": height,
            "score": score,
        }

        if (
            best is None
            or candidate["score"] > best["score"]
        ):
            best = candidate

    if best is not None:
        fixed_info = add_epg_id(
            info,
            name,
        )

        fixed_info = add_logo(
            fixed_info,
            name,
        )

        working_lines.extend(
            [
                fixed_info,
                best["url"],
            ]
        )

        quality = quality_label(
            best["width"],
            best["height"],
        )

        if best["url"] == original_url:
            status = "ORIJINAL_CALISIYOR"
        else:
            status = "EN_IYI_ADAY_SECILDI"

        report_rows.append(
            [
                name,
                status,
                quality,
                best["width"],
                best["height"],
                best["source"],
                best["probe"],
                best["url"],
                original_url,
                len(candidates),
            ]
        )

        print(
            f"  SECILDI -> "
            f"{quality} "
            f"{best['width']}x{best['height']} "
            f"[{best['source']}]",
            flush=True,
        )

        print(
            f"  URL -> {best['url']}",
            flush=True,
        )

    else:
        bad_lines.extend(
            [
                name,
                original_url,
                "",
            ]
        )

        report_rows.append(
            [
                name,
                "CALISMIYOR",
                "",
                0,
                0,
                "",
                last_detail,
                "",
                original_url,
                len(candidates),
            ]
        )

        print(
            "  CALISAN KAYNAK BULUNAMADI",
            flush=True,
        )


# ============================================================
# CALISANLAR.M3U
# ============================================================

m3u_header = (
    f'#EXTM3U '
    f'url-tvg="{EPG_URL}" '
    f'x-tvg-url="{EPG_URL}"'
)

Path(
    "CALISANLAR.m3u"
).write_text(
    m3u_header
    + "\n"
    + "\n".join(working_lines)
    + "\n",
    encoding="utf-8",
)


# ============================================================
# CALISMAYANLAR.TXT
# ============================================================

Path(
    "CALISMAYANLAR.txt"
).write_text(
    "\n".join(bad_lines),
    encoding="utf-8",
)


# ============================================================
# TEST_RAPORU.CSV
# ============================================================

with open(
    "TEST_RAPORU.csv",
    "w",
    newline="",
    encoding="utf-8-sig",
) as file:
    writer = csv.writer(
        file
    )

    writer.writerow(
        [
            "Kanal",
            "Durum",
            "Kalite",
            "Genislik",
            "Yukseklik",
            "Kaynak",
            "FFprobe",
            "Secilen_URL",
            "Orijinal_URL",
            "Aday_Sayisi",
        ]
    )

    writer.writerows(
        report_rows
    )


# ============================================================
# SONUÇ
# ============================================================

working_count = (
    len(working_lines) // 2
)

failed_count = (
    len(bad_lines) // 3
)

print()
print("===================================")
print("MADSC IPTV TESTI TAMAMLANDI")
print(f"Toplam kanal : {len(items)}")
print(f"Calisan      : {working_count}")
print(f"Calismayan   : {failed_count}")
print("===================================")
