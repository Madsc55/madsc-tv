"""Exact-source, fail-closed K1 exception for one reviewed read-only audit.

Not a general write detector or permission to modify protected data.
Any edit to the reviewed workflow invalidates this exception.
"""
import hashlib
import re

REVIEWED_WORKFLOW = "toplu-sistem-kontrol.yml"
REVIEWED_BLOB_SHA = "34cf72108fb7aea4a1abde31027cfd3a859db43d"


def git_blob_sha(content: str) -> str:
    payload = content.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()


def is_reviewed_readonly_scanner(filename: str, content: str) -> bool:
    return bool(
        filename == REVIEWED_WORKFLOW
        and git_blob_sha(content) == REVIEWED_BLOB_SHA
        and re.search(r"(?m)^permissions:\s*\n  contents: read\s*$", content)
        and "persist-credentials: false" in content
        and "python - <<'PY'" in content
        and 'if re.search(r"\\bgit\\s+push\\b",raw)' in content
    )
