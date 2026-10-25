#!/usr/bin/env python3
"""Fail-closed K5 per-workflow evidence validator; no repository mutations."""
import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")
REQUIRED = ("legacy_workflow", "replacement_workflow", "source_sha",
            "run_id", "job_id", "artifact_id", "checks")

def validate(rows, legacy_names, replacement_candidates=None):
    if not isinstance(rows, list) or not isinstance(legacy_names, (list, set, tuple)):
        raise ValueError("Evidence and inventory must be collections")
    if any(not isinstance(name, str) for name in legacy_names):
        raise ValueError("Legacy workflow names must be strings")
    known = set(legacy_names)
    if len(legacy_names) != 92 or len(known) != 92 or any(not isinstance(name, str) or not name.endswith((".yml", ".yaml")) for name in known):
        raise ValueError("Expected exactly 92 unique legacy workflows")
    if replacement_candidates is not None and (not isinstance(replacement_candidates, dict) or set(replacement_candidates) != known):
        raise ValueError("Incomplete replacement mapping inventory")
    allowed_replacements = {f"madsc-0{n}-{suffix}.yml" for n, suffix in ((1, "guvenlik"), (2, "kesif"), (3, "kanal-test"), (4, "arsiv-yedek"), (5, "genel-bakim"))}
    if replacement_candidates is not None and any(
        not isinstance(candidates, list) or
        any(not isinstance(candidate, str) or candidate not in allowed_replacements for candidate in candidates) or
        len(candidates) != len(set(candidates))
        for candidates in replacement_candidates.values()
    ):
        raise ValueError("Malformed replacement mapping candidates")
    seen = set()
    approved = set()
    for row in rows:
        if not isinstance(row, dict) or any(key not in row for key in REQUIRED):
            raise ValueError("Incomplete evidence record")
        name = row["legacy_workflow"]
        if not isinstance(name, str) or name not in known or name in seen:
            raise ValueError("Unknown or duplicate legacy workflow")
        seen.add(name)
        if not isinstance(row["replacement_workflow"], str) or row["replacement_workflow"] not in allowed_replacements:
            raise ValueError("Missing five-system replacement")
        if replacement_candidates is not None and (not isinstance(replacement_candidates[name], list) or row["replacement_workflow"] not in replacement_candidates[name]):
            raise ValueError("Replacement is not a mapped candidate for legacy workflow")
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
    parser.add_argument("--require-production-ready", action="store_true",
                        help="Exit nonzero unless independent 92/92 verification exists")
    args = parser.parse_args()
    inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    if not isinstance(inventory, dict) or not isinstance(inventory.get("items"), list):
        raise ValueError("Inventory must contain items list")
    if any(not isinstance(item, dict) or not isinstance(item.get("file"), str) or
           not isinstance(item.get("possible_replacement_workflows"), list)
           for item in inventory["items"]):
        raise ValueError("Invalid inventory item")
    report = validate(evidence, [item["file"] for item in inventory["items"]],
                      {item["file"]: item["possible_replacement_workflows"] for item in inventory["items"]})
    # Every legacy workflow gets an actionable parity gap, not a blanket pass.
    by_name = {item["file"]: item for item in inventory["items"]}
    report["workflow_gaps"] = [
        {
            "legacy_workflow": name,
            "evidence_submitted": name not in report["missing_evidence"],
            "replacement_candidates": by_name[name]["possible_replacement_workflows"],
            "unmatched_script_entrypoints": by_name[name].get("unmatched_script_entrypoints", []),
            "unmatched_trigger_signals": by_name[name].get("unmatched_trigger_signals", []),
            "unmatched_cron_expressions": by_name[name].get("unmatched_cron_expressions", []),
            "migration_gap_reasons": by_name[name].get("migration_gap_reasons", []),
            "behavioral_parity_verified": False,
        }
        for name in sorted(by_name)
    ]
    report["unverified_evidence_workflows"] = sorted(row["legacy_workflow"] for row in report["workflow_gaps"] if row["evidence_submitted"])
    report["production_acceptance_blockers"] = [
        "NO_INDEPENDENT_BEHAVIOR_VERIFICATION",
        "NOT_ALL_92_WORKFLOWS_HAVE_ACCEPTED_EVIDENCE",
    ]
    report["unmapped_workflows"] = sorted(row["legacy_workflow"] for row in report["workflow_gaps"] if not row["replacement_candidates"])
    report["missing_script_workflows"] = sorted(row["legacy_workflow"] for row in report["workflow_gaps"] if row["unmatched_script_entrypoints"])
    report["unmatched_trigger_workflows"] = sorted(row["legacy_workflow"] for row in report["workflow_gaps"] if row["unmatched_trigger_signals"] or row["unmatched_cron_expressions"])
    report["gap_reason_counts"] = {
        reason: sum(reason in row["migration_gap_reasons"] for row in report["workflow_gaps"])
        for reason in sorted({reason for row in report["workflow_gaps"] for reason in row["migration_gap_reasons"]})
    }
    report["unmapped_workflow_count"] = sum(not row["replacement_candidates"] for row in report["workflow_gaps"])
    report["missing_script_workflow_count"] = sum(bool(row["unmatched_script_entrypoints"]) for row in report["workflow_gaps"])
    report["unmatched_trigger_workflow_count"] = sum(bool(row["unmatched_trigger_signals"] or row["unmatched_cron_expressions"]) for row in report["workflow_gaps"])
    output_path = Path(args.output)
    if output_path.is_dir():
        raise ValueError("Report output must be a file")
    if output_path.resolve() in {Path(args.inventory).resolve(), Path(args.evidence).resolve()}:
        raise ValueError("Report output must not overwrite inventory or evidence")
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "missing_evidence"}))
    if args.require_production_ready and not report["production_ready"]:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
