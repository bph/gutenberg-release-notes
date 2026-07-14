"""
Pending-milestone Gutenberg PRs treated as a pseudo-release.

When a Gutenberg version has merged PRs but hasn't been published yet, we
still want its work to show up in the punchlist so nothing gets missed
before the WP feature-freeze deadline. We fetch merged PRs by GitHub
milestone name, filter them to a user-facing subset (labels + title
keywords), apply the same phase-aware backport filter used for real
releases, and cache the result as if it were a normal cached release.

Cache shape mirrors `github_releases.CachedRelease` — same
`data/versions/<version>.json` layout — plus a top-level `"pending": true`.
Because pending PRs move milestones and get merged/reverted, the cache
carries a short TTL (6h) and can be force-refreshed via `--refresh-pending`.
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from config import (
    DATA_DIR,
    PENDING_PACKAGE_REJECT,
    PENDING_TYPE_ALLOW,
    PENDING_TYPE_REJECT,
)
from lib import github_api
from lib.github_releases import CachedRelease, _backport_filter
from lib.parse import _is_user_facing


VERSIONS_DIR = Path(DATA_DIR) / "versions"
CACHE_TTL_SECONDS = 6 * 60 * 60  # 6 hours


def _cache_path(version: str) -> Path:
    return VERSIONS_DIR / f"{version}.json"


def _cache_fresh(path: Path) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < CACHE_TTL_SECONDS


def _search_milestone_prs(milestone: str) -> list[dict]:
    """Return PR numbers + titles + URLs for merged PRs in the milestone.

    Uses `gh api search/issues` — same data source as the Gutenberg
    `npm run other:changelog -- --milestone=...` command.
    """
    query = (
        f'repo:WordPress/gutenberg is:pr is:merged milestone:"{milestone}"'
    )
    result = subprocess.run(
        [
            "gh", "api", "-X", "GET", "search/issues",
            "-f", f"q={query}",
            "--paginate",
            "--jq", '.items[] | {number, title, url: .html_url}',
        ],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh search failed for milestone {milestone!r}: {result.stderr.strip()}"
        )
    prs: list[dict] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            prs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return prs


def _fetch_labels(number: int) -> list[str]:
    data = github_api.get(f"/repos/WordPress/gutenberg/pulls/{number}")
    return [lbl["name"] for lbl in data.get("labels", [])]


def _label_filter(labels: list[str]) -> tuple[bool, str | None]:
    """Approximate the changelog Enhancements filter using PR labels + title.

    Returns (kept, excluded_reason).
    """
    type_labels = [l for l in labels if l.startswith("[Type]")]
    allow_hit = any(l in PENDING_TYPE_ALLOW for l in type_labels)
    reject_hit = any(l in PENDING_TYPE_REJECT for l in type_labels)

    if allow_hit:
        return True, None

    if type_labels and reject_hit:
        return False, f"dev-only [Type] label(s): {', '.join(type_labels)}"

    # No decisive [Type] label — fall back to package-label rejection.
    pkg_reject = [l for l in labels if l in PENDING_PACKAGE_REJECT]
    if pkg_reject and not any(l.startswith("[Type]") for l in labels):
        return False, f"dev-only [Package] label(s): {', '.join(pkg_reject)}"

    return True, None


def _title_filter(title: str) -> tuple[bool, str | None]:
    if _is_user_facing(title):
        return True, None
    return False, "title matched developer keyword"


def _refresh_from_gh(milestone: str, version: str) -> CachedRelease:
    print(f"  Fetching pending milestone {milestone!r} via gh search…", flush=True)
    raw = _search_milestone_prs(milestone)
    print(f"    {len(raw)} PR(s) carry the milestone")

    # Strip the "-pending" suffix so backport phase detection works on
    # the underlying version number (e.g. v23.6.0), not the tag literal.
    real_version = version.split("-", 1)[0]

    prs: list[dict] = []
    kept = 0
    dropped_label = 0
    dropped_title = 0
    dropped_backport = 0

    for i, item in enumerate(raw, start=1):
        number = item["number"]
        title = item["title"]
        url = item["url"]

        try:
            labels = _fetch_labels(number)
        except FileNotFoundError:
            print(f"    ⚠️  PR #{number} not found, skipping")
            continue

        included, reason = _label_filter(labels)
        if included:
            included, reason = _title_filter(title)
            if not included:
                dropped_title += 1
        else:
            dropped_label += 1

        if included:
            bp_included, bp_reason = _backport_filter(real_version, labels)
            if not bp_included:
                included = False
                reason = bp_reason
                dropped_backport += 1

        if included:
            kept += 1

        prs.append({
            "number": number,
            "title": title,
            "url": url,
            "labels": labels,
            "subsection": "",
            "text": title,
            "included": included,
            "excluded_reason": reason,
        })

        if i % 25 == 0:
            print(f"    …{i}/{len(raw)} processed", flush=True)

    print(
        f"    kept {kept}; dropped {dropped_label} by label, "
        f"{dropped_title} by title, {dropped_backport} by backport filter"
    )

    payload = {
        "version": version,
        "tag": version,
        "published_at": "",
        "prerelease": False,
        "pending": True,
        "milestone": milestone,
        "fetched_at": int(time.time()),
        "prs": prs,
    }
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    _cache_path(version).write_text(json.dumps(payload, indent=2, sort_keys=True))

    return CachedRelease(version=version, published_at="", prs=prs)


def ensure_pending(
    milestone: str,
    version: str,
    *,
    force_refresh: bool = False,
) -> CachedRelease:
    """Return the pending-milestone pseudo-release, using the cache when fresh."""
    path = _cache_path(version)
    if not force_refresh and _cache_fresh(path):
        data = json.loads(path.read_text())
        return CachedRelease(
            version=data["version"],
            published_at=data.get("published_at", ""),
            prs=data["prs"],
        )
    return _refresh_from_gh(milestone, version)
