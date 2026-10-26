#!/usr/bin/env python3
"""Non-destructive legacy workflow integration inventory and archive integrity report."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE_NAMES = (
    "MASTER_PROJE_HAFIZASI.md",
    "MASTER_PROJE_HAFIZASI_PART2.md",
    "MASTER_PROJE_HAFIZASI_PART3.md",
)
PROTECTED = ("CALISANLAR.m3u", "YENILER.m3u")
STAGES = {
    "K1": ("kaynak", "source", "kesif", "discovery", "tarama"),
    "K2": ("aday", "candidate", "dogrula", "verification", "verify", "test"),
    "K3": ("son-kontrol", "final", "continuity", "sureklilik"),
    "K4": ("logo", "epg", "gorsel", "image"),
    "K5": ("rapor", "report", "yedek", "backup", "audit", "publish"),
}


def tracked_files() -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        check=True, capture_output=True,
    )
    return [ROOT / p.decode("utf-8", "surrogateescape")
            for p in result.stdout.split(b"\0") if p]


def digest(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(path: pathlib.Path) -> list[str]:
    name = path.stem.lower()
    return [stage for stage, keys in STAGES.items() if any(key in name for key in keys)] or ["UNMAPPED"]


def workflow_details(path: pathlib.Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Retain source references rather than replacing unknown legacy semantics.
    triggers = [key for key in ("workflow_dispatch", "schedule", "workflow_run", "push", "pull_request")
                if re.search(r"(?m)^\s*" + re.escape(key) + r"\s*:", raw)]
    uses = re.findall(r"(?m)^\s*uses:\s*([^\n#]+)", raw)
    return {
        "path": str(path.relative_to(ROOT)), "sha256": digest(path),
        "stages": classify(path), "triggers": triggers,
        "dependencies": sorted(set(x.strip() for x in uses)),
        "has_write_permission": bool(re.search(r"(?m)^\s*(?:contents|actions):\s*write\b", raw)),
    }


def build_report() -> dict:
    files = tracked_files()
    workflows = sorted(
        (p for p in files if p.parent == ROOT / ".github" / "workflows"
         and p.suffix.lower() in (".yml", ".yaml") and p.is_file()),
        key=lambda p: p.name,
    )
    archives = []
    for name in ARCHIVE_NAMES:
        matches = sorted(p for p in files if p.name == name and p.is_file())
        archives.append({
            "requested_name": name,
            "matches": [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size,
                         "sha256": digest(p)} for p in matches],
            "status": "present" if matches else "not_found",
        })
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only",
        "workflow_count": len(workflows),
        "expected_legacy_count": 92,
        "legacy_equivalence_proven": False,
        "workflows": [workflow_details(p) for p in workflows],
        "archives": archives,
        "protected_files": [
            {"path": name, "sha256": digest(ROOT / name) if (ROOT / name).is_file() else None}
            for name in PROTECTED
        ],
        "notes": [
            "Classification is advisory; it does not prove behavior equivalence.",
            "Missing archives are reported, never replaced with synthetic contents.",
            "This tool never edits playlists, archives or legacy workflows.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="madsc_legacy_integration_report.json")
    args = parser.parse_args()
    report = build_report()
    output = pathlib.Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {report['workflow_count']} workflows; report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
