"""Development 17: read-only candidate status dashboard."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

STATES = ("new", "verified", "quarantine", "broken", "identity_pending")
ALIASES = {
    "yeni": "new", "aday": "new", "new": "new",
    "dogrulandi": "verified", "verified": "verified", "working": "verified",
    "karantina": "quarantine", "quarantine": "quarantine",
    "bozuk": "broken", "broken": "broken", "failed": "broken",
    "kimlik_bekliyor": "identity_pending", "identity_pending": "identity_pending",
}

def summarize(rows):
    counts = Counter()
    unknown = 0
    for row in rows:
        raw = str(row.get("status", "")).strip().lower()
        state = ALIASES.get(raw)
        if state:
            counts[state] += 1
        else:
            unknown += 1
    return {"total": sum(counts.values()) + unknown,
            "new": counts["new"], "verified": counts["verified"],
            "quarantine": counts["quarantine"], "broken": counts["broken"],
            "identity_pending": counts["identity_pending"], "unknown": unknown}

def load(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data["candidates"]
        if not isinstance(data, list):
            raise ValueError("Expected candidate list")
        return data
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))
    raise ValueError("Input must be CSV or JSON")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Candidate CSV or JSON containing a status field")
    args = parser.parse_args()
    print(json.dumps(summarize(load(args.input)), ensure_ascii=False, indent=2))
