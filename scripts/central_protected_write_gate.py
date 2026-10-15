#!/usr/bin/env python3
"""Korunan listelere yazma yetkisi olan GitHub Actions islerini salt okunur denetle."""
import json
import re
from pathlib import Path

def inspect(root):
    import yaml
    rows = []
    errors = []
    files = sorted(p for p in (root / ".github/workflows").iterdir() if p.suffix in (".yml", ".yaml"))
    for p in files:
        try:
            content = p.read_text(encoding="utf-8-sig")
            data = yaml.safe_load(content)
            if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict):
                errors.append(f"Invalid workflow: {p.name}")
                continue
            # A central workflow without explicit permissions inherits repository
            # defaults; do not treat that unknown default as read-only.
            if re.match(r"madsc-0[1-5]-", p.name) and "permissions" not in data:
                errors.append(f"Central workflow missing explicit permissions: {p.name}")
            permissions = data.get("permissions", {})
            writes = (permissions == "write-all" or
                      (isinstance(permissions, dict) and any(v == "write" for v in permissions.values())) or
                      bool(re.search(r"git\s+(?:push|commit)|create-pull-request", content, re.I)))
            # Job-level permissions override workflow-level defaults.
            for job in data["jobs"].values():
                if not isinstance(job, dict):
                    continue
                grant = job.get("permissions", {})
                if grant == "write-all" or (
                    isinstance(grant, dict) and any(value == "write" for value in grant.values())
                ):
                    writes = True
            if not writes:
                continue
            protected = bool(re.search(r"CALISANLAR\.m3u|YENILER\.m3u|yedekler/", content, re.I))
            gate = bool(re.search(r"environment:\s*[^\s]+", content))
            rows.append({"workflow": str(p.relative_to(root)), "write_capability": True,
                         "protected_path_reference": protected, "environment_gate_marker": gate,
                         "status": "MANUAL_REVIEW_REQUIRED"})
        except Exception as exc:
            errors.append(f"{p.name}: {exc}")
    central_violations = [
        row["workflow"] for row in rows
        if re.match(r"madsc-0[1-5]-", Path(row["workflow"]).name)
    ]
    return {"workflows_scanned": len(files), "review_required": rows, "review_count": len(rows),
            "central_write_violations": central_violations,
            "errors": errors, "limitations": ["Static heuristic cannot prove authorization enforcement",
                                              "No channel files or workflows were executed"]}

def main():
    root = Path(__file__).resolve().parents[1]
    result = inspect(root)
    out = root / "madsc_merkezi_denetim"
    out.mkdir(exist_ok=True)
    (out / "protected-write-gate-report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Korunan liste yazma denetimi: {result['workflows_scanned']} workflow, "
          f"{result['review_count']} manuel inceleme, {len(result['errors'])} hata.")
    if result["errors"] or result["central_write_violations"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
