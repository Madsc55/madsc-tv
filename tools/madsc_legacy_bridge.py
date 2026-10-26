#!/usr/bin/env python3
"""Read-only, deterministic bridge for legacy GitHub Actions workflows.

No synthetic workflows are generated: unknown behavior stays explicitly unmapped.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
STAGES = {
    "K1": ("kesif", "discovery", "source", "tarama"),
    "K2": ("dogrula", "verification", "candidate", "uc-asama"),
    "K3": ("son-kontrol", "continuity", "final"),
    "K4": ("epg", "logo", "image"),
    "K5": ("backup", "yedek", "audit", "rapor", "report"),
}
PROTECTED = ("CALISANLAR.m3u", "YENILER.m3u")


def discover():
    result = []
    for path in sorted(WORKFLOWS.glob("*")):
        if path.suffix not in (".yml", ".yaml"):
            continue
        source = path.read_text(encoding="utf-8", errors="replace")
        name = path.stem.lower()
        stages = [stage for stage, terms in STAGES.items()
                  if any(term in name for term in terms)]
        result.append({
            "file": path.name,
            "stages": stages or ["UNMAPPED"],
            "manual": bool(re.search(r"(?m)^\s*workflow_dispatch\s*:", source)),
            "scheduled": bool(re.search(r"(?m)^\s*schedule\s*:", source)),
            "source_preserved": True,
        })
    return result


def build_stage_index(entries):
    """Build a standard five-stage routing manifest without modifying legacy code."""
    stages = {stage: [] for stage in STAGES}
    unmapped = []
    for entry in entries:
        mapped = [stage for stage in entry["stages"] if stage in stages]
        if not mapped:
            unmapped.append(entry["file"])
            continue
        for stage in mapped:
            stages[stage].append(entry["file"])
    return {
        "stages": stages,
        "unmapped": unmapped,
        "coverage": {
            "indexed": len(entries),
            "classified": len(entries) - len(unmapped),
            "target": 92,
            "behavior_equivalence_verified": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="madsc_legacy_bridge.json")
    args = parser.parse_args()
    entries = discover()
    stage_index = build_stage_index(entries)
    report = {
        "stage_index": stage_index,
        "legacy_target": 92,
        "observed_workflow_files": len(entries),
        "equivalence_claimed": False,
        "protected_files_unchanged": list(PROTECTED),
        "entries": entries,
        "unmapped": [e["file"] for e in entries if e["stages"] == ["UNMAPPED"]],
        "warning": "Name-based routing is informational, not a replacement for legacy behavior.",
    }
    destination = pathlib.Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(entries)} workflow files; unmapped: {len(report['unmapped'])}")


if __name__ == "__main__":
    main()
