"""Read-only K1 workflow risk inventory, never executes workflows or edits files."""
from collections import Counter
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / ".github" / "workflows"
PROTECTED = re.compile(r"(?:CALISANLAR\.m3u|CALISMAYANLAR\.txt|YENILER\.m3u|YABANCI_KANALLAR\.m3u)", re.I)
WRITE = re.compile(r"(?:\bgit\s+push\b|\bgh\s+api\b|curl[^\n]*(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE))", re.I)
PERMISSION = re.compile(r"(?:contents|actions|pull-requests|workflows):\s*write\b|permissions:\s*write-all", re.I)
TRIGGER = re.compile(r"^\s*(push|pull_request|pull_request_target|workflow_run|schedule|workflow_dispatch|repository_dispatch):", re.M)
GATE = "tools/protected_write_gate.py"

def inspect(path):
    s = path.read_text(encoding="utf-8-sig")
    triggers = sorted(set(TRIGGER.findall(s)))
    pushes = len(re.findall(r"\bgit\s+push\b", s))
    gates = s.count(GATE)
    has_write = bool(WRITE.search(s))
    has_permission = bool(PERMISSION.search(s))
    protected = bool(PROTECTED.search(s))
    risky_triggers = any(x in triggers for x in ("pull_request_target", "workflow_run"))
    if pushes and not has_permission and "persist-credentials: false" in s and (path.name.startswith("test-") or not re.search(r"\bGH_TOKEN\b|\bGITHUB_TOKEN\b", s)):
        tier = "READ_ONLY_AUDIT_TEXT"
    elif pushes and gates < pushes:
        tier = "CRITICAL_UNGATED_PUSH"
    elif has_write and (protected or risky_triggers):
        tier = "HIGH_WRITE_OR_TRIGGER"
    elif has_write or has_permission:
        tier = "REVIEW_WRITE"
    else:
        tier = "LOW_STATIC_SIGNAL"
    return {
        "path": str(path.relative_to(ROOT)),
        "tier": tier,
        "triggers": triggers,
        "explicit_permissions": bool(re.search(r"^\s*permissions\s*:", s, re.M)),
        "write_permission_signal": has_permission,
        "protected_reference": protected,
        "git_push_count": pushes,
        "gate_reference_count": gates,
        "write_command_signal": has_write,
        "risky_trigger": risky_triggers,
    }

def audit():
    paths = sorted([*DIRECTORY.glob("*.yml"), *DIRECTORY.glob("*.yaml")])
    records = [inspect(p) for p in paths]
    return {
        "workflow_count": len(records),
        "tiers": dict(Counter(r["tier"] for r in records)),
        "missing_explicit_permissions": sum(not r["explicit_permissions"] for r in records),
        "push_commands": sum(r["git_push_count"] for r in records),
        "gate_references": sum(r["gate_reference_count"] for r in records),
        "records": records,
        "limitations": "Static signals only: YAML context, scripts, action side effects, branch rules and runtime enforcement need separate verification.",
    }

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
