"""Utility for closing stale docs(sync) pull requests.

This script replicates the manual GitHub CLI workflow that closes every
`docs(sync)` pull request except for the most recently created one.  It relies
on the GitHub REST API so that it can run in environments where the GitHub CLI
is not available.

Usage:
    python scripts/close_stale_sync_prs.py <owner> <repo>

The script expects a ``GITHUB_TOKEN`` environment variable with permissions to
read pull requests, post comments, and close issues in the target repository.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Iterable, List, Optional


DOCS_SYNC_PATTERN = re.compile(r"^docs\(sync\)")


class GitHubClient:
    def __init__(self, owner: str, repo: str, token: str) -> None:
        self.owner = owner
        self.repo = repo
        self.token = token

    def _url(self, path: str) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repo}{path}"

    def iter_open_pull_requests(self) -> Iterable[dict]:
        page = 1
        while True:
            params = urllib.parse.urlencode({"state": "open", "per_page": 100, "page": page})
            response = self._request("GET", self._url("/pulls") + f"?{params}")
            data = json.loads(response)
            if not data:
                break
            for item in data:
                yield item
            page += 1

    def post_comment(self, number: int, body: str) -> None:
        self._request(
            "POST",
            self._url(f"/issues/{number}/comments"),
            data=json.dumps({"body": body}).encode(),
        )

    def close_pull_request(self, number: int) -> None:
        self._request(
            "PATCH",
            self._url(f"/issues/{number}"),
            data=json.dumps({"state": "closed"}).encode(),
        )

    def _request(self, method: str, url: str, data: Optional[bytes] = None) -> str:
        request = urllib.request.Request(url, data=data, method=method)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("Authorization", f"token {self.token}")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request) as response:
                return response.read().decode()
        except urllib.error.HTTPError as exc:  # pragma: no cover - convenience message
            message = exc.read().decode()
            raise RuntimeError(f"GitHub API request failed: {exc.code} {exc.reason}: {message}") from exc


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner", help="Repository owner")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not post comments or close pull requests; only log the actions that would be taken.",
    )
    return parser.parse_args(argv)


def iso_to_datetime(iso: str) -> dt.datetime:
    return dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN environment variable is required", file=sys.stderr)
        return 1

    client = GitHubClient(args.owner, args.repo, token)

    sync_prs = [pr for pr in client.iter_open_pull_requests() if DOCS_SYNC_PATTERN.search(pr["title"])]

    if not sync_prs:
        print("No open docs(sync) pull requests found.")
        return 0

    sync_prs.sort(key=lambda pr: iso_to_datetime(pr["created_at"]))
    newest = sync_prs[-1]
    newest_number = newest["number"]
    print(f"Newest sync PR: #{newest_number}")

    for pr in sync_prs:
        number = pr["number"]
        if number == newest_number:
            continue
        print(f"Closing superseded sync PR #{number}")
        if args.dry_run:
            continue
        body = f"Closing as superseded by newer sync PR #{newest_number}."
        client.post_comment(number, body)
        client.close_pull_request(number)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
