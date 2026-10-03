import sys
import subprocess
import csv
import re
import urllib.request
from pathlib import Path

src = Path(sys.argv[1])
lines = src.read_text(encoding="utf-8-sig", errors="ignore").splitlines()

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

# Kanal logoları
LOGOS = {
    "TRT 1": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/TRT_1_logo.svg/512px-TRT_1_logo.svg.png",
    "TRT 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/TRT_2_logo.svg/512px-TRT_2_logo.svg.png",
    "TV8": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/TV8_logo.svg/512px-TV8_logo.svg.png",
    "ATV": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Atv_logo.svg/512px-Atv_logo.svg.png",
    "SHOW TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Show_TV_logo.svg/512px-Show_TV_logo.svg.png",
    "STAR TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Star_TV_logo.svg/512px-Star_TV_logo.svg.png",
    "KANAL D": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kanal_D_logo.svg/512px-Kanal_D_logo.svg.png",
}
EPG_IDS = {
    "TRT 1": "TRT 1",
    "TRT 2": "TRT 2",
    "TV8": "TV8",
    "ATV": "ATV",
    "SHOW TV": "Show TV",
    "STAR TV": "STAR",
    "KANAL D": "KANAL D",
}
def clean_channel_name(name):
    # "TRT 1 • ALTERNATİF 2" -> "TRT 1"
    return re.sub(
        r"\s*[•\-]\s*ALTERNAT[İI]F\s*\d+.*$",
        "",
        name,
        flags=re.IGNORECASE,
    ).strip()

def add_logo(info, name):
    channel = clean_channel_name(name)
    logo = LOGOS.get(channel.upper())

    if not logo:
        return info

    # Varsa eski tvg-logo değerini değiştir
    if 'tvg-logo="' in info:
        return re.sub(
            r'tvg-logo="[^"]*"',
            f'tvg-logo="{logo}"',
            info
        )

    # Yoksa #EXTINF satırına ekle
    if "," in info:
        left, right = info.split(",", 1)
        return f'{left} tvg-logo="{logo}",{right}'

    return info

def add_epg_id(info, name):
    channel = clean_channel_name(name)
    epg_id = EPG_IDS.get(channel.upper())

    if not epg_id:
        return info

    if 'tvg-id="' in info:
        return re.sub(r'tvg-id="[^"]*"', f'tvg-id="{epg_id}"', info)

    if "," in info:
        left, right = info.split(",", 1)
        return f'{left} tvg-id="{epg_id}",{right}'

    return info

ok = ['#EXTM3U url-tvg="https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml"']
bad = []
rows = []

for i, (inf, name, url) in enumerate(items, 1):
    print(f"[{i}/{len(items)}] {name}", flush=True)

    try:
        p = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-rw_timeout", "12000000",
                "-show_entries", "stream=codec_type",
                "-of", "csv=p=0",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        good = p.returncode == 0 and bool(p.stdout.strip())
        detail = (p.stderr or "").strip()[:500]

    except Exception as e:
        good = False
        detail = str(e)

    if good:
        inf_with_logo = add_logo(inf, name)
        inf_with_logo = add_epg_id(inf_with_logo, name)
        ok += [inf_with_logo, url]
        ok[0] = '#EXTM3U url-tvg="https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml"'
    else:
        bad += [name, url, ""]

    rows.append([
        name,
        "CALISIYOR" if good else "CALISMIYOR",
        detail,
        url
    ])

epg_url = "https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml"

m3u_header = f'#EXTM3U url-tvg="{epg_url}"'

Path("CALISANLAR.m3u").write_text(
    m3u_header + "\n" + "\n".join(ok) + "\n",
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
    w.writerow(["Kanal", "Durum", "Detay", "URL"])
    w.writerows(rows)
