#!/usr/bin/env python3
"""Read-only consolidated acceptance gate. Never equates passing unit tests with production proof."""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
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
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", name, "-v"],
            cwd=ROOT, capture_output=True, text=True, timeout=240,
        )
        tests.append({"suite": name, "passed": result.returncode == 0,
                      "returncode": result.returncode,
                      "log_tail": (result.stdout + result.stderr)[-8000:]})
    runtime = subprocess.run([sys.executable, "-m", "unittest",
                              "test_five_category_runtime_integrity", "-v"],
                             cwd=ROOT, capture_output=True, text=True, timeout=240)
    tests.append({"suite": "test_five_category_runtime_integrity",
                  "passed": runtime.returncode == 0, "returncode": runtime.returncode,
                  "log_tail": (runtime.stdout + runtime.stderr)[-8000:]})
    rules = security_audit()
    workflows = inspect(ROOT)
    risks = risk_audit()
    if len(rules["rows"]) != 26 or workflows["total"] != 92:
        raise ValueError("Expected 26 rules and 92 legacy workflows")
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
        "legacy_workflow_count": workflows["total"],
        "legacy_behavior_verified": workflows["behavioral_parity_verified_count"],
        "legacy_behavior_blocked": workflows["migration_blocked_count"],
        "workflow_risk_count": risks["workflow_count"],
        "acceptance_complete": bool(
            all(row["passed"] for row in tests)
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
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "test_suites"}, ensure_ascii=False))
    if not all(row["passed"] for row in report["test_suites"]):
        return 1
    if args.require_full_acceptance and not report["acceptance_complete"]:
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
