#!/usr/bin/env python3
"""Fetch TVMaze schedule metadata without destroying the last good snapshot."""
import datetime
import json
import os
from pathlib import Path
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "vod" / "guncel-bolumler.json"


def collect(day, opener=urllib.request.urlopen):
    records = []
    successful_days = 0
    for delta in range(-7, 8):
        date = (day + datetime.timedelta(days=delta)).isoformat()
        url = "https://api.tvmaze.com/schedule?country=TR&date=" + date
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "MadscTV-VOD-Metadata/1.0"})
            with opener(request, timeout=20) as response:
                episodes = json.load(response)
            if not isinstance(episodes, list):
                raise ValueError("Schedule response is not a list")
            successful_days += 1
            for ep in episodes:
                if not isinstance(ep, dict):
                    raise ValueError("Invalid episode record")
                show = ep.get("show") or {}
                records.append({"show": show.get("name"), "episode": ep.get("name"),
                                "season": ep.get("season"), "number": ep.get("number"),
                                "airdate": ep.get("airdate"), "url": ep.get("url"),
                                "watch_url": None})
        except (OSError, ValueError, TypeError, KeyError) as exc:
            print("Skipped", date, str(exc))
    return records, successful_days


def update(out=OUT, day=None, opener=urllib.request.urlopen):
    day = day or datetime.date.today()
    records, successful_days = collect(day, opener)
    if successful_days != 15:
        print("Incomplete schedule: preserving previous snapshot", successful_days, "/15")
        return 1
    payload = {"updated": day.isoformat(),
               "note": "Bölüm yayın takvimi; oynatma bağlantısı değildir.",
               "episodes": records}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=out.parent,
                                         prefix=".vod-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, out)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print("Episodes", len(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(update())
