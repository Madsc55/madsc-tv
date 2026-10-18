#!/usr/bin/env python3
"""Read-only cross-category impact map; shared controls must cover all consumers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "K1": "madsc-01-guvenlik.yml",
    "K2": "madsc-02-kesif.yml",
    "K3": "madsc-03-kanal-test.yml",
    "K4": "madsc-04-arsiv-yedek.yml",
    "K5": "madsc-05-genel-bakim.yml",
}
# Shared controls are checked as a single unit; a missing consumer blocks preflight.
CONTROLS = {
    "protected_integrity": {"script": "scripts/k1_protected_integrity.py", "categories": list(CATEGORIES)},
    "category_evidence": {"script": "scripts/category_evidence_collect.py", "categories": ["K5"]},
    "migration_readiness": {"script": "scripts/five_system_cutover_readiness.py", "categories": ["K5"]},
}

def inspect(root=ROOT):
    folder = Path(root) / ".github" / "workflows"
    rows = {}
    missing = []
    for control, spec in CONTROLS.items():
        consumers = {}
        for category in spec["categories"]:
            path = folder / CATEGORIES[category]
            present = path.is_file() and spec["script"] in path.read_text(encoding="utf-8")
            consumers[category] = present
            if not present:
                missing.append({"control": control, "category": category, "workflow": CATEGORIES[category]})
        rows[control] = {"script": spec["script"], "consumers": consumers, "all_consumers_present": all(consumers.values())}
    return {"status": "STATIC_READY" if not missing else "BLOCKED",
            "shared_controls": rows, "missing_consumers": missing,
            "note": "Static references only; does not certify runtime enforcement or 92-workflow parity."}

def main():
    result = inspect()
    target = ROOT / "madsc_merkezi_denetim" / "besli_ortak_kural_etki_haritasi.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "missing_consumers": result["missing_consumers"]}, ensure_ascii=False))
    if result["missing_consumers"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
