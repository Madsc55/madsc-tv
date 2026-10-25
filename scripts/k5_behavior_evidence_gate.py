#!/usr/bin/env python3
"""K5: fail-closed validation of per-workflow behavioral parity evidence."""
import csv
import json
import sys
import re
from urllib.parse import urlsplit
from pathlib import Path

REQUIRED = ("legacy_sha", "replacement_sha", "trigger_comparison", "input_output_comparison",
            "failure_comparison", "write_permission_comparison", "actions_run_url")
RUN_PREFIX = "https://github.com/Madsc55/madsc-tv/actions/runs/"


def validate(matrix, evidence):
    with open(matrix, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    names = [r["legacy_workflow"] for r in rows]
    errors = []
    if len(names) != 92 or len(set(names)) != 92:
        errors.append("Expected exactly 92 unique legacy workflows")
    unknown = set(evidence) - set(names)
    if unknown:
        errors.append("Unknown evidence entries: " + ", ".join(sorted(unknown)))
    accepted = []
    for row in rows:
        name = row["legacy_workflow"]
        record = evidence.get(name)
        if not isinstance(record, dict):
            if record is not None:
                errors.append(name + ": evidence entry must be an object")
            continue
        if any(not isinstance(record.get(key), str) or not record[key].strip() for key in REQUIRED):
            errors.append(name + ": incomplete behavior evidence")
            continue
        parsed = urlsplit(record["actions_run_url"])
        if (parsed.scheme != "https" or parsed.netloc != "github.com"
                or not re.fullmatch(r"/Madsc55/madsc-tv/actions/runs/[0-9]+", parsed.path)
                or parsed.query or parsed.fragment):
            errors.append(name + ": invalid Actions run URL")
            continue
        if (not re.fullmatch(r"[0-9a-fA-F]{40}", record["legacy_sha"])
                or not re.fullmatch(r"[0-9a-fA-F]{40}", record["replacement_sha"])):
            errors.append(name + ": invalid commit SHA")
            continue
        if record.get("decision") != "PASS":
            errors.append(name + ": evidence entry requires explicit PASS decision")
            continue
        if row["migration_decision"] != "BLOCKED_NEEDS_BEHAVIOR_EVIDENCE":
            errors.append(name + ": unexpected inventory decision")
            continue
        accepted.append(name)
    return {"inventory_total": len(names), "evidence_submitted": len(evidence),
            "evidence_complete_pass_count": len(accepted), "accepted_candidates": accepted,
            "errors": errors, "production_parity_verified": False,
            "note": "Evidence completeness is NOT independent verification of run contents or production behavior."}


def main():
    matrix = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("madsc_merkezi_denetim/92_workflow_esdegerlik_kabul_matrisi.csv")
    evidence_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("k5_workflow_behavior_evidence.json")
    evidence = json.loads(evidence_file.read_text(encoding="utf-8"))
    if not isinstance(evidence, dict):
        raise SystemExit("Evidence registry must be a JSON object")
    report = validate(matrix, evidence)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
