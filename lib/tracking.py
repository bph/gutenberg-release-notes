"""
Resolve a roadmap tracking issue to its authoritative set of PR numbers.

Sources (unioned):
1. GitHub native sub-issues endpoint (introduced 2024 — gracefully degrades)
2. Issue timeline `cross-referenced` events with PR sources
3. `- [ ] #NNNNN` task-list refs parsed from the issue body
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from config import DATA_DIR, GITHUB_REPO
from lib import github_api


TRACKING_DIR = Path(DATA_DIR) / "tracking"

TASK_LIST_REF_RE = re.compile(r"-\s*\[[ x]\]\s*.*?#(\d+)", re.IGNORECASE)
PR_URL_RE = re.compile(r"https?://github\.com/[^/]+/[^/]+/pull/(\d+)")


@dataclass
class TrackingResolution:
    issue_number: int
    pr_numbers: list[int]
    title: str = ""
    url: str = ""


def _sub_issues(issue_n: int) -> set[int]:
    """Native sub-issues endpoint. Returns issue numbers that are PRs."""
    try:
        items = github_api.get(f"/repos/{GITHUB_REPO}/issues/{issue_n}/sub_issues")
    except Exception:
        return set()
    out: set[int] = set()
    if isinstance(items, list):
        for it in items:
            # Sub-issues may themselves be issues or PRs; filter to PRs by html_url
            url = it.get("html_url", "")
            m = PR_URL_RE.match(url)
            if m:
                out.add(int(m.group(1)))
            elif it.get("pull_request"):
                out.add(int(it["number"]))
    return out


def _timeline_cross_refs(issue_n: int) -> set[int]:
    """PRs that cross-referenced this issue (typically via 'Closes #N' or trackedBy)."""
    out: set[int] = set()
    page = 1
    while True:
        try:
            items = github_api.get(
                f"/repos/{GITHUB_REPO}/issues/{issue_n}/timeline",
                accept="application/vnd.github.mockingbird-preview+json",
                params={"per_page": 100, "page": page},
            )
        except Exception:
            break
        if not items:
            break
        for ev in items:
            if ev.get("event") != "cross-referenced":
                continue
            src = ev.get("source") or {}
            issue = src.get("issue") or {}
            if issue.get("pull_request"):
                out.add(int(issue["number"]))
        if len(items) < 100:
            break
        page += 1
    return out


def _fetch_issue(issue_n: int) -> dict:
    """Fetch the issue itself (for title + body)."""
    try:
        return github_api.get(f"/repos/{GITHUB_REPO}/issues/{issue_n}")
    except Exception:
        return {}


def _body_task_refs_from(issue_body: str) -> set[int]:
    return {int(m.group(1)) for m in TASK_LIST_REF_RE.finditer(issue_body or "")}


def resolve(issue_n: int, *, use_cache: bool = True) -> TrackingResolution:
    """Resolve and cache the PR set + metadata for a tracking issue."""
    TRACKING_DIR.mkdir(parents=True, exist_ok=True)
    cache = TRACKING_DIR / f"{issue_n}.json"
    if use_cache and cache.exists():
        data = json.loads(cache.read_text())
        return TrackingResolution(
            issue_number=issue_n,
            pr_numbers=data["pr_numbers"],
            title=data.get("title", ""),
            url=data.get("url", ""),
        )

    issue = _fetch_issue(issue_n)
    title = issue.get("title", "")
    url = issue.get("html_url", f"https://github.com/{GITHUB_REPO}/issues/{issue_n}")
    body = issue.get("body", "")

    prs = _sub_issues(issue_n) | _timeline_cross_refs(issue_n) | _body_task_refs_from(body)
    pr_numbers = sorted(prs)
    cache.write_text(json.dumps({
        "issue_number": issue_n,
        "pr_numbers": pr_numbers,
        "title": title,
        "url": url,
    }, indent=2))
    return TrackingResolution(
        issue_number=issue_n, pr_numbers=pr_numbers, title=title, url=url
    )
