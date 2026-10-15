#!/usr/bin/env python3
"""P0 legacy security acceptance: read-only, fail-closed on missing evidence."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / ".github" / "workflows"
PROTECTED = ("CALISANLAR.m3u", "YENILER.m3u", "FAVORILER", "YEDEKLER")
GATE = "tools/workflow_failure_gate.py"


def inspect(root=ROOT):
    folder = Path(root) / ".github" / "workflows"
    legacy = sorted(p for p in folder.glob("*.y*ml")
                    if not re.match(r"madsc-0[1-5]-", p.name)
                    and p.name != "madsc-p0-dort-guvenlik-kabul.yml")
    if len(legacy) != 92:
        raise ValueError(f"Expected 92 legacy workflows, found {len(legacy)}")
    rows = []
    for path in legacy:
        raw = path.read_text(encoding="utf-8-sig")
        # These are conservative indicators, not proof of actual execution.
        declared_write = bool(re.search(r"(?m)^\s*(?:contents|actions|pull-requests):\s*write\s*$", raw))
        git_push = bool(re.search(r"\bgit\s+push\b", raw))
        reset_hard = bool(re.search(r"\bgit\s+reset\s+--hard\b", raw))
        dispatch = bool(re.search(r"\b(?:gh\s+workflow\s+run|dispatches)\b", raw))
        scheduled = bool(re.search(r"(?m)^\s*schedule:\s*$", raw))
        workflow_run = bool(re.search(r"(?m)^\s*workflow_run:\s*$", raw))
        concurrency = bool(re.search(r"(?m)^concurrency:\s*$", raw))
        write_candidate = declared_write or git_push or reset_hard
        rows.append({
            "workflow": path.name, "declared_write": declared_write,
            "git_push": git_push, "reset_hard": reset_hard,
            "dispatch": dispatch, "schedule": scheduled,
            "workflow_run": workflow_run, "concurrency": concurrency,
            "rule24_direct_gate": GATE in raw,
            "protected_reference": any(x.lower() in raw.lower() for x in PROTECTED),
            "manual_review_required": write_candidate,
            "risk_reasons": (["WRITE_WITHOUT_CONCURRENCY"] if write_candidate and not concurrency else [])
                            + (["WRITE_WITHOUT_DIRECT_RULE24_GATE"] if write_candidate and GATE not in raw else [])
                            + (["MULTIPLE_EVENT_TYPES"] if scheduled and workflow_run else [])
                            + (["HARD_RESET"] if reset_hard else [])
        })
    return {
        "legacy_count": len(rows), "rows": rows,
        "write_review_count": sum(r["manual_review_required"] for r in rows),
        "risk_count": sum(bool(r["risk_reasons"]) for r in rows),
        "acceptance": "BLOCKED_NEEDS_ENFORCEMENT_AND_RUNTIME_EVIDENCE",
        "limits": [
            "Static text inspection is not runtime authorization proof",
            "Branch protection requires independent GitHub settings verification",
            "26-rule policy cannot be declared fully enforced by this audit",
            "No playlists, workflows, or backups are modified"
        ]
    }


def main():
    report = inspect()
    out = ROOT / "madsc_merkezi_denetim"
    out.mkdir(exist_ok=True)
    (out / "p0_dort_guvenlik_toplu_kabul.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"92 legacy workflows inspected; {report['risk_count']} risk rows; "
          f"{report['write_review_count']} write candidates; acceptance blocked.")
    for row in report["rows"]:
        if row["risk_reasons"]:
            print("OPEN", row["workflow"], ": ", ", ".join(row["risk_reasons"]))
    if report["risk_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
