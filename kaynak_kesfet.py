#!/usr/bin/env python3
"""Discover public Turkish IPTV M3U sources; report only, never auto-trust or edit playlists."""
import csv
import datetime
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

QUERIES = ["iptv turkey m3u", "turkiye iptv", "turkish iptv playlist", "turk tv m3u", "turkish channels m3u"]
MAX_REPOS = 60
MAX_SOURCES = 120
MAX_AGE_DAYS = 90
NOW = datetime.datetime.now(datetime.timezone.utc)
OUT = Path("YENI_KAYNAK_ONERILERI.csv")
ERR = Path("KAYNAK_KESIF_HATALARI.txt")
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "MADSC-TV-source-discovery"}
if os.getenv("GITHUB_TOKEN"):
    HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

def get(url, limit=2000000):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=12) as response:
        return response.read(limit)

def api(url):
    return json.loads(get(url))

existing_script = Path("yeni_kanal_tara.py").read_text(encoding="utf-8")
rows, errors, seen_repos, seen_urls = [], [], set(), set()
repos = []
for query in QUERIES:
    try:
        url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
            {"q": query, "sort": "updated", "per_page": 30})
        for item in api(url).get("items", []):
            if item["full_name"] not in seen_repos and not item.get("archived"):
                repos.append(item)
                seen_repos.add(item["full_name"])
    except Exception as exc:
        errors.append("search " + query + ": " + str(exc))

for repo in repos[:MAX_REPOS]:
    pushed = repo.get("pushed_at", "")
    if pushed:
        try:
            if (NOW - datetime.datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days > MAX_AGE_DAYS:
                continue
        except ValueError:
            continue
    full = repo["full_name"]
    branch = repo.get("default_branch", "main")
    try:
        tree_url = "https://api.github.com/repos/" + full + "/git/trees/" + urllib.parse.quote(branch, safe="") + "?recursive=1"
        tree = api(tree_url)
        paths = [item["path"] for item in tree.get("tree", [])
                 if item.get("type") == "blob" and item["path"].lower().endswith((".m3u", ".m3u8"))
                 and any(word in item["path"].lower() for word in ("tr", "tur", "türk", "turk", "kanal", "iptv"))]
        for path in paths[:8]:
            if len(rows) >= MAX_SOURCES:
                break
            raw = "https://raw.githubusercontent.com/" + full + "/" + urllib.parse.quote(branch, safe="") + "/" + urllib.parse.quote(path, safe="/")
            if raw in seen_urls:
                continue
            seen_urls.add(raw)
            if raw in existing_script:
                continue
            try:
                body = get(raw, limit=300000).decode("utf-8-sig", errors="replace")
                if not body.lstrip().startswith("#EXTM3U"):
                    continue
                count = sum(line.startswith("#EXTINF") for line in body.splitlines())
                if count == 0:
                    continue
                commit_api = ("https://api.github.com/repos/" + full +
                              "/commits?" + urllib.parse.urlencode({"path": path, "per_page": 1}))
                try:
                    commits = api(commit_api)
                    changed = commits[0]["commit"]["committer"]["date"] if commits else ""
                    age = (NOW - datetime.datetime.fromisoformat(changed.replace("Z", "+00:00"))).days
                except Exception as exc:
                    errors.append("Tarih dogrulanamadi " + full + "/" + path + ": " + str(exc))
                    continue
                if age < 0 or age > MAX_AGE_DAYS:
                    continue
                rows.append((full, path, raw, count, changed, age, "ONERI_KONTROL_GEREKLI"))
            except Exception as exc:
                errors.append(raw + ": " + str(exc))
    except Exception as exc:
        errors.append(full + ": " + str(exc))

with OUT.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(("DEPO", "DOSYA", "KAYNAK_URL", "YAKLASIK_KANAL", "DOSYA_SON_GUNCELLEME", "YAS_GUN", "DURUM"))
    writer.writerows(sorted(rows, key=lambda row: row[5]))
ERR.write_text("\n".join(errors) or "Hata yok", encoding="utf-8")
print(f"Kaynak kesfi: {len(repos[:MAX_REPOS])} depo incelendi, {len(rows)} yeni kaynak onerisi; otomatik ekleme yapilmadi.")
