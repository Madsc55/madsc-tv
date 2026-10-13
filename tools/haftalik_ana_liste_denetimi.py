"""Ana listeyi değiştirmeden haftalık yayın ve EPG teknik denetimi."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

PLAYLIST = pathlib.Path("CALISANLAR.m3u")
OUTPUT = pathlib.Path("madsc_ana_liste_denetimi")
META = re.compile(r'([\w-]+)="([^"]*)"')

def entries():
    result = []
    meta = None
    for line in PLAYLIST.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            attrs = dict(META.findall(line))
            meta = {"name": line.rsplit(",", 1)[-1], "tvg_id": attrs.get("tvg-id", ""),
                    "tvg_name": attrs.get("tvg-name", ""), "group": attrs.get("group-title", "")}
        elif line and not line.startswith("#") and meta is not None:
            result.append({**meta, "url": line})
            meta = None
    return result

def probe(entry):
    # No stream URLs or credentials are written to reports.
    result = {k: entry[k] for k in ("name", "tvg_id", "tvg_name", "group")}
    result["stream_id"] = hashlib.sha256(entry["url"].encode()).hexdigest()[:16]
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-rw_timeout", "12000000",
            "-show_entries", "stream=codec_type", "-of", "json", entry["url"]],
            capture_output=True, text=True, timeout=25)
        streams = json.loads(p.stdout or "{}").get("streams", [])
        kinds = {s.get("codec_type") for s in streams}
        result["video"] = "video" in kinds
        result["audio"] = "audio" in kinds
        result["status"] = "TEKNIK_ERISIM_VAR" if p.returncode == 0 and kinds else "ERISIM_DOGRULANAMADI"
    except (subprocess.TimeoutExpired, ValueError, OSError):
        result["video"] = False
        result["audio"] = False
        result["status"] = "ERISIM_DOGRULANAMADI"
    result["kimlik"] = "GORSEL_DOGRULAMA_GEREKLI"
    return result

def epg_status(rows):
    first = PLAYLIST.read_text(encoding="utf-8-sig").splitlines()[0]
    urls = re.findall(r'(?:x-tvg-url|url-tvg)="([^"]+)"', first)
    if not urls:
        return {"status": "EPG_ADRESI_YOK"}, set()
    try:
        req = urllib.request.Request(urls[0], headers={"User-Agent": "MADSC-weekly-audit/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read(30_000_000)
        root = ET.fromstring(data)
        ids = {node.get("id") for node in root.findall("channel")}
        programs = {}
        for item in root.findall("programme"):
            channel = item.get("channel")
            programs[channel] = programs.get(channel, 0) + 1
        return {"status": "EPG_OK", "channel_count": len(ids),
                "program_count": sum(programs.values())}, set(programs)
    except (OSError, ET.ParseError, ValueError):
        return {"status": "EPG_OKUNAMADI"}, set()

def main():
    OUTPUT.mkdir(exist_ok=True)
    channels = entries()
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        checked = list(executor.map(probe, channels))
    epg, programmed = epg_status(checked)
    for row in checked:
        row["epg"] = ("PROGRAM_KAYDI_VAR" if row["tvg_id"] in programmed else
                      "PROGRAM_ESLESMEDI" if epg["status"] == "EPG_OK" else "EPG_DOGRULANAMADI")
    same_urls = {}
    for row in checked:
        same_urls.setdefault(row["stream_id"], []).append(row["name"])
    duplicate_streams = [names for names in same_urls.values() if len(names) > 1]
    report = {"checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "scope": "Ana liste salt okunur; yayın kimliği ve canlı EPG eşleşmesi ayrıca incelenmeli.",
              "total": len(checked),
              "technical_access": sum(r["status"] == "TEKNIK_ERISIM_VAR" for r in checked),
              "unverified_access": sum(r["status"] != "TEKNIK_ERISIM_VAR" for r in checked),
              "epg": epg, "duplicate_stream_groups": duplicate_streams,
              "channels": checked}
    (OUTPUT / "rapor.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Ana liste: {len(checked)}; teknik erişim: {report['technical_access']}; "
          f"doğrulanamayan: {report['unverified_access']}; EPG: {epg['status']}")
    print("Yayın kimliği ve canlı yayın-EPG eşleşmesi otomatik olarak kesin doğrulanmadı.")

if __name__ == "__main__":
    main()
