#!/usr/bin/env python3
"""Korunan dosya butunlugu ve yedek geri yukleme kanitlarini salt okunur incele."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)
protected = ["CALISANLAR.m3u", "AGENTS.md", "GUVENLIK_KURALLARI.md",
             "DEVAM_NOTU.md", "OZELLIK_ENVANTERI.md", "SEKIZ_GOREV_TOPLU_DENETIM.md"]
entries = []
for name in protected:
    path = ROOT / name
    entries.append({"path": name, "exists": path.is_file(),
                    "size": path.stat().st_size if path.is_file() else None,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None})
workflows = sorted((ROOT / ".github/workflows").glob("*.yml"))
backup_flows = [p.name for p in workflows if "yedek" in p.name.lower() or "backup" in p.name.lower()]
tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False)
files = tracked.stdout.splitlines() if tracked.returncode == 0 else []
backup_names = [x for x in files if "yedek" in x.lower() or "backup" in x.lower()]
restore_path = OUT / "izole_git_geri_yukleme_kaniti.json"
try:
    restore_evidence = json.loads(restore_path.read_text(encoding="utf-8"))
except (OSError, ValueError):
    restore_evidence = None
restore_verified = isinstance(restore_evidence, dict) and restore_evidence.get("all_match") is True
report = {
    "protected_files": entries,
    "protected_missing": [x["path"] for x in entries if not x["exists"]],
    "backup_workflows": backup_flows,
    "tracked_backup_named_files": backup_names,
    "restore_test": "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI" if restore_verified else "DOGRULANMADI",
    "restore_files_checked": len(restore_evidence.get("files", [])) if restore_verified else 0,
    "k4_archive_verifier": {\n        "script_present": (ROOT / "scripts/k4_external_restore_verify.py").is_file(),\n        "test_present": (ROOT / "test_k4_external_restore_verify.py").is_file(),\n        "workflow_present": (ROOT / ".github/workflows/k4-izole-geri-yukleme.yml").is_file(),\n        "archive_integrity_evidence": "GERCEK_YEDEK_KANITI_BEKLIYOR",\n        "actions_run_id": None,\n        "actions_result": "BU_RAPORDA_CANLI_API_ILE_DOGRULANMADI",\n        "external_backup_verified": False,\n        "historical_recovery_verified": False,\n    },\n    "historical_recovery_verified": False,
    "off_github_copy": "DOGRULANMADI",
    "github_branch_protection": "API_IZNI_OLMADAN_DOGRULANMADI",
    "limitations": "SHA256 mevcut surumun parmak izidir, onceki surumle degismeme kaniti degildir. Arşiv adi veya workflow varligi kurtarma basarisi kaniti degildir.",
    "safety": "Salt okunur; arsiv acilmaz, liste, yedek, cron veya izinler degistirilmez."
}
(OUT / "yedek_ve_korunan_dosyalar_kanit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
if report["protected_missing"]:
    raise SystemExit("Zorunlu korunan dosyalar eksik: " + ", ".join(report["protected_missing"]))
print(f"{len(entries)} korunan dosyanin SHA256 parmak izi kaydedildi; Git HEAD izole eslesme={restore_verified}; harici ve tarihsel geri yukleme dogrulanmadi.")
