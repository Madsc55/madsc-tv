#!/usr/bin/env python3
"""Korunan dosyalarin HEAD git surumunu gecici dizine geri alip byte esligini test et."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ("CALISANLAR.m3u", "AGENTS.md", "GUVENLIK_KURALLARI.md")
OUT = ROOT / "madsc_merkezi_denetim"

def verify(repo=ROOT):
    rows = []
    with tempfile.TemporaryDirectory(prefix="madsc-izole-geri-yukleme-") as folder:
        for name in FILES:
            current = repo / name
            cmd = subprocess.run(["git", "show", f"HEAD:{name}"], cwd=repo,
                                 capture_output=True, check=False)
            if cmd.returncode or not current.is_file():
                rows.append({"file": name, "status": "GIT_SURUMU_VEYA_DOSYA_YOK"})
                continue
            restored = Path(folder) / name
            restored.write_bytes(cmd.stdout)
            actual = hashlib.sha256(current.read_bytes()).hexdigest()
            archived = hashlib.sha256(restored.read_bytes()).hexdigest()
            rows.append({"file": name, "status": "ESLESIYOR" if actual == archived else "FARK_VAR",
                         "working_sha256": actual, "restored_sha256": archived})
    return {"method": "GIT_HEAD_TO_TEMPORARY_DIRECTORY", "files": rows,
            "all_match": bool(rows) and all(x["status"] == "ESLESIYOR" for x in rows),
            "external_backup_verified": False, "historical_recovery_verified": False,
            "limitations": "Yalniz HEAD git blobu gecici dizinde geri acilip mevcut dosyayla karsilastirildi; eski surum veya GitHub disi yedek testi degildir.",
            "safety": "Korunan dosyalar, git gecmisi, yedekler ve cron degistirilmez."}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    result = verify()
    (OUT / "izole_git_geri_yukleme_kaniti.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Izole Git HEAD geri yukleme: {len(result['files'])} dosya; eslesme={result['all_match']}.")
    if not result["all_match"]:
        raise SystemExit("Korunan dosya Git HEAD butunluk farki!")
