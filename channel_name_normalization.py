"""Pure channel-name normalization with explicit legacy-compatible profiles.

No network, filesystem access, or playlist writes.
"""
import re
import unicodedata


def normalize_channel_name(name, profile="wide_scan"):
    """Normalize names without silently equating distinct legacy policies."""
    if profile == "wide_scan":
        value = re.sub(r"\[[^]]*\]|\([^)]*\)", "", name).casefold()
        value = "".join(
            char for char in unicodedata.normalize("NFKD", value.replace("ı", "i"))
            if not unicodedata.combining(char)
        )
        value = re.sub(
            r"\b(4k|uhd|fhd|hd|sd|hq|1440p|1080p|720p|576p|480p|360p|270p|aday|alternatif|tr)\b",
            "", value,
        )
        return re.sub(r"[^a-z0-9]", "", value)
    if profile == "new_scan":
        value = name.upper().translate(str.maketrans("İÇŞĞÜÖ", "ICSGUO"))
        value = re.sub(r"\[[^]]*\]|\([^)]*\)", " ", value)
        value = re.sub(
            r"\b(?:TR|TURKIYE|HD|FHD|UHD|QHD|SD|1080P|720P|576P|480P|360P)\b",
            " ", value,
        )
        return re.sub(r"[^A-Z0-9]", "", value)
    raise ValueError("Unknown normalization profile: " + str(profile))
