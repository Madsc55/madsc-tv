"""Read-only comparison of tracked protected files against origin/main.

This does not inspect IBO Player device-side favorites or category order.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXACT = ("CALISANLAR.m3u", "CALISMAYANLAR.txt", "YENILER.m3u",
         "YABANCI_KANALLAR.m3u", "GUVENLIK_KURALLARI.md", "AGENTS.md")
PREFIXES = ("yedekler/", "YEDEKLER/", "FAVORILER/", "HEPSI/")


def git(*args):
    return subprocess.check_output(["git", *args]).decode("utf-8").strip()


def protected(path):
    folded = path.casefold()
    return (folded in {name.casefold() for name in EXACT}
            or any(folded.startswith(prefix.casefold()) for prefix in PREFIXES)
            or folded.endswith(".m3u")
            or Path(folded).stem in {"favoriler", "favorites", "hepsi"})


def tree(ref):
    data = subprocess.check_output(["git", "ls-tree", "-r", "-z", ref])
    entries = {}
    for item in data.split(b"\x00"):
        if not item:
            continue
        metadata, path = item.split(b"\t", 1)
        name = path.decode("utf-8")
        if protected(name):
            entries[name] = metadata.split()[-1].decode("ascii")
    return entries


def working_snapshot():
    # HEAD preserves the baseline even if a job removes a path from the index.
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    # Include newly created protected files, even when they are not in the index.
    # Keep generated nested candidate M3U reports outside protected collections.
    untracked = subprocess.check_output(["git", "ls-files", "--others", "-z"]).decode().split("\0")
    def protected_untracked(name):
        folded = name.casefold()
        return protected(name) and (
            "/" not in name or any(folded.startswith(prefix.casefold()) for prefix in PREFIXES)
        )
    paths = (set(tree("HEAD"))
             | {p for p in tracked if p and protected(p)}
             | {p for p in untracked if p and protected_untracked(p)})
    result = {}
    for name in sorted(paths):
        path = Path(name)
        if path.is_symlink():
            result[name] = {"kind": "symlink", "target": str(path.readlink())}
        elif path.is_file():
            result[name] = {"kind": "file", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "mode": path.stat().st_mode & 0o777}
        else:
            result[name] = {"kind": "missing"}
    return result


def runtime_check(mode, manifest):
    current = working_snapshot()
    if mode == "snapshot":
        if not current or any(item["kind"] != "file" for item in current.values()):
            raise ValueError("Protected baseline missing or not a regular file")
        manifest.write_text(json.dumps(current, sort_keys=True), encoding="utf-8")
        print(f"Korunan dosya baslangici: {len(current)}")
        return 0
    baseline = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(baseline, dict) or not baseline:
        raise ValueError("Empty or invalid protected baseline")
    changes = [name for name in sorted(set(baseline) | set(current))
               if baseline.get(name) != current.get(name)]
    print(json.dumps({"protected_files": len(baseline), "changed_paths": changes}))
    return int(bool(changes))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("snapshot", "check"))
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.mode:
        if not args.manifest:
            parser.error("--manifest is required with --mode")
        return runtime_check(args.mode, args.manifest)

    baseline, current = tree("origin/main"), tree("HEAD")
    paths = sorted(set(baseline) | set(current))
    mismatches = [p for p in paths if baseline.get(p) != current.get(p)]
    for path in paths:
        print(f"{path}: {'MISMATCH' if path in mismatches else 'MATCH'}")
    print(f"Protected tracked paths: {len(paths)}, mismatches: {len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
