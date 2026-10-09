#!/usr/bin/env python3
"""Import successful technical candidates from two completed GitHub Actions runs into a separate backup M3U."""
import csv, io, json, os, re, urllib.request, urllib.parse, zipfile
from pathlib import Path

REPO = "Madsc55/madsc-tv"
RUNS = [37917250685, 37930058848]
TOKEN = os.environ["GH_TOKEN"]
HEADERS = {"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json", "User-Agent": "madsc-tv-backup"}
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and urllib.parse.urlparse(newurl).hostname != "api.github.com":
            redirected.remove_header("Authorization")
            redirected.headers.pop("Authorization", None)
            redirected.unredirected_hdrs.pop("Authorization", None)
        return redirected

def get(url):
    opener = urllib.request.build_opener(SafeRedirect())
    with opener.open(urllib.request.Request(url, headers=HEADERS), timeout=50) as response:
        return response.read()
def entries(text):
    meta = None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            meta = line
        elif meta and line.startswith(("https://", "http://")):
            yield meta.rsplit(",", 1)[-1], line
            meta = None
def norm(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper().translate(str.maketrans("İÇŞĞÜÖ", "ICSGUO")))
existing = list(entries(Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig")))
known_urls = {u for _, u in existing}
known_names = {norm(n) for n, _ in existing}
prior = Path("yedekler/ADAY_KANALLAR_2026-10-09.txt")
if prior.exists():
    known_urls.update(u for _, u in entries(prior.read_text(encoding="utf-8-sig")))
passed = {}
for run in RUNS:
    payload = json.loads(get(f"https://api.github.com/repos/{REPO}/actions/runs/{run}/artifacts?per_page=100"))
    artifacts = [a for a in payload["artifacts"] if a["name"].startswith("YENILER-KANAL-ADAYLARI-GRUP-")]
    expected = 34 if run == RUNS[0] else 66
    if len(artifacts) != expected:
        raise RuntimeError(f"Missing artifacts in run {run}: {len(artifacts)}/{expected}")
    for a in artifacts:
        with zipfile.ZipFile(io.BytesIO(get(a["archive_download_url"]))) as z:
            for row in csv.DictReader(io.StringIO(z.read("YENILER_TARAMA_RAPORU.csv").decode("utf-8-sig"))):
                if row.get("TEKNIK_TEST") != "TEKNIK_AKIS_VAR" or row.get("MEDYA_TEST") != "VIDEO_SES_VAR":
                    continue
                url = row["YAYIN_URL"].strip()
                if url not in known_urls and url not in passed:
                    passed[url] = row
out = Path("yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u")
out.parent.mkdir(exist_ok=True)
lines = ["#EXTM3U"]
for url, row in sorted(passed.items(), key=lambda item: item[1]["KANAL"].casefold()):
    name = row["KANAL"].replace("\n", " ").replace("\r", " ").replace('"', "'")
    kind = "YEDEK ALTERNATIF" if norm(name) in known_names else "YEDEK YENI ADAY"
    lines += [f'#EXTINF:-1 group-title="{kind}",{name} [TEKNIK TEST - KANAL KIMLIGI DOGRULANMADI]', url]
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Saved {len(passed)} distinct technically tested candidate streams to {out}")
