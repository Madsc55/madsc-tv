#!/usr/bin/env python3
"""Read-only fail-chain gate for GitHub Actions. Fail closed on API errors."""
import json
import os
import sys
import urllib.request
import urllib.parse

def should_stop(runs, current_id, threshold=2):
    current_run = next((r for r in runs if r.get("id") == current_id), None)
    current_created = current_run.get("created_at") if current_run else None
    if current_created is None:
        # Missing current run metadata cannot establish which runs are earlier.
        # Deny rather than accidentally counting later failures as history.
        raise ValueError("Current workflow run missing from failure history")
    prior = [r for r in runs if r.get("id") != current_id and r.get("status") == "completed"
             and (not current_created or r.get("created_at", "") <= current_created)]
    prior.sort(key=lambda r: (r.get("created_at", ""), r.get("id", 0)), reverse=True)
    streak = 0
    for run in prior:
        if run.get("conclusion") == "success":
            break
        if run.get("conclusion") in ("failure", "timed_out"):
            streak += 1
        else:
            break
    return streak >= threshold, streak

def main():
    repo = os.environ["GITHUB_REPOSITORY"]
    workflow = os.environ["GITHUB_WORKFLOW_REF"].split("/.github/workflows/", 1)[1].split("@", 1)[0]
    current = int(os.environ["GITHUB_RUN_ID"])
    # Manual dispatch must not bypass a circuit already opened by failures.
    branch = os.environ["GITHUB_REF_NAME"]
    url = (f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/runs"
           f"?per_page=100&branch={urllib.parse.quote(branch, safe='')}")
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(req, timeout=25) as response:
        runs = json.load(response)["workflow_runs"]
    # GitHub branch query is an API-side filter; verify returned data as well.
    runs = [r for r in runs if r.get("head_branch") == branch]
    stop, streak = should_stop(runs, current)
    print(f"Previous consecutive failed/timed-out runs: {streak}; threshold: 2")
    if stop:
        print("CIRCUIT OPEN: stopping this workflow safely. Existing reports and playlists untouched.")
        sys.exit(1)

if __name__ == "__main__":
    main()
