#!/usr/bin/env python3
"""Read-only fail-chain gate for GitHub Actions. Fail closed on API errors."""
import json
import os
import sys
import urllib.request
import urllib.parse

MAX_HISTORY_PAGES = 10


class IncompleteHistory(ValueError):
    """More API history is needed before a safe decision is possible."""


def should_stop(runs, current_id, threshold=2, history_complete=True):
    current_run = next((r for r in runs if r.get("id") == current_id), None)
    current_created = current_run.get("created_at") if current_run else None
    if current_created is None:
        if not history_complete:
            raise IncompleteHistory("Current workflow run not yet found in paginated history")
        # Missing current run metadata cannot establish which runs are earlier.
        # Deny rather than accidentally counting later failures as history.
        raise ValueError("Current workflow run missing from failure history")
    if any(r.get("id") != current_id and r.get("status") == "completed"
           and not r.get("created_at") for r in runs):
        raise ValueError("Completed workflow run missing creation timestamp")
    prior = [r for r in runs if r.get("id") != current_id and r.get("status") == "completed"
             and (r["created_at"] < current_created
                  or (r["created_at"] == current_created and r.get("id", 0) < current_id))]
    prior.sort(key=lambda r: (r["created_at"], r.get("id", 0)), reverse=True)
    if len(prior) < threshold and not history_complete:
        raise IncompleteHistory("Insufficient completed workflow history")
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
    headers = {
        "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"}
    runs = []
    received = 0
    for page in range(1, MAX_HISTORY_PAGES + 1):
        req = urllib.request.Request(url + f"&page={page}", headers=headers)
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.load(response)
        batch = payload["workflow_runs"]
        total = payload.get("total_count")
        if (not isinstance(batch, list) or any(not isinstance(r, dict) for r in batch)
                or (total is not None and (type(total) is not int or total < 0))):
            raise ValueError("Invalid workflow history response")
        received += len(batch)
        more = received < total if total is not None else len(batch) == 100
        if more and not batch:
            raise ValueError("Workflow history ended before reported total")
        # Check branch locally as well as relying on the API-side filter.
        runs.extend(r for r in batch if r.get("head_branch") == branch)
        try:
            stop, streak = should_stop(runs, current, history_complete=not more)
        except IncompleteHistory:
            continue
        break
    else:
        raise ValueError("Workflow history page limit reached without sufficient evidence")
    print(f"Previous consecutive failed/timed-out runs: {streak}; threshold: 2")
    if stop:
        print("CIRCUIT OPEN: stopping this workflow safely. Existing reports and playlists untouched.")
        sys.exit(1)

if __name__ == "__main__":
    main()
