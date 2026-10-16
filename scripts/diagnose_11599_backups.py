"""Read-only investigation of the 11599-vs-current backup discrepancy.

Never runs restore_all_11599_backups.main(), never writes playlists.
"""
import json
from collections import Counter
from pathlib import Path
from scripts.restore_all_11599_backups import P, SNAP, entries, key

EXPECTED = 11599


def inspect():
    original = list(entries(P.read_text(encoding="utf-8-sig").splitlines()))
    archived = list(entries(SNAP.read_text(encoding="utf-8-sig").splitlines()))
    backups = [(m, u) for m, u in original if 'group-title="📦 YEDEKLER' in m]
    known = {key(u) for _, u in original}
    skipped = Counter()
    candidates = []
    for m, u in archived:
        normalized = key(u)
        if normalized in known:
            skipped["already_present_or_duplicate"] += 1
            continue
        known.add(normalized)
        candidates.append((m, u))
    total = len(backups) + len(candidates)
    return {
        "expected": EXPECTED,
        "actual": total,
        "difference": EXPECTED - total,
        "existing_backup_entries": len(backups),
        "archive_entries": len(archived),
        "unique_restorable_entries": len(candidates),
        "skipped_archive_entries": dict(skipped),
        "status": "MISMATCH_READ_ONLY" if total != EXPECTED else "COUNT_MATCH_READ_ONLY",
        "note": "No files modified. Counts do not establish whether missing entries ever existed.",
    }


if __name__ == "__main__":
    print(json.dumps(inspect(), ensure_ascii=False, indent=2))
