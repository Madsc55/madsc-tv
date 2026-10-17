"""Read-only evidence matrix for all 26 approved MADSC TV safety rules.

A passing audit validates inventory completeness, NOT runtime enforcement.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "GUVENLIK_KURALLARI.md"
AGENT_RULES = ROOT / "AGENTS.md"
EVIDENCE = {
    1: ("tools/protected_write_gate.py", "Runtime and main-list change authorization"),
    2: ("scripts/k1_protected_integrity.py", "Channel metadata and authorized change comparison"),
    3: ("scripts/k1_protected_integrity.py", "IBO favorites and category order on device"),
    4: ("tools/protected_write_gate.py", "Explicit authorization for category movement"),
    5: ("scripts/k1_protected_integrity.py", "New channel approvals and alphabetical ordering"),
    6: ("scripts/k1_protected_integrity.py", "External and device backups"),
    7: (None, "Deletion history and tested restoration"),
    8: (None, "IBO user-approved working channel records"),
    9: (None, "Failed-channel and technical test history"),
    10: (None, "URL retest deduplication and retained history"),
    11: (None, "Alternative URL candidate isolation"),
    12: (None, "Discovery candidate deduplication and persistence"),
    13: (None, "Playback video audio resolution continuity checks"),
    14: (None, "Broadcast identity verification distinct from playback"),
    15: ("GUVENLIK_KURALLARI.md", "Real IBO Player device confirmation"),
    16: (None, "Pending candidate queue and idempotent continuation"),
    17: ("tools/protected_write_gate.py", "Approval for protected list edits"),
    18: (None, "Full candidate decision and edit history retention"),
    19: ("DEVAM_NOTU.md", "Complete handoff and task trail"),
    20: (None, "Restorable pre-edit backup and restore drill"),
    21: ("tools/protected_write_gate.py", "All production writers runtime gate enforcement"),
    22: ("scripts/k1_protected_integrity.py", "Authorized post-edit M3U ordering and URL checks"),
    23: (None, "Rollback target recorded and tested without silent changes"),
    24: ("tools/workflow_failure_gate.py", "Cross-run failure streak and stop/recovery in production"),
    25: ("AGENTS.md", "Actual GitHub Actions run ID and successful result for each code change"),
    26: ("AGENTS.md", "Turkish user-visible workflow job and step names for new or edited tests"),
}

def audit():
    source = RULES.read_text(encoding="utf-8")
    numbered = {int(n) for n in re.findall(r"(?m)^(\d{1,2})\.\s", source)}
    agent_source = AGENT_RULES.read_text(encoding="utf-8")
    agent_numbered = {int(n) for n in re.findall(r"(?m)^## Kural (25|26):", agent_source)}
    rows = []
    for number in range(1, 27):
        artifact, missing = EVIDENCE[number]
        exists = bool(artifact and (ROOT / artifact).is_file())
        rows.append({
            "rule": number,
            "evidence_candidate": artifact,
            "evidence_file_exists": exists,
            "status": "PARTIAL_EVIDENCE" if exists else "NEEDS_EVIDENCE",
            "outstanding_verification": missing,
        })
    return {
        "documented_rules": sorted(numbered | agent_numbered),
        "expected_rule_count": 26,
        "rule_count_valid": numbered == set(range(1, 25)),
        "rows": rows,
        "fully_verified_rules": 0,
        "limitations": "File existence is NOT enforcement proof; this audit intentionally makes no fully verified claims.",
    }

if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["rule_count_valid"] and len(report["rows"]) == 26 else 1)
