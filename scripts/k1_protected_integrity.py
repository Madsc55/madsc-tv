"""Read-only comparison of tracked protected files against origin/main.

This does not inspect IBO Player device-side favorites or category order.
"""
import subprocess
import sys

EXACT = ("CALISANLAR.m3u", "CALISMAYANLAR.txt", "YENILER.m3u",
         "YABANCI_KANALLAR.m3u", "GUVENLIK_KURALLARI.md")
PREFIXES = ("yedekler/", "YEDEKLER/", "FAVORILER/", "HEPSI/")


def git(*args):
    return subprocess.check_output(["git", *args]).decode("utf-8").strip()


def protected(path):
    folded = path.casefold()
    return (folded in {name.casefold() for name in EXACT}
            or any(folded.startswith(prefix.casefold()) for prefix in PREFIXES)
            or folded.endswith(".m3u"))


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


def main():
    baseline, current = tree("origin/main"), tree("HEAD")
    paths = sorted(set(baseline) | set(current))
    mismatches = [p for p in paths if baseline.get(p) != current.get(p)]
    for path in paths:
        print(f"{path}: {'MISMATCH' if path in mismatches else 'MATCH'}")
    print(f"Protected tracked paths: {len(paths)}, mismatches: {len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
