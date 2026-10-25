#!/usr/bin/env python3
"""K5: read-only legacy workflow behavioral parity gate.

A mapping of workflow names to five stages is not behavioral equivalence.
Compare an independently captured baseline with the current workflow inventory.
"""
import argparse
import json
from pathlib import Path

FIELDS = ("schedule_utc", "manual", "push", "workflow_run", "writes_contents", "has_concurrency", "concurrency_group")
# Optional independently captured step-level fingerprints and dispatch targets.
OPTIONAL_FIELDS = ("job_steps_sha256", "dispatch_targets", "job_dependencies", "workflow_content_sha256")

def compare(baseline, current):
    old = {w["file"]: w for w in baseline["workflows"]}
    new = {w["file"]: w for w in current["workflows"]}
    if len(old) != len(baseline["workflows"]) or len(new) != len(current["workflows"]):
        raise ValueError("Duplicate workflow file in inventory")
    missing = sorted(old.keys() - new.keys())
    added = sorted(new.keys() - old.keys())
    changes = []
    for name in sorted(old.keys() & new.keys()):
        differences = {field: {"before": old[name].get(field), "after": new[name].get(field)}
                       for field in FIELDS + tuple(field for field in OPTIONAL_FIELDS if field in old[name])
                       if old[name].get(field) != new[name].get(field)}
        if differences:
            changes.append({"file": name, "differences": differences})
    missing_evidence = sorted(name for name in old if name in new and
                              any(field not in old[name] or field not in new[name]
                                  for field in OPTIONAL_FIELDS))
    return {"status": "REVIEW_REQUIRED" if missing or changes or missing_evidence else "PASS",
            "baseline_count": len(old), "current_count": len(new),
            "missing_workflows": missing, "added_workflows": added,
            "changed_triggers_or_permissions": changes,
            "missing_step_level_evidence": missing_evidence,
            "behavioral_parity_verified": False,
            "limitations": "Static metadata comparison cannot prove step-level behavior, dispatch chains, runtime success, or 92 historical workflow equivalence."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("current", type=Path)
    args = parser.parse_args()
    report = compare(json.loads(args.baseline.read_text(encoding="utf-8")),
                     json.loads(args.current.read_text(encoding="utf-8")))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
