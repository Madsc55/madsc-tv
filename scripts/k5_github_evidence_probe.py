#!/usr/bin/env python3
"""Read-only GitHub Actions identity checks; NOT behavioral parity certification."""
import argparse
import json
import os
import urllib.error
import re
import urllib.request
from pathlib import Path


def fetch_json(repo, endpoint, token):
    if not re.fullmatch(r"(?!\\.{1,2}(?:/|$))[A-Za-z0-9_][A-Za-z0-9_.-]*/[A-Za-z0-9_][A-Za-z0-9_.-]*", repo or "") or not token:
        raise ValueError("GitHub repository and read-only token required")
    url = "https://api.github.com/repos/" + repo + "/" + endpoint
    request = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "madsc-k5-evidence-probe",
    })
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def probe(rows, repo, token, fetch=fetch_json):
    if not isinstance(rows, list):
        raise ValueError("Evidence must be a list")
    if not isinstance(repo, str) or not re.fullmatch(r"(?!\\.{1,2}(?:/|$))[A-Za-z0-9_][A-Za-z0-9_.-]*/[A-Za-z0-9_][A-Za-z0-9_.-]*", repo):
        raise ValueError("Invalid repository identifier")
    results = []
    seen = set()
    for row in rows:
        name = row.get("legacy_workflow") if isinstance(row, dict) else None
        result = {"legacy_workflow": name, "github_metadata_verified": False, "errors": []}
        results.append(result)
        try:
            if not isinstance(row, dict):
                raise ValueError("Evidence record must be an object")
            if not isinstance(name, str) or not name.endswith((".yml", ".yaml")) or "/" in name:
                raise ValueError("Invalid legacy workflow name")
            if name in seen:
                raise ValueError("Duplicate legacy workflow evidence")
            seen.add(name)
            replacement = row.get("replacement_workflow")
            if not isinstance(replacement, str) or not re.fullmatch(r"madsc-0[1-5]-[A-Za-z0-9_.-]+\.ya?ml", replacement):
                raise ValueError("Invalid replacement workflow")
            sha = row.get("source_sha")
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
                raise ValueError("Invalid source SHA")
            run_id, job_id, artifact_id = (row.get(k) for k in ("run_id", "job_id", "artifact_id"))
            if any(type(value) is not int or value <= 0 for value in (run_id, job_id, artifact_id)):
                raise ValueError("Positive integer run/job/artifact IDs required")
            run = fetch(repo, "actions/runs/" + str(run_id), token)
            job = fetch(repo, "actions/jobs/" + str(job_id), token)
            artifact = fetch(repo, "actions/artifacts/" + str(artifact_id), token)
            expected_path = ".github/workflows/" + str(row.get("replacement_workflow", ""))
            checks = {
                "run_success": run.get("conclusion") == "success",
                "run_repository": isinstance(run.get("repository"), dict) and run["repository"].get("full_name") == repo,
                "run_event": run.get("event") in ("push", "pull_request", "workflow_dispatch", "schedule", "workflow_call"),
                "run_sha": run.get("head_sha") == row.get("source_sha"),
                "run_workflow": run.get("path", "").split("@", 1)[0] == expected_path,
                "job_run": job.get("run_id") == run_id,
                "job_workflow": job.get("workflow_name") in (None, run.get("name")),
                "job_id": job.get("id") == job_id,
                "artifact_id": artifact.get("id") == artifact_id,
                "job_success": job.get("conclusion") == "success",
                "artifact_run": artifact.get("workflow_run", {}).get("id") == run_id,
                "artifact_available": artifact.get("expired") is False and artifact.get("size_in_bytes", 0) > 0,
            }
            result["checks"] = checks
            result["errors"] = [key for key, ok in checks.items() if not ok]
            result["github_metadata_verified"] = all(checks.values())
        except (ValueError, KeyError, TypeError, AttributeError, urllib.error.URLError, TimeoutError) as exc:
            result["errors"].append(type(exc).__name__)
    return {"records": results, "github_metadata_verified_count": sum(r["github_metadata_verified"] for r in results),
            "independently_verified_behavior_count": 0, "production_ready": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    args = parser.parse_args()
    output = Path(args.output)
    if output.resolve() == Path(args.evidence).resolve():
        raise ValueError("Output must not overwrite evidence")
    report = probe(json.loads(Path(args.evidence).read_text(encoding="utf-8")),
                   args.repo, os.environ.get("GH_TOKEN", ""))
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "records"}))


if __name__ == "__main__":
    main()
