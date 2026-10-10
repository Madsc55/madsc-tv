"""13. gelistirme: salt okunur kaynak degisiklik raporu."""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def parse_m3u(path):
    result = {}
    meta = None
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            meta = line
        elif line and not line.startswith("#") and meta is not None:
            key = hashlib.sha256(meta.encode("utf-8")).hexdigest()[:16]
            result.setdefault(key, []).append(line)
            meta = None
    return result

def compare(before, after):
    old, new = parse_m3u(before), parse_m3u(after)
    changes = []
    for key in sorted(set(old) | set(new)):
        a, b = old.get(key, []), new.get(key, [])
        if a != b:
            changes.append({"identity": key, "old_urls": a, "new_urls": b,
                            "type": "added" if not a else "removed" if not b else "changed"})
    return changes

def main():
    p = argparse.ArgumentParser()
    p.add_argument("before")
    p.add_argument("after")
    p.add_argument("--output", default="kaynak_degisiklik_raporu.json")
    args = p.parse_args()
    changes = compare(args.before, args.after)
    report = {"generated_at": datetime.now(timezone.utc).isoformat(),
              "before": args.before, "after": args.after, "changes": changes,
              "rollback_note": "Rapor bilgilendirme amaclidir; otomatik geri alma yapilmaz."}
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Degisiklik sayisi: {len(changes)}")

if __name__ == "__main__":
    main()
