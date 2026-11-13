#!/usr/bin/env python3
"""Read-only validator for timestamped K3 video/audio probes; not continuous playback proof."""
import argparse
import datetime as dt
import json
from collections import defaultdict

def validate(records, target=75, hours=6, max_gap=300):
    grouped = defaultdict(list)
    for record in records:
        ident = record.get("channel_id")
        if not isinstance(ident, str) or not ident.strip() or len(ident) > 128:
            raise ValueError("Invalid channel_id")
        if type(record.get("video_ok")) is not bool or type(record.get("audio_ok")) is not bool:
            raise ValueError("Probe flags must be booleans")
        stamp = dt.datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Timezone-aware timestamp required")
        grouped[ident].append((stamp.astimezone(dt.timezone.utc), record["video_ok"] and record["audio_ok"]))
    passed = 0
    for values in grouped.values():
        values.sort()
        if len(values) < 2 or not all(ok for _, ok in values):
            continue
        if len({stamp for stamp, _ in values}) != len(values):
            continue
        if (values[-1][0] - values[0][0]).total_seconds() < hours * 3600:
            continue
        if any((b[0] - a[0]).total_seconds() > max_gap for a, b in zip(values, values[1:])):
            continue
        passed += 1
    return {"hedef_kanal": target, "hedef_saat": hours,
            "maksimum_aralik_saniye": max_gap, "kanitli_tekil_kanal": passed,
            "eksik_kanal": max(0, target - passed),
            "periyodik_probe_kabulu": "EVET" if passed >= target else "BEKLIYOR",
            "kesintisiz_oynatma_kaniti": "YOK", "ibo_epg_onayi": "BEKLIYOR",
            "aciklama": "Periyodik ornekler kesintisiz oynatma veya cihaz dogrulamasi kaniti degildir."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", help="JSONL: channel_id, timestamp, video_ok, audio_ok")
    parser.add_argument("--output")
    args = parser.parse_args()
    with open(args.evidence, encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    result = validate(rows)
    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as out:
            out.write(serialized + "\n")
    print(serialized)
    return 0 if result["periyodik_probe_kabulu"] == "EVET" else 1

if __name__ == "__main__":
    raise SystemExit(main())
