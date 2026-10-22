"""Safe normalization of persisted longitudinal observation history."""
from __future__ import annotations
import datetime


def normalize_history(rows, now):
    """Return valid timezone-aware observations from the preceding seven days.

    Invalid, naive, and future timestamps are ignored so they cannot inflate
    the measured stability span. This function never creates observations.
    """
    if not isinstance(now, datetime.datetime) or now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    now = now.astimezone(datetime.timezone.utc)
    if not isinstance(rows, list):
        return []
    result = []
    for item in rows:
        if not isinstance(item, dict) or not item.get("at") or not item.get("state"):
            continue
        try:
            stamp = datetime.datetime.fromisoformat(
                str(item["at"]).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        if stamp.tzinfo is None:
            continue
        stamp = stamp.astimezone(datetime.timezone.utc)
        age = (now - stamp).total_seconds()
        if 0 <= age <= 7 * 86400:
            result.append({"at": stamp.isoformat(), "state": str(item["state"])})
    return result
