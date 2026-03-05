#!/usr/bin/env python3
"""
Request a review from the central PR service (no webhook).
Uses the same logic as the GitHub Actions workflow: POST /review?repo_id=<repo_id>
with diff, title, description. Run locally or in CI.

Usage:
  export REVIEW_SERVICE_URL=https://your-service.example.com
  export REPO_ID=owner/pr_system_test_project   # or leave unset to use GITHUB_REPOSITORY
  git diff main --no-color > pr.diff
  python scripts/request_review.py [pr.diff]

Requires: REVIEW_SERVICE_URL. Optional: REPO_ID (default from GITHUB_REPOSITORY), diff file (default pr.diff).
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def main() -> int:
    base_url = os.environ.get("REVIEW_SERVICE_URL", "").rstrip("/")
    repo_id = os.environ.get("REPO_ID") or os.environ.get("GITHUB_REPOSITORY", "")
    if not base_url:
        print("Set REVIEW_SERVICE_URL.", file=sys.stderr)
        return 1
    if not repo_id:
        print("Set REPO_ID or GITHUB_REPOSITORY (e.g. owner/pr_system_test_project).", file=sys.stderr)
        return 1

    diff_path = sys.argv[1] if len(sys.argv) > 1 else "pr.diff"
    if not os.path.isfile(diff_path):
        print(f"Diff file not found: {diff_path}", file=sys.stderr)
        return 1

    with open(diff_path, encoding="utf-8", errors="replace") as f:
        diff_text = f.read()

    url = f"{base_url}/review?repo_id={urllib.parse.quote(repo_id, safe='')}"
    payload = {
        "diff": diff_text,
        "title": os.environ.get("PR_TITLE", "PR"),
        "description": os.environ.get("PR_BODY", ""),
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        return 1

    print("## Summary")
    print(result.get("summary", ""))
    print("\n## Verdict")
    print(result.get("verdict", ""))
    print("\n## Comments")
    for c in result.get("comments", []):
        loc = c.get("path", "") + (f" (line {c.get('line')})" if c.get("line") is not None else "")
        print(f"  [{c.get('severity', '')}] {loc}")
        print(f"    {c.get('body', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
