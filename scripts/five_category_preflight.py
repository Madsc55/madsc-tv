#!/usr/bin/env python3
"""Five-category read-only migration preflight: verify referenced scripts, tests and safety."""
from __future__ import annotations
import json
import re
from pathlib import Path

NAMES = (
    "madsc-01-guvenlik.yml",
    "madsc-02-kesif.yml",
    "madsc-03-kanal-test.yml",
    "madsc-04-arsiv-yedek.yml",
    "madsc-05-genel-bakim.yml",
)
PROTECTED = ("CALISANLAR.m3u", "AGENTS.md", "GUVENLIK_KURALLARI.md")

def inspect(root: Path) -> dict:
    rows = []
    errors = []
    for name in NAMES:
        path = root / ".github" / "workflows" / name
        if not path.is_file():
            errors.append(f"Missing category: {name}")
            continue
        raw = path.read_text(encoding="utf-8")
        scripts = re.findall(r"python3 (scripts/[\w.-]+\.py)", raw)
        tests = []
        for line in re.findall(r"python3 -m unittest ([^\n]+)", raw):
            tests.extend(t for t in line.split(";")[0].split() if t != "-v" and not t.startswith("-") and "$" not in t)
        for suites in re.findall(r"for suite in ([^\n;]+); do", raw):
            tests.extend(suites.split())
        missing_scripts = sorted(set(p for p in scripts if not (root / p).is_file()))
        missing_tests = sorted(set(t for t in tests if not (root / (t + ".py")).is_file()))
        read_only = bool(re.search(r"^\s*contents:\s*read\s*$", raw, re.M)) and not bool(re.search(r"^\s*contents:\s*write\s*$", raw, re.M))
        manual = bool(re.search(r"^\s*workflow_dispatch:\s*$", raw, re.M))
        hash_check = "sha256sum -c" in raw and all(p in raw for p in PROTECTED)
        if missing_scripts or missing_tests or not (read_only and manual and hash_check):
            errors.append(f"{name}: scripts={missing_scripts}, tests={missing_tests}, read_only={read_only}, manual={manual}, hash={hash_check}")
        rows.append({"category": name, "scripts": scripts, "tests": tests, "missing_scripts": missing_scripts, "missing_tests": missing_tests, "read_only": read_only, "manual": manual, "protected_hash_check": hash_check})
    backlog = root / "BES_SISTEM_TOPLU_IS_DEFTERI.md"
    if not backlog.is_file():
        errors.append("Missing durable work backlog")
    return {"status": "STATIC_READY" if not errors else "BLOCKED", "categories": rows, "errors": errors, "warning": "Static check only. Does not prove GitHub Actions success, full legacy parity, or IBO Player validation."}

def main():
    root = Path(__file__).resolve().parents[1]
    report = inspect(root)
    out = root / "madsc_merkezi_denetim" / "bes_kategori_on_kontrol.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "categories": len(report["categories"]), "errors": report["errors"]}, ensure_ascii=False))
    if report["errors"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
