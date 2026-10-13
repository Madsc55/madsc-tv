#!/usr/bin/env python3
"""MADSC-TV read-only repository integration, safety and health audit."""
import argparse
import ast
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRITICAL = ("AGENTS.md", "GUVENLIK_KURALLARI.md", "DEVAM_NOTU.md",
            "OZELLIK_ENVANTERI.md", "CALISANLAR.m3u", "YENILER.m3u")
PIPELINE = ("madsc_akilli_kesif.py", "madsc_uc_asama.py",
            "final_validation.py", "tools/son_kontrol_yedekler_aktar.py",
            "tools/yedekler_guvenli_ekle.py")
REPORTS = ("madsc_dogrulama/summary.json", "madsc_son_kontrol/summary.json",
           "madsc_son_kontrol/results.json", "madsc_kesif/candidate_epg_logo_join.json")


def inspect(root=ROOT):
    findings = []
    actions = {
        "MISSING_FILE": "Eksik dosyayı araştır; otomatik geri yükleme yapma.",
        "BROAD_PERMISSIONS": "Actions izinlerini gereken en dar kapsamla sınırla.",
        "PYTHON_SYNTAX": "Dosyanın sözdizimini düzeltip test et.",
        "INVALID_JSON": "Rapor üreticisini ve son başarılı çalışmayı incele.",
        "COUNT_MISMATCH": "Özet ile sonuçların aynı çalışmaya ait olduğunu doğrula.",
        "DUPLICATE_CANDIDATE_IDS": "Tekrar eden adayları araştır; geçmişi silme.",
        "SHARED_CONCURRENCY_GROUP": "Grup farklı workflowları sıraya alıyor; iptal ayarını ve gecikmeyi izle.",
        "SHARED_CONCURRENCY_SAFE": "cancel-in-progress: false ile sıralama bilinçli; uzun kuyrukları izle.",
        "WRITE_WORKFLOW_REVIEW": "Yazma iznini ve tetikleyici güvenliğini incele.",
        "RESET_PUSH_REVIEW": "Reset ve push komutlarının veri kaybı riskini incele.",
        "RESET_PUSH_GUARDED": "Rapor çakışmasında işlem durdurulur ve artifact korunur; başarısız çalışmaları izle.",
        "MISSING_REPORT": "Raporu üreten otomasyonun son çalışmasını incele.",
        "PENDING_CANDIDATES": "Sonraki aday kontrol partilerini bekle.",
        "NO_READY_CANDIDATES": "Kimlik ve IBO doğrulaması olmadan hazır kabul etme.",
        "EMPTY_CANDIDATE_JOIN": "Yeni aday yoksa işlem gerekmez; keşif sonuçlarını izle.",
    }
    def add(level, category, code, detail):
        findings.append({"severity": level, "category": category, "code": code,
                         "detail": detail, "next_action": actions.get(code, "Bulguyu incele; korunan verileri değiştirme.")})

    for path in CRITICAL + PIPELINE:
        if not (root / path).is_file():
            add("ERROR", "inventory", "MISSING_FILE", path)
    workflows = sorted((root / ".github/workflows").glob("*.yml"))
    workflows += sorted((root / ".github/workflows").glob("*.yaml"))
    if not workflows:
        add("ERROR", "automation", "NO_WORKFLOWS", "GitHub Actions bulunamadı")
    for path in workflows:
        raw = path.read_text(encoding="utf-8")
        if re.search(r"pull_request_target\s*:", raw) and re.search(r"actions/checkout@", raw):
            add("WARN", "security", "PR_TARGET_CHECKOUT", path.name)
        if re.search(r"cancel-in-progress:\s*true", raw):
            add("INFO", "automation", "CANCEL_ON_NEW_RUN", path.name)
        if "workflow_dispatch:" in raw and "schedule:" in raw:
            add("INFO", "automation", "MANUAL_AND_SCHEDULED", path.name)
    # Same concurrency group across distinct workflows can cause unexpected cancellations.
    groups = {}
    for path in workflows:
        raw = path.read_text(encoding="utf-8")
        for line in raw.splitlines():
            match = re.fullmatch(r"group:\s*([A-Za-z0-9_.-]+)", line.strip())
            if match:
                groups.setdefault(match.group(1), []).append((path.name, "cancel-in-progress: false" in raw))
        if re.search(r"(?m)^\s*permissions:\s*write-all\s*$", raw):
            add("ERROR", "security", "BROAD_PERMISSIONS", path.name)
        if "contents: write" in raw and "workflow_dispatch:" not in raw and "workflow_run:" not in raw:
            add("WARN", "security", "WRITE_WORKFLOW_REVIEW", path.name)
        if "git reset --hard" in raw and "git push" in raw:
            if "madsc-rapor-base-sha" in raw and "git diff --quiet" in raw and "Artifact saklandi" in raw:
                add("INFO", "automation", "RESET_PUSH_GUARDED", path.name)
            else:
                add("WARN", "automation", "RESET_PUSH_REVIEW", path.name)
    for group, owners in groups.items():
        if len(owners) > 1:
            names = ", ".join(name for name, _ in owners)
            if all(safe for _, safe in owners):
                add("INFO", "automation", "SHARED_CONCURRENCY_SAFE", f"{group}: {names}; iptal kapalı, sıralama amaçlı")
            else:
                add("WARN", "automation", "SHARED_CONCURRENCY_GROUP", f"{group}: {names}; iptal riski incelenmeli")
    for path in sorted(root.glob("*.py")) + sorted((root / "tools").glob("*.py")) + sorted((root / "scripts").glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            add("ERROR", "code", "PYTHON_SYNTAX", f"{path.relative_to(root)}: {exc}")
    snapshots = {}
    for rel in REPORTS:
        path = root / rel
        if not path.exists():
            add("WARN", "pipeline", "MISSING_REPORT", rel)
            continue
        try:
            snapshots[rel] = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError):
            add("ERROR", "pipeline", "INVALID_JSON", rel)
    summary = snapshots.get("madsc_son_kontrol/summary.json")
    results = snapshots.get("madsc_son_kontrol/results.json")
    if isinstance(summary, dict) and isinstance(results, list):
        if summary.get("completed") != len(results):
            add("ERROR", "pipeline", "COUNT_MISMATCH", f"summary={summary.get('completed')} results={len(results)}")
        if summary.get("remaining", 0) > 0:
            add("INFO", "pipeline", "PENDING_CANDIDATES", str(summary["remaining"]))
        if summary.get("ready_for_playlist", 0) == 0:
            add("INFO", "pipeline", "NO_READY_CANDIDATES", "Teknik geçiş gerçek kimlik/IBO onayı değildir")
    if isinstance(results, list):
        tokens = [row.get("candidate_id") for row in results if isinstance(row, dict)]
        if len(tokens) != len(set(tokens)):
            add("ERROR", "pipeline", "DUPLICATE_CANDIDATE_IDS", "Son kontrol kayıtlarında tekrar eden aday kimliği")
        if len(tokens) != len(results):
            add("ERROR", "pipeline", "MALFORMED_RESULT", "Son kontrol kaydında aday kimliği eksik")
    join = snapshots.get("madsc_kesif/candidate_epg_logo_join.json")
    if isinstance(join, dict) and join.get("source_candidates") == 0:
        add("INFO", "integration", "EMPTY_CANDIDATE_JOIN", "Bu rapor döneminde yeni logo/EPG adayı yok; tek başına hata değildir")
    playlist = root / "CALISANLAR.m3u"
    if playlist.is_file():
        content = playlist.read_text(encoding="utf-8-sig")
        if not content.startswith("#EXTM3U"):
            add("ERROR", "playlist", "BAD_M3U_HEADER", "CALISANLAR.m3u")
        backups = re.findall(r'group-title="📦 YEDEKLER \((\d+)\)"', content)
        if backups and len(backups) != int(backups[0]):
            add("ERROR", "playlist", "BACKUP_COUNT_MISMATCH", f"etiket={backups[0]} kayıt={len(backups)}")
        if backups and len(set(backups)) != 1:
            add("ERROR", "playlist", "BACKUP_COUNT_LABELS", str(sorted(set(backups))))
    findings.sort(key=lambda f: ({"ERROR": 0, "WARN": 1, "INFO": 2}[f["severity"]], f["code"], f["detail"]))
    return {"generated_utc": datetime.now(timezone.utc).isoformat(),
            "mode": "READ_ONLY", "workflows_scanned": len(workflows),
            "findings": findings,
            "counts": {s: sum(f["severity"] == s for f in findings) for s in ("ERROR", "WARN", "INFO")},
            "scope": "Repository static checks and saved-report consistency; not live IBO or real stream identity"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="madsc_bakim/sistem_saglik_raporu.json")
    args = parser.parse_args()
    report = inspect()
    path = ROOT / args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], ensure_ascii=False))
    print(f"Denetlenen GitHub Actions: {report['workflows_scanned']}")
    raise SystemExit(1 if report["counts"]["ERROR"] else 0)


if __name__ == "__main__":
    main()
