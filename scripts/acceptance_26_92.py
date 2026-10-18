#!/usr/bin/env python3
"""Read-only consolidated acceptance gate. Never equates passing unit tests with production proof."""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    "test_*security_audit.py",
    "test_protected_write_gate.py",
    "test_protected_gate_integration.py",
    "test_k1_failure_gate.py",
    "test_k1_24_rule_evidence.py",
    "test_k1_workflow_risk_inventory.py",
    "test_k1_legacy_writer_guards.py",
    "test_k1_runtime_workflow_guard.py",
    "test_five_category_92_workflow_audit.py",
    "test_legacy_permission_gap.py",
    "test_five_system_cutover_readiness.py",
]

def execute():
    from scripts.k1_24_rule_evidence import audit as security_audit
    from scripts.five_category_92_workflow_audit import inspect
    from scripts.k1_workflow_risk_inventory import audit as risk_audit

    tests = []
    for name in SUITES:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", name, "-v"],
                cwd=ROOT, capture_output=True, text=True, timeout=240,
            )
            tests.append({"suite": name, "passed": result.returncode == 0 and bool(re.search(r"Ran [1-9][0-9]* tests? in ", result.stdout + result.stderr)),
                          "returncode": result.returncode,
                          "log_tail": (result.stdout + result.stderr)[-8000:]})
        except (subprocess.TimeoutExpired, OSError) as exc:
            tests.append({"suite": name, "passed": False, "returncode": None,
                          "log_tail": str(exc)})
    try:
        runtime = subprocess.run([sys.executable, "-m", "unittest", "discover",
                                  "-s", ".", "-p", "test_five_category_runtime_integrity.py", "-v"],
                                 cwd=ROOT, capture_output=True, text=True, timeout=240)
        tests.append({"suite": "test_five_category_runtime_integrity",
                      "passed": runtime.returncode == 0 and bool(re.search(r"Ran [1-9][0-9]* tests? in ", runtime.stdout + runtime.stderr)),
                      "returncode": runtime.returncode,
                      "log_tail": (runtime.stdout + runtime.stderr)[-8000:]})
    except (subprocess.TimeoutExpired, OSError) as exc:
        tests.append({"suite": "test_five_category_runtime_integrity",
                      "passed": False, "returncode": None, "log_tail": str(exc)})
    audit_errors = []
    rules = None
    workflows = None
    risks = None
    for label, fn in (("security", security_audit), ("workflows", lambda: inspect(ROOT)),
                      ("risks", risk_audit)):
        try:
            result = fn()
            if label == "security":
                rules = result
            elif label == "workflows":
                workflows = result
            else:
                risks = result
        except (Exception, SystemExit) as exc:
            audit_errors.append({"audit": label, "error": str(exc)})
    if audit_errors:
        return {"generated_utc": datetime.now(timezone.utc).isoformat(),
                "git_sha": os.environ.get("GITHUB_SHA"),
                "github_run_id": os.environ.get("GITHUB_RUN_ID"),
                "test_suites": tests,
                "audit_errors": audit_errors,
                "regression_suites_passed": sum(row["passed"] for row in tests),
                "regression_suites_total": len(tests),
                "static_security_clean": False, "acceptance_complete": False,
                "security_runtime_verified": 0, "legacy_behavior_verified": 0}
    if len(rules["rows"]) != 26 or workflows["total"] != 92:
        audit_errors.append({"audit": "inventory", "error": "Expected 26 rules and 92 legacy workflows"})
        return {"generated_utc": datetime.now(timezone.utc).isoformat(),
                "git_sha": os.environ.get("GITHUB_SHA"),
                "github_run_id": os.environ.get("GITHUB_RUN_ID"),
                "test_suites": tests, "audit_errors": audit_errors,
                "regression_suites_passed": sum(row["passed"] for row in tests),
                "regression_suites_total": len(tests),
                "static_security_clean": False, "acceptance_complete": False,
                "security_runtime_verified": 0, "legacy_behavior_verified": 0}
    critical_risks = risks["tiers"].get("CRITICAL_UNGATED_PUSH", 0)
    missing_permissions = risks["missing_explicit_permissions"]
    static_security_clean = critical_risks == 0 and missing_permissions == 0
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "git_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "test_suites": tests,
        "regression_suites_passed": sum(row["passed"] for row in tests),
        "regression_suites_total": len(tests),
        "security_rule_count": 26,
        "security_runtime_verified": rules["fully_verified_rules"],
        "security_runtime_unverified": rules["runtime_unverified_rule_numbers"],
        "security_rule_evidence": rules["rows"],
        "legacy_workflow_count": workflows["total"],
        "legacy_behavior_verified": workflows["behavioral_parity_verified_count"],
        "legacy_behavior_blocked": workflows["migration_blocked_count"],
        "legacy_workflow_evidence": [{"file": item["file"],
                                     "category": item["primary_category"],
                                     "candidate_replacements": item["possible_replacement_workflows"],
                                     "missing_script_entrypoints": item["unmatched_script_entrypoints"],
                                     "missing_legacy_script_files": item["missing_legacy_script_files"],
                                     "gaps": item["migration_gap_reasons"]}
                                    for item in workflows["items"]],
        "workflow_risk_count": risks["workflow_count"],
        "critical_ungated_push_count": critical_risks,
        "missing_explicit_permission_count": missing_permissions,
        "static_security_clean": static_security_clean,
        "acceptance_complete": bool(
            all(row["passed"] for row in tests)
            and static_security_clean
            and rules["runtime_acceptance_allowed"]
            and workflows["behavioral_parity_verified_count"] == 92
        ),
        "warning": "Unit/integration test success is NOT production, device, or behavioral parity proof.",
    }
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="acceptance-26-92.json")
    parser.add_argument("--require-full-acceptance", action="store_true")
    args = parser.parse_args()
    report = execute()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "test_suites"}, ensure_ascii=False))
    for suite in report["test_suites"]:
        if not suite["passed"]:
            print("::error title=Toplu test hatasi::{} failed; see acceptance artifact".format(suite["suite"]))
    for issue in report.get("audit_errors", []):
        print("::error title=Envanter denetimi::{}: {}".format(issue["audit"], issue["error"]))
    if not all(row["passed"] for row in report["test_suites"]) or report.get("audit_errors"):
        return 1
    if args.require_full_acceptance and not report["acceptance_complete"]:
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
