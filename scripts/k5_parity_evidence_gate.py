#!/usr/bin/env python3
"""Fail-closed K5 per-workflow evidence validator; no repository mutations."""
import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")
REQUIRED = ("legacy_workflow", "replacement_workflow", "source_sha",
            "run_id", "job_id", "artifact_id", "checks")

def validate(rows, legacy_names):
    if not isinstance(rows, list) or not isinstance(legacy_names, (list, set, tuple)):
        raise ValueError("Evidence and inventory must be collections")
    known = set(legacy_names)
    if len(legacy_names) != 92 or len(known) != 92:
        raise ValueError("Expected exactly 92 unique legacy workflows")
    seen = set()
    approved = set()
    for row in rows:
        if not isinstance(row, dict) or any(key not in row for key in REQUIRED):
            raise ValueError("Incomplete evidence record")
        name = row["legacy_workflow"]
        if not isinstance(name, str) or name not in known or name in seen:
            raise ValueError("Unknown or duplicate legacy workflow")
        seen.add(name)
        if row["replacement_workflow"] not in {f"madsc-0{n}-{suffix}.yml" for n, suffix in ((1, "guvenlik"), (2, "kesif"), (3, "kanal-test"), (4, "arsiv-yedek"), (5, "genel-bakim"))}:
            raise ValueError("Missing five-system replacement")
        if not isinstance(row["source_sha"], str) or not SHA.fullmatch(row["source_sha"]):
            raise ValueError("Invalid source commit SHA")
        if any(type(row[key]) is not int or row[key] <= 0 for key in ("run_id", "job_id", "artifact_id")):
            raise ValueError("Real run, job and artifact identifiers required")
        checks = row["checks"]
        required_checks = ("trigger", "outputs", "failure_behavior", "permissions",
                           "protected_paths", "regression")
        if not isinstance(checks, dict) or any(checks.get(key) is not True for key in required_checks):
            raise ValueError("Missing verified behavioral checks")
        # Caller must independently validate referenced GitHub records before using approval.
        approved.add(name)
    return {"inventory_total": 92, "evidence_records": len(seen),
            "candidate_evidence_count": len(approved),
            "independently_verified_count": 0,
            "production_ready": False,
            "missing_evidence": sorted(known - seen)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    report = validate(evidence, [item["file"] for item in inventory["items"]])
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "missing_evidence"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
