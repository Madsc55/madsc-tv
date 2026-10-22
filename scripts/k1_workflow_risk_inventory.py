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
FAILURE_GATE_CALL = re.compile(
    r"(?m)^\s*(?:-\s*)?(?:run:\s*)?python3?\s+tools/workflow_failure_gate\.py(?:\s|$)"
)


def job_scope(source):
    """Conservative context for the repository's block-style jobs/steps.

    This is source evidence, not YAML/shell execution. Never grants clearance.
    Only command-shaped lines in run blocks count; embedded code still needs review.
    """
    jobs = []
    job = step = None
    run_indent = None
    in_jobs = False
    command = re.compile(r"(?:^|[;&|()])\s*(?:git\s+(?:(?:-c|--config)\s+\S+\s+)*push\b|gh\s+(?:workflow\s+(?:run|enable|disable)|run\s+rerun|api\b)|curl\b[^\n]*(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE))")
    for number, line in enumerate(source.splitlines(), 1):
        if re.match(r"^jobs:\s*(?:#.*)?$", line):
            in_jobs = True
            continue
        if re.match(r"^\S", line) and not line.startswith("#"):
            in_jobs = False
            job = step = None
        if not in_jobs:
            continue
        job_match = re.match(r"^  ([\w-]+):\s*$", line)
        if job_match:
            job = {"job": job_match[1], "line": number, "condition_signal": None, "steps": []}
            jobs.append(job)
            step = None
            run_indent = None
            continue
        if job is None:
            continue
        condition = re.match(r"^    if:\s*(.*)$", line)
        if condition:
            job["condition_signal"] = condition[1]
        reusable = re.match(r"^    uses:\s*(.*)$", line)
        if reusable:
            job["reusable_workflow_signal"] = reusable[1]
        step_match = re.match(r"^      - (name|uses|run):\s*(.*)$", line)
        if step_match:
            step = {"line": number, "name": step_match[2] if step_match[1] == "name" else "(unnamed)",
                    "failure_gate_call_lines": [], "mutation_signal_lines": [],
                    "script_mutation_name_lines": [], "continue_on_error_signal": False}
            job["steps"].append(step)
            run_indent = None
        if step is None:
            continue
        if re.match(r"^        continue-on-error:\s*true\s*(?:#.*)?$", line):
            step["continue_on_error_signal"] = True
        run_match = re.match(r"^(?:      - |        )run:\s*(.*)$", line)
        if run_match:
            body = run_match[1]
            run_indent = 8 if re.fullmatch(r"[|>][-+]?\s*(?:#.*)?", body) else None
            if run_indent is not None:
                continue
        elif run_indent is not None and (not line.strip() or len(line) - len(line.lstrip()) > run_indent):
            body = line.strip()
        else:
            run_indent = None
            continue
        if body.startswith("#"):
            continue
        if re.match(r"^python3?\s+tools/workflow_failure_gate\.py(?:\s|$)", body):
            step["failure_gate_call_lines"].append(number)
        readonly_api = (GH_API.search(body) and READ_ONLY_ACTIONS_API.search(body)
                        and not GH_API_MUTATION_FLAGS.search(body) and "graphql" not in body.casefold()
                        and not GIT_MUTATION.search(body) and not GH_CLI_MUTATION.search(body)
                        and not WRITE.search(body))
        if command.search(body) and not readonly_api:
            step["mutation_signal_lines"].append(number)
        if PYTHON_MUTATION.match(body):
            step["script_mutation_name_lines"].append(number)
    for job in jobs:
        gates = [line for step in job["steps"] if not step["continue_on_error_signal"]
                 for line in step["failure_gate_call_lines"]]
        mutations = [line for step in job["steps"]
                     for line in step["mutation_signal_lines"] + step["script_mutation_name_lines"]]
        job["mutation_lines_without_prior_failure_gate_signal"] = [line for line in mutations
                                                                   if not any(gate < line for gate in gates)]
        job["runtime_verified"] = False
    return jobs

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
                         if re.search(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+|(?:-[A-Za-z]+|--[\w-]+(?:=\S+)?)\s+)*push\b", line)]
    gate_line_numbers = [i for i, line in enumerate(lines)
                         if re.search(r"\bpython3?\s+tools/protected_write_gate\.py\b", line)]
    # Same-line shell chains are common: count a gate before push on that
    # line as an ordering signal, but never as runtime authorization proof.
    # A later gate on the same line cannot protect an earlier push.
    gate_pattern = re.compile(r"\bpython3?\s+tools/protected_write_gate\.py\b")
    push_pattern = re.compile(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+|(?:-[A-Za-z]+|--[\w-]+(?:=\S+)?)\s+)*push\b")
    pushes_without_prior_gate = 0
    for i, line in enumerate(lines):
        for match in push_pattern.finditer(line):
            prior_line_gate = any(g < i for g in gate_line_numbers)
            same_line_gate = any(g.start() < match.start() for g in gate_pattern.finditer(line))
            if not (prior_line_gate or same_line_gate):
                pushes_without_prior_gate += 1
    # An audit-text exemption is not a security exemption: flag any executable
    # push text in the same file for manual review, even with read-only tokens.
    read_only_audit_exemption = (pushes > 0 and path.name in {
        "test-32-unapproved-write-regression.yml",
        "test-38-audit-selftest.yml",
        "toplu-sistem-kontrol.yml",
    } and "persist-credentials: false" in s
        and bool(re.search(r"(?m)^  contents: read\s*$", s)))
    has_permission = bool(PERMISSION.search(s))
    failure_gate_calls = len(FAILURE_GATE_CALL.findall(s))
    protected = bool(PROTECTED.search(s))
    risky_triggers = any(x in triggers for x in ("pull_request_target", "workflow_run"))
    if read_only_audit_exemption:
        tier = "READ_ONLY_AUDIT_TEXT"
    elif pushes and (gates < pushes or pushes_without_prior_gate):
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
        "failure_gate_call_signal_count": failure_gate_calls,
        "mutation_or_write_permission_without_failure_gate_signal":
            (has_write or has_permission) and failure_gate_calls == 0,
        "failure_circuit_runtime_verified": False,
        "failure_circuit_job_scope": job_scope(s),
        "indirect_write_signal": indirect_write,
        "indirect_write_without_gate_reference": indirect_write and gates == 0,
        "runtime_gate_order_verified": False,
        "pushes_without_prior_gate_signal": pushes_without_prior_gate,
        "push_gate_order_static_signal_only": True,
        "audit_text_exemption_requires_review": read_only_audit_exemption,
        "unverified_push_execution": bool(pushes),
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
        "failure_gate_call_signal_workflows": [r["path"] for r in records if r["failure_gate_call_signal_count"]],
        "failure_circuit_scope_review_paths": [r["path"] for r in records
                                               if r["mutation_or_write_permission_without_failure_gate_signal"]],
        "failure_circuit_runtime_verified_workflows": 0,
        "failure_circuit_job_scope_review": [
            {"path": r["path"], "jobs": r["failure_circuit_job_scope"]}
            for r in records if r["mutation_or_write_permission_without_failure_gate_signal"]
        ],
        "indirect_writers_without_gate_reference": [r["path"] for r in records if r["indirect_write_without_gate_reference"]],
        "runtime_gate_order_verified_workflows": 0,
        "audit_text_exemption_review_paths": [r["path"] for r in records if r["audit_text_exemption_requires_review"]],
        "pushes_without_prior_gate_signal": sum(r["pushes_without_prior_gate_signal"] for r in records),
        "push_order_review_paths": [r["path"] for r in records if r["pushes_without_prior_gate_signal"]],
        "unverified_push_execution_paths": [r["path"] for r in records if r["unverified_push_execution"]],
        "records": records,
        "limitations": "Static signals only: YAML context, scripts, action side effects, branch rules and runtime enforcement need separate verification.",
    }

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
