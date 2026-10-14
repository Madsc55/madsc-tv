"""Read-only inventory for newly discovered channels with missing artwork."""
import json
from collections import Counter, defaultdict
from pathlib import Path

def build(candidates, prepared):
    prepared_by_hash = {str(row.get("stream_sha256", "")): row for row in prepared if isinstance(row, dict)}
    source_by_name = defaultdict(set)
    for c in candidates:
        if not isinstance(c, dict):
            continue
        name = " ".join(str(c.get("channel", "")).casefold().split())
        url = str(c.get("logo_url", "")).strip()
        if name and url and not c.get("logo_source_review_required"):
            source_by_name[name].add(url)
    rows = []
    for c in candidates:
        if not isinstance(c, dict):
            continue
        key = str(c.get("stream_sha256", ""))
        name = str(c.get("channel", ""))
        row = prepared_by_hash.get(key, {})
        status = str(row.get("status", "NOT_PREPARED"))
        source = str(c.get("logo_url", "")).strip()
        if not source:
            category = "LOGO_KAYNAGI_YOK"
        elif c.get("logo_source_review_required"):
            category = "LOGO_KAYNAGI_GUVENLIK_INCELEMESI"
        elif status == "PNG_READY_REVIEW_PENDING":
            category = "PNG_HAZIR_KIMLIK_ONAYI_BEKLIYOR"
        elif status in ("SOURCE_LOGO_FAILED", "PNG_FILE_UNAVAILABLE"):
            category = "LOGO_INDIRME_VEYA_DONUSUM_HATASI"
        else:
            category = "PNG_HAZIRLIGI_BEKLIYOR"
        same_name = source_by_name.get(" ".join(name.casefold().split()), set())
        suggestions = sorted(same_name - ({source} if source else set()))
        rows.append({"channel": name, "stream_sha256": key, "source": c.get("source", ""),
                     "category": category, "preparation_status": status,
                     "same_name_source_suggestions": suggestions,
                     "identity_verified": False, "playlist_approved": False})
    counts = Counter(row["category"] for row in rows)
    return {"total_candidates": len(rows), "category_counts": dict(sorted(counts.items())),
            "candidates": rows, "main_playlist_modified": False,
            "note": "Same-name logos are suggestions, not proven channel identity. No playlist writes."}

def main():
    folder = Path("madsc_kesif")
    source = folder / "logo_candidates.json"
    prepared = folder / "candidate_logos.json"
    try:
        candidates = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        candidates = []
    try:
        existing = json.loads(prepared.read_text(encoding="utf-8")).get("results", [])
    except (OSError, ValueError, AttributeError):
        existing = []
    report = build(candidates if isinstance(candidates, list) else [],
                   existing if isinstance(existing, list) else [])
    folder.mkdir(exist_ok=True)
    (folder / "candidate_logo_missing_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Yeni kanal adayları logo raporu:", report["total_candidates"], report["category_counts"])

if __name__ == "__main__":
    main()
