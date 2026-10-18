#!/usr/bin/env python3
"""Read-only migration readiness report; never approves or performs cutover."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = (
    "madsc-01-guvenlik.yml", "madsc-02-kesif.yml",
    "madsc-03-kanal-test.yml", "madsc-04-arsiv-yedek.yml",
    "madsc-05-genel-bakim.yml",
)
REQUIRED = (
    "26_RULE_RUNTIME_ENFORCEMENT",
    "PROTECTED_FILE_DIFFERENCES_RECONCILED",
    "92_LEGACY_BEHAVIOR_PARITY",
    "CURRENT_SHA_FIVE_CATEGORY_CI",
    "NO_DUPLICATE_PRODUCTION_WRITERS",
    "EPG_PAGES_END_TO_END",
    "INDEPENDENT_OFFSITE_RESTORE",
    "IBO_DEVICE_ACCEPTANCE",
    "EXPLICIT_USER_CUTOVER_APPROVAL",
    "ROLLBACK_DRILL",
)

def inspect(root=ROOT):
    folder = Path(root) / ".github" / "workflows"
    present = {name: (folder / name).is_file() for name in CATEGORIES}
    raw = (folder / CATEGORIES[-1]).read_text(encoding="utf-8") if present[CATEGORIES[-1]] else ""
    order = [raw.find("uses: ./.github/workflows/" + name) for name in CATEGORIES[:-1]]
    orchestration = all(index >= 0 for index in order) and order == sorted(order)
    safe_permissions = all(
        "contents: read" in (folder / name).read_text(encoding="utf-8")
        and "contents: write" not in (folder / name).read_text(encoding="utf-8")
        for name, exists in present.items() if exists
    )
    checks = {
        "FIVE_WORKFLOW_FILES_PRESENT": all(present.values()),
        "CATEGORY_CALL_ORDER_PRESENT": orchestration,
        "SHADOW_WORKFLOWS_READ_ONLY": safe_permissions and all(present.values()),
    }
    # Neither a static check nor the existence of an artifact is runtime proof.
    blockers = list(REQUIRED)
    if not all(checks.values()):
        blockers.extend(k for k, ok in checks.items() if not ok)
    return {
        "schema_version": 1,
        "mode": "READ_ONLY_SHADOW",
        "migration_approved": False,
        "cutover_allowed": False,
        "legacy_workflows_retirement_allowed": False,
        "static_checks": checks,
        "category_files": present,
        "blockers": blockers,
        "next_action": "Collect per-SHA CI and 92-workflow behavioral parity evidence; obtain explicit approval before cutover.",
        "warning": "Static checks do not establish production readiness or authorize changes.",
    }

def main():
    report = inspect()
    output = ROOT / "madsc_merkezi_denetim" / "besli_sistem_gecis_hazirlik.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"static_checks": report["static_checks"], "blockers": report["blockers"],
                      "cutover_allowed": report["cutover_allowed"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
