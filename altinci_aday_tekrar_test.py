#!/usr/bin/env python3
"""Recheck quarantined candidates; never change main playlists or backups."""
import csv
import json
import os
from pathlib import Path
# Import only scanner helper definitions, without executing its full scan.
import ast
import subprocess
import time
import urllib.request
import urllib.parse

def load_probes():
    source = Path("yeni_kanal_tara.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {"fetch", "hls_probe", "ffprobe_stream"}
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names]
    module = ast.Module(body=nodes, type_ignores=[])
    namespace = {"json": json, "subprocess": subprocess, "time": time,
                 "urllib": urllib, "HEADERS": {"User-Agent": "Mozilla/5.0 MADSC-TV-Scanner/2.0"}}
    exec(compile(module, "yeni_kanal_tara.py", "exec"), namespace)
    return namespace["hls_probe"], namespace["ffprobe_stream"]

hls_probe, ffprobe_stream = load_probes()

STATE = Path("aday_bekletme/gecmis.json")
OUT = Path("aday_bekletme/ALTINCI_TEKRAR_TEST.csv")
FIELDS = ["KANAL", "YAYIN_URL", "KAYNAK", "ONCEKI_DURUM", "TEKNIK_TEST", "MEDYA_TEST", "SON_DURUM", "ACIKLAMA"]

def eligible(record):
    return len(record.get("successful_runs", [])) < 2

def check(url, record):
    technical, explanation, _ = hls_probe(url, seconds=20)
    media = "TEST_EDILMEDI"
    if technical == "TEKNIK_AKIS_VAR":
        media, detail = ffprobe_stream(url)
        explanation += "; " + detail
    success = technical == "TEKNIK_AKIS_VAR" and media == "VIDEO_SES_VAR"
    status = "TEKNIK_TEST_GECTI_KIMLIK_BEKLIYOR" if success else "TEKRAR_TEST_BEKLIYOR"
    return [record.get("name", ""), url, record.get("source", ""),
            record.get("technical", ""), technical, media, status, explanation[:300]]

def main():
    history = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if not isinstance(history, dict):
        raise ValueError("Gecmis dosyasi hatali")
    limit = max(0, min(int(os.getenv("RETEST_LIMIT", "10")), 30))
    candidates = [(url, rec) for url, rec in history.items()
                  if isinstance(rec, dict) and eligible(rec)
                  and url.startswith(("https://", "http://"))]
    # Prioritize previously timed-out or once successful candidates.
    candidates.sort(key=lambda x: (-len(x[1].get("successful_runs", [])),
                                   x[1].get("last_seen", ""), x[0]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(FIELDS)
        for url, record in candidates[:limit]:
            writer.writerow(check(url, record))
    print(f"Altinci gelistirme: {min(limit, len(candidates))} aday yeniden denendi; ana liste degismedi")

if __name__ == "__main__":
    main()
