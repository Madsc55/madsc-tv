"""Check backup category count without assuming a historical channel total."""
import re

def backup_metadata_consistent(entries):
    """Return evidence for backup entries, accepting zero entries without invented counts."""
    counts = []
    for item in entries:
        match = re.search(r'group-title="📦 YEDEKLER \((\d+)\)"', item.get("meta", ""))
        if not match:
            return {"ok": False, "declared_count": None, "actual_count": len(entries)}
        counts.append(int(match.group(1)))
    declared = counts[0] if counts else 0
    return {"ok": all(n == len(entries) for n in counts),
            "declared_count": declared, "actual_count": len(entries)}
