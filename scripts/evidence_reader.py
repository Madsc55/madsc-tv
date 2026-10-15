"""Shared, side-effect-free JSON evidence reader for central reports."""
import json


def read_json_evidence(path):
    """Return (state, payload): missing, invalid, or present.

    A present JSON value is not necessarily a valid report schema.
    """
    if not path.is_file():
        return "missing", None
    try:
        return "present", json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return "invalid", None
