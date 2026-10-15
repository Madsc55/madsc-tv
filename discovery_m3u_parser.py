"""Pure M3U discovery parsers with explicit legacy-compatible policies.

No network requests, filesystem access, or playlist mutations.
"""
import re


def parse_discovery_m3u(text, profile):
    """Return scanner-compatible rows, preserving each scanner's metadata rules."""
    if profile == "wide_scan":
        rows = []
        meta = None
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("#EXTINF:"):
                meta = line
            elif line.startswith(("http://", "https://")) and meta:
                rows.append((meta.split(",", 1)[-1], line, meta))
                meta = None
        return rows
    if profile == "new_scan":
        rows = []
        meta = None
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("#EXTINF:"):
                meta = line
            elif line and not line.startswith("#") and meta:
                name = meta.rsplit(",", 1)[-1].strip()
                if name and line.startswith(("http://", "https://")):
                    match = re.search(r'tvg-logo="([^"]+)"', meta)
                    rows.append((name, line, match.group(1) if match else ""))
                meta = None
        return rows
    raise ValueError("Unknown M3U parse profile: " + str(profile))
