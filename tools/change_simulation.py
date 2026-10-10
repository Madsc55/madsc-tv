"""Development 18: read-only proposed playlist change simulation and rollback plan."""
import argparse
import hashlib
import json
from pathlib import Path

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def simulate(original, proposed):
    old = original.splitlines()
    new = proposed.splitlines()
    old_entries = [x for x in old if x.startswith("#EXTINF:")]
    new_entries = [x for x in new if x.startswith("#EXTINF:")]
    return {
        "applied": False,
        "changed": original != proposed,
        "original_sha256": digest(original),
        "proposed_sha256": digest(proposed),
        "original_channels": len(old_entries),
        "proposed_channels": len(new_entries),
        "channel_count_delta": len(new_entries) - len(old_entries),
        "rollback": {
            "method": "restore original file from a verified Git commit or saved backup",
            "original_sha256": digest(original),
            "verification": "sha256 of restored file must match original_sha256",
        },
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("original")
    p.add_argument("proposed")
    args = p.parse_args()
    old = Path(args.original).read_text(encoding="utf-8-sig")
    new = Path(args.proposed).read_text(encoding="utf-8-sig")
    print(json.dumps(simulate(old, new), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
