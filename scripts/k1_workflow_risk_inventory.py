"""Read-only K1 workflow risk inventory, never executes workflows or edits files."""
from collections import Counter
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / ".github" / "workflows"
PROTECTED = re.compile(r"(?:CALISANLAR\.m3u|CALISMAYANLAR\.txt|YENILER\.m3u|YABANCI_KANALLAR\.m3u|HEPSI|FAVORILER|YEDEKLER/|EPG/|epg\.xml|logolar/|arsiv/)", re.I)
WRITE = re.compile(r"(?:\bgit\s+push\b|curl[^\n]*(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE))", re.I)
GH_API = re.compile(r"\bgh\s+api\b[^\n]*", re.I)
GH_CLI_MUTATION = re.compile(r"\bgh\s+(?:workflow\s+(?:run|enable|disable)|run\s+rerun|release\s+(?:create|delete|edit|upload)|repo\s+(?:create|delete|edit)|pr\s+(?:merge|create|close)|issue\s+(?:create|close|edit))\b", re.I)
GIT_MUTATION = re.compile(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+)*(?:push|reset\s+--hard|clean\s+-(?=[A-Za-z]*f)[A-Za-z]+|checkout\s+--|restore\b)\b", re.I)
PYTHON_MUTATION = re.compile(r"\b(?:python3?|bash|sh)\s+(?:\S+/)*\S*(?:publish|upload|update|write|sync|deploy|delete|restore)\S*\.(?:py|sh)\b", re.I)
# Only the existing monthly audit\u0027s known GET-only Actions report calls are exempt.
READ_ONLY_ACTIONS_API = re.compile(r"\brepos/\$\{GITHUB_REPOSITORY\}/actions/(?:runs|workflows)(?:\?[^\s\"]*)?", re.I)
GH_API_MUTATION_FLAGS = re.compile(r"(?<!\w)(?:-X|--method|-f|-F|--field|--raw-field|--input)(?:\s|=|$)", re.I)
PERMISSION = re.compile(r"(?:contents|actions|pull-requests|workflows):\s*write\b|permissions:\s*write-all", re.I)
TRIGGER = re.compile(r"^\s*(push|pull_request|pull_request_target|workflow_run|schedule|workflow_dispatch|repository_dispatch):", re.M)
GATE = "tools/protected_write_gate.py"

def inspect(path):
    s = path.read_text(encoding="utf-8-sig")
    triggers = sorted(set(TRIGGER.findall(s)))
    pushes = len(re.findall(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+|(?:-[A-Za-z]+|--[\w-]+(?:=\S+)?)\s+)*push\b", s))
    gates = s.count(GATE)
    force_pushes = len(re.findall(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+|(?:-[A-Za-z]+|--[\w-]+(?:=\S+)?)\s+)*push\b[^\n]*(?:--force(?:-with-lease)?\b|\s-f(?:\s|$))", s))
    api_calls = GH_API.findall(s)
    api_write = any(
        not READ_ONLY_ACTIONS_API.search(call)
        or bool(GH_API_MUTATION_FLAGS.search(call))
        or "graphql" in call.casefold()
        for call in api_calls
    )
    has_write = (bool(WRITE.search(s)) or api_write or bool(GH_CLI_MUTATION.search(s))
                 or bool(GIT_MUTATION.search(s)) or bool(PYTHON_MUTATION.search(s)))
    # A gate reference alone does not prove it runs before an indirect writer.
    indirect_write = bool(PYTHON_MUTATION.search(s) or GH_CLI_MUTATION.search(s) or api_write)
    # Conservative source-order evidence: a later gate never protects an earlier push.
    # This remains a static signal, not proof of runtime execution or authorization.
    lines = s.splitlines()
    push_line_numbers = [i for i, line in enumerate(lines)
                         if re.search(r"\\bgit\\s+(?:(?:-c|--config)\\s+\\S+\\s+|(?:-[A-Za-z]+|--[\\w-]+(?:=\\S+)?)\\s+)*push\\b", line)]
    gate_line_numbers = [i for i, line in enumerate(lines)
                         if re.search(r"\\bpython3?\\s+tools/protected_write_gate\\.py\\b", line)]
    pushes_without_prior_gate = sum(not any(g < p for g in gate_line_numbers)
                                    for p in push_line_numbers)
    has_permission = bool(PERMISSION.search(s))
    protected = bool(PROTECTED.search(s))
    risky_triggers = any(x in triggers for x in ("pull_request_target", "workflow_run"))
    if pushes and path.name in {"test-32-unapproved-write-regression.yml", "test-38-audit-selftest.yml", "toplu-sistem-kontrol.yml"} and "persist-credentials: false" in s and re.search(r"(?m)^  contents: read\s*$", s):
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
        "force_push_count": force_pushes,
        "multiple_push_signal": pushes > 1,
        "gate_reference_count": gates,
        "write_command_signal": has_write,
        "indirect_write_signal": indirect_write,
        "indirect_write_without_gate_reference": indirect_write and gates == 0,
        "runtime_gate_order_verified": False,
        "pushes_without_prior_gate_signal": pushes_without_prior_gate,
        "push_gate_order_static_signal_only": True,
        "risky_trigger": risky_triggers,
    }

def audit():
    paths = sorted([*DIRECTORY.glob("*.yml"), *DIRECTORY.glob("*.yaml")])
    records = [inspect(p) for p in paths]
    return {
        "workflow_count": len(records),
        "tiers": dict(Counter(r["tier"] for r in records)),
        "missing_explicit_permissions": sum(not r["explicit_permissions"] for r in records),
        "missing_permission_paths": [r["path"] for r in records if not r["explicit_permissions"]],
        "push_commands": sum(r["git_push_count"] for r in records),
        "force_push_commands": sum(r["force_push_count"] for r in records),
        "workflows_with_multiple_push_signals": [r["path"] for r in records if r["multiple_push_signal"]],
        "gate_references": sum(r["gate_reference_count"] for r in records),
        "indirect_writers_without_gate_reference": [r["path"] for r in records if r["indirect_write_without_gate_reference"]],
        "runtime_gate_order_verified_workflows": 0,
        "pushes_without_prior_gate_signal": sum(r["pushes_without_prior_gate_signal"] for r in records),
        "push_order_review_paths": [r["path"] for r in records if r["pushes_without_prior_gate_signal"]],
        "records": records,
        "limitations": "Static signals only: YAML context, scripts, action side effects, branch rules and runtime enforcement need separate verification.",
    }

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
