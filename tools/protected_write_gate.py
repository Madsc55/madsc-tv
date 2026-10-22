"""Fail-closed protected path check for *proposed* Git changes.

This module never writes a playlist or changes Git state. Call before any push.
A successful check is not a substitute for GitHub branch rulesets.
"""
import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath

PROTECTED_EXACT = frozenset({
    "CALISANLAR.m3u",
    "CALISMAYANLAR.txt",
    "YENILER.m3u",
    "YABANCI_KANALLAR.m3u",
    "GUVENLIK_KURALLARI.md",
    "AGENTS.md",
})
PROTECTED_PREFIXES = ("yedekler/", "YEDEKLER/", "FAVORILER/", "HEPSI/",
                      "EPG/", "logolar/", "logos/", "arsiv/")


def blocked_paths(paths):
    """Conservatively reject protected paths and any unexpected M3U mutations."""
    blocked = []
    for raw in paths:
        name = raw.replace("\\", "/")
        parts = name.split("/")
        if (not name or name.startswith("/")
                or any(part in ("", ".", "..") for part in parts)):
            blocked.append(name)
            continue
        folded = name.casefold()
        if (folded in {item.casefold() for item in PROTECTED_EXACT}
                or any(folded.startswith(prefix.casefold()) for prefix in PROTECTED_PREFIXES)
                or PurePosixPath(name).suffix.lower() in (".m3u", ".m3u8")
                or PurePosixPath(folded).stem in ("favoriler", "favorites", "hepsi")
                or any(part.casefold() in ("favoriler", "hepsi", "yedekler",
                                            "epg", "logolar", "logos", "arsiv") for part in parts)):
            blocked.append(name)
    return blocked


def git_changed_paths(base):
    """Read changes between base and HEAD; fail on missing or invalid Git base."""
    # Resolve with option parsing explicitly ended; never interpolate caller input
    # into git diff, where --relative/--output could suppress evidence or write.
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.decode("ascii").strip()
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", resolved):
        raise ValueError("Invalid resolved baseline commit")
    result = subprocess.run(
        ["git", "diff", "--name-only", "-z", "--no-renames", f"{resolved}..HEAD"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "-z", "--no-renames"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    unstaged = subprocess.run(
        ["git", "diff", "--name-only", "-z", "--no-renames"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    # Include ignored files so protected runtime paths cannot hide in .gitignore.
    ignored = subprocess.run(
        ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return [p.decode("utf-8", errors="strict") for p in
            (result.stdout + staged.stdout + unstaged.stdout + untracked.stdout + ignored.stdout).split(bytes([0])) if p]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="trusted baseline commit")
    args = parser.parse_args(argv)
    try:
        paths = git_changed_paths(args.base)
        blocked = blocked_paths(paths)
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError) as exc:
        print(f"DENY: unable to verify Git changes: {exc}", file=sys.stderr)
        return 2
    if blocked:
        print("DENY: protected paths changed: " + ", ".join(blocked), file=sys.stderr)
        return 1
    print(f"ALLOW: {len(paths)} changed paths checked, no protected paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
