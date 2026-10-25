#!/usr/bin/env python3
"""Fetch TVMaze schedule metadata without overwriting prior data on incomplete or invalid responses."""
import datetime
import json
import os
import pathlib
import tempfile
import urllib.request

root = pathlib.Path(__file__).resolve().parents[1]
out = root / "vod" / "guncel-bolumler.json"

def collect(today, opener=urllib.request.urlopen):
    records = []
    successes = 0
    for delta in range(-7, 8):
        day = (today + datetime.timedelta(days=delta)).isoformat()
        url = "https://api.tvmaze.com/schedule?country=TR&date=" + day
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MadscTV-VOD-Metadata/1.0"})
            with opener(req, timeout=20) as response:
                episodes = json.load(response)
            if not isinstance(episodes, list):
                raise ValueError("Expected a list of episodes")
            day_records = []
            for ep in episodes:
                if not isinstance(ep, dict):
                    raise ValueError("Invalid episode")
                show = ep.get("show")
                if show is None:
                    show = {}
                if not isinstance(show, dict):
                    raise ValueError("Invalid show metadata")
                day_records.append({"show": show.get("name"), "episode": ep.get("name"),
                                "season": ep.get("season"), "number": ep.get("number"),
                                "airdate": ep.get("airdate"), "url": ep.get("url"),
                                "watch_url": None})
            records.extend(day_records)
            successes += 1
        except Exception as exc:
            print("Skipped", day, type(exc).__name__)
    return successes, records

def main():
    today = datetime.date.today()
    successes, records = collect(today)
    if successes < 15:
        raise RuntimeError("Incomplete TVMaze schedule; previous metadata preserved")
    payload = {"updated": today.isoformat(),
               "note": "Bölüm yayın takvimi; oynatma bağlantısı değildir.",
               "episodes": records}
    out.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=out.parent,
                                         prefix=".vod-", suffix=".tmp", delete=False) as f:
            temp_name = f.name
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_name, out)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
    print("Episodes", len(records), "successful days", successes)

if __name__ == "__main__":
    main()
