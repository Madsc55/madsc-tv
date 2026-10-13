#!/usr/bin/env python3
"""Read public/non-secret repository settings for the unified recovery package."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

repo = os.environ.get("GITHUB_REPOSITORY", "Madsc55/madsc-tv")
token = os.environ.get("GH_TOKEN", "")
root = f"https://api.github.com/repos/{repo}"
endpoints = {
    "repository": root,
    "branches": root + "/branches?per_page=100",
    "workflows": root + "/actions/workflows?per_page=100",
    "rulesets": root + "/rulesets?per_page=100",
    "actions_permissions": root + "/actions/permissions",
}
results = {}
for name, url in endpoints.items():
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "MADSC-backup"}
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urlopen(Request(url, headers=headers), timeout=15) as response:
            data = json.load(response)
        if name == "repository":
            allowed = ("name", "full_name", "private", "default_branch", "description",
                       "has_issues", "has_wiki", "has_projects", "allow_squash_merge",
                       "allow_merge_commit", "allow_rebase_merge", "delete_branch_on_merge",
                       "visibility", "archived", "disabled")
            data = {k: data.get(k) for k in allowed}
        elif name == "branches":
            data = [{"name": x.get("name"), "protected": x.get("protected")} for x in data]
        elif name == "workflows":
            data = [{"name": x.get("name"), "path": x.get("path"), "state": x.get("state")} for x in data.get("workflows", [])]
        elif name == "rulesets":
            data = [{"name": x.get("name"), "enforcement": x.get("enforcement"), "target": x.get("target")} for x in data]
        results[name] = {"status": "OK", "data": data}
    except (HTTPError, URLError, ValueError, KeyError) as exc:
        results[name] = {"status": "UNAVAILABLE", "reason": type(exc).__name__}
results["external_settings"] = {
    "status": "NOT_INCLUDED",
    "items": ["GitHub secret values", "IBO Player device/account settings",
              "untracked files", "expired workflow artifacts", "GitHub account settings"],
    "reason": "Not readable safely via repository file backup",
}
Path("MADSC-SISTEM-AYAR-ENVANTERI.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print("Ayar envanteri olusturuldu; gizli degerler arsivlenmedi.")
