#!/usr/bin/env python3
"""Export an isolated IBO trial M3U from verified 3-pass + continuity evidence."""
import argparse
import hashlib
import json
from pathlib import Path

PASS = {"TECHNICAL_PASS_IDENTITY_PENDING", "TECHNICAL_PASS_CONTENT_REVIEW"}

def export(root, output, limit=50):
    root = Path(root)
    results = json.loads((root / "madsc_son_kontrol/results.json").read_text(encoding="utf-8"))
    state = json.loads((root / "madsc_dogrulama/state.json").read_text(encoding="utf-8"))["channels"]
    manifest = json.loads((root / "final_validation_manifest.json").read_text(encoding="utf-8"))
    lookup = {}
    for item in manifest["candidates"]:
        url = item.get("url", "")
        if url:
            lookup[hashlib.sha256(url.encode()).hexdigest()[:20]] = item
    for record in state.values():
        url = record.get("url", "")
        if url and len(record.get("checks", [])) == 3 and all(c.get("passed") is True for c in record["checks"]):
            lookup.setdefault(hashlib.sha256(url.encode()).hexdigest()[:20], {
                "url": url, "label": record.get("channel", ""), "source_id": record.get("source_id", ""),
                "source_language_hint": record.get("source_language_hint", "")})
    existing = set()
    main = root / "CALISANLAR.m3u"
    if main.exists():
        existing = {line.strip() for line in main.read_text(encoding="utf-8").splitlines()
                    if line.strip().startswith(("http://", "https://"))}
    lines = ["#EXTM3U"]
    evidence = []
    seen = set()
    for item in results:
        if not isinstance(item, dict) or item.get("status") not in PASS:
            continue
        token = item.get("candidate_id")
        source = lookup.get(token)
        if not source:
            continue
        url = source["url"].strip()
        checks = next((rec.get("checks", []) for rec in state.values() if rec.get("url") == url), [])
        if len(checks) != 3 or not all(c.get("passed") is True for c in checks):
            continue
        if url in seen or url in existing or not url.startswith(("https://", "http://")):
            continue
        seen.add(url)
        name = str(item.get("label") or source.get("label") or "Adsiz aday").replace("\n", " ").replace("\r", " ").replace(",", " ")
        name = name.replace('"', "'")
        lines.extend([f'#EXTINF:-1 group-title="📦 YEDEKLER - IBO TEST",'+name, url])
        evidence.append({"channel": name, "candidate_id": token, "status": item["status"],
                         "three_pass": True, "ibo_device_tested": False})
        if len(evidence) >= limit:
            break
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines)+"\n", encoding="utf-8")
    output.with_suffix(".json").write_text(json.dumps({"count": len(evidence), "items": evidence,
        "note": "Isolated IBO test only; no production playlist or backups changed."},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"IBO trial candidates: {len(evidence)}")
    return len(evidence)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="madsc_merkezi_denetim/IBO-IKI-ASAMA-TEST.m3u")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    export(args.root, args.output, args.limit)
