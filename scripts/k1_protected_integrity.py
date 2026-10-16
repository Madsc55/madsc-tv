"""Read-only integrity comparison of critical files against origin/main."""
import subprocess
import sys

FILES = ("CALISANLAR.m3u", "CALISMAYANLAR.txt", "YENILER.m3u", "YABANCI_KANALLAR.m3u")

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def main():
    for path in FILES:
        baseline = git("rev-parse", "origin/main:" + path)
        current = git("rev-parse", "HEAD:" + path)
        print(f"{path}: main={baseline} branch={current} {'MATCH' if baseline == current else 'MISMATCH'}")
        if baseline != current:
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
