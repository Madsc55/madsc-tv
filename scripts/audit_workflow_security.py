"""Read-only audit of GitHub Actions workflows.

Does not execute workflows, change permissions, or write protected playlists.
Run: python scripts/audit_workflow_security.py
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
TRIGGERS = ("push", "pull_request", "pull_request_target", "workflow_run",
            "workflow_dispatch", "schedule", "repository_dispatch", "workflow_call")
RISK = {
    "git_push": r"\bgit\s+(?:(?:-[A-Za-z]+|--[\w-]+(?:=[^\s]+)?|(?:-c|--config)\s+[^\s]+)\s+)*push\b",
    "git_commit": r"\bgit\s+(?:(?:-[A-Za-z]+|--[\w-]+(?:=[^\s]+)?|(?:-c|--config)\s+[^\s]+)\s+)*commit\b",
    "gh_api": r"\bgh\s+api\b",
    "curl_write": r"\bcurl\b[^\n]*(?:-X\s*(?:POST|PUT|PATCH|DELETE)|--request\s+(?:POST|PUT|PATCH|DELETE))",
    "protected_file_reference": r"\b(?:CALISANLAR\.m3u|CALISMAYANLAR\.txt|YENILER\.m3u|YABANCI_KANALLAR\.m3u)\b",
    "write_permissions": r"\b(?:contents|actions|pull-requests|workflows):\s*write\b",
    "write_all": r"\bpermissions:\s*write-all\b",
    "git_force_push": r"\bgit\s+(?:(?:-[A-Za-z]+|--[\w-]+(?:=[^\s]+)?|(?:-c|--config)\s+[^\s]+)\s+)*push\b[^\n]*(?:--force(?:-with-lease)?\b|\s-f(?:\s|$))",
    "github_token_env": r"\b(?:GH_TOKEN|GITHUB_TOKEN|PERSONAL_ACCESS_TOKEN)\b",
}
DANGEROUS = ("pull_request_target", "workflow_run")


def inspect_workflow(path):
    source = path.read_text(encoding="utf-8-sig")
    lines = source.splitlines()
    # Text-level inventory; not a YAML interpreter or a permission enforcement gate.
    trigger_lines = [i + 1 for i, line in enumerate(lines)
                     if re.match(r"^\s*(?:on:|['\"]on['\"]:|(?:- )?(?:" +
                                 "|".join(TRIGGERS) + r")\s*:)", line)]
    matches = {
        key: [i + 1 for i, line in enumerate(lines) if re.search(pattern, line, re.I)]
        for key, pattern in RISK.items()
    }
    permissions = [i + 1 for i, line in enumerate(lines)
                   if re.search(r"^\s*permissions\s*:", line)]
    return {
        "path": str(path.relative_to(ROOT)),
        "trigger_line_numbers": trigger_lines,
        "permissions_line_numbers": permissions,
        "risk_line_numbers": {k: v for k, v in matches.items() if v},
        "manual_review_required": bool(
            any(matches.values()) or not permissions or
            any(re.search(r"\b" + key + r"\s*:", source) for key in DANGEROUS)
        ),
    }


def audit():
    paths = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    records = [inspect_workflow(path) for path in paths]
    return {
        "workflow_count": len(records),
        "explicit_permissions_count": sum(bool(r["permissions_line_numbers"]) for r in records),
        "manual_review_count": sum(r["manual_review_required"] for r in records),
        "records": records,
        "limitations": "Static line-based signals; nested YAML, defaults, shell expansion and reusable actions require human review. No changes applied.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
