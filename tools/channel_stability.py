#!/usr/bin/env python3
"""Read-only 7/30 day IPTV test stability report from JSONL test history."""
import argparse
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

UTC = dt.timezone.utc

def parse_time(value):
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(UTC)

def report(events, now=None):
    now = now or dt.datetime.now(UTC)
    groups = defaultdict(list)
    for event in events:
        name = event.get("channel") or event.get("channel_id")
        if not name:
            continue
        when = parse_time(event["timestamp"])
        if when > now:
            continue
        status = event.get("success")
        if type(status) is not bool:
            raise ValueError("success must be a boolean")
        groups[str(name)].append((when, status))
    output = []
    for name, checks in sorted(groups.items()):
        row = {"channel": name}
        successes = [when for when, success in checks if success]
        row["last_success"] = max(successes).isoformat() if successes else None
        for days in (7, 30):
            start = now - dt.timedelta(days=days)
            selected = [success for when, success in checks if start <= when <= now]
            count = len(selected)
            row[f"days_{days}"] = {
                "tests": count, "passed": sum(selected),
                "success_rate_percent": round(100 * sum(selected) / count, 2) if count else None
            }
        output.append(row)
    return {"generated_at": now.isoformat(), "channels": output}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("history", type=Path, help="JSONL rows: channel, timestamp, success")
    parser.add_argument("--output", type=Path, default=Path("stability-report.json"))
    args = parser.parse_args()
    events = [json.loads(line) for line in args.history.read_text(encoding="utf-8").splitlines() if line.strip()]
    args.output.write_text(json.dumps(report(events), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
