"""Read-only verification of declared permissions in shadow workflow files."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    ".github/workflows/madsc-03-kanal-test.yml": "EPG ve Pages yayin baglantisi salt okunur kabul kontrolu",
    ".github/workflows/madsc-04-arsiv-yedek.yml": "Yedek kurtarma ve uzak kopya ayrimi kabul kontrolu",
}

def declared_permissions(raw):
    found = []
    run_indent = None
    permission_indent = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if run_indent is not None:
            if indent > run_indent:
                continue
            run_indent = None
        if permission_indent is not None and indent <= permission_indent:
            permission_indent = None
        if re.match(r"^\s*(?:-\s*)?run:\s*[|>][-+]?\s*(?:#.*)?$", line):
            run_indent = indent
            continue
        if re.match(r"^\s*permissions:\s*$", line):
            permission_indent = indent
            continue
        if permission_indent is not None and indent > permission_indent:
            match = re.match(r"^\s*(contents|actions):\s*([\w-]+)\s*(?:#.*)?$", line)
            if match:
                found.append((match.group(1), match.group(2)))
    return found

def validate(raw, gate_name):
    if gate_name not in raw:
        raise AssertionError("Missing shadow acceptance step: " + gate_name)
    declared = declared_permissions(raw)
    if ("contents", "read") not in declared:
        raise AssertionError("Explicit read-only contents permission missing")
    unsafe = [(name, value) for name, value in declared if value not in ("read", "none")]
    if unsafe:
        raise AssertionError("Write or unknown permission in shadow workflow: " + str(unsafe))
    return declared

def main(root=ROOT):
    result = {}
    for path, gate in TARGETS.items():
        result[path] = validate((Path(root) / path).read_text(encoding="utf-8"), gate)
    print("Two shadow permission checks passed (static evidence)")
    return result

if __name__ == "__main__":
    main()
