"""
Discover Gutenberg plugin releases in the current WP cycle and extract
user-facing enhancement PRs, with PR-label resolution and a phase-aware
backport filter.

Cache shape — `data/versions/v22.X.0.json`:

    {
      "version": "v22.7.0",
      "tag": "v22.7.0",
      "published_at": "2026-06-15T...",
      "prerelease": false,
      "prs": [
        {"number": 75890, "title": "...", "url": "...",
         "labels": ["..."], "subsection": "Block Editor",
         "text": "Original bullet text", "included": true,
         "excluded_reason": null}
      ]
    }

`included` reflects the phase-aware backport rule:
- Pre-Beta-1: include non-backport, exclude backport
- Post-Beta-1 (release tag >= BETA_1): include backport, exclude non-backport
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config import (
    BACKPORT_LABEL,
    DATA_DIR,
    GITHUB_REPO,
    WP_CYCLE_BETA_1_VERSION,
    WP_CYCLE_END_VERSION,
    WP_CYCLE_START_VERSION,
)
from lib import github_api
from lib.parse import parse_enhancements


VERSIONS_DIR = Path(DATA_DIR) / "versions"


def _parse_tag(tag: str) -> tuple[int, ...]:
    """v22.7.0 → (22, 7, 0). Returns (0,) on parse failure."""
    s = tag.lstrip("v")
    try:
        return tuple(int(p) for p in s.split("."))
    except ValueError:
        return (0,)


def _in_cycle(tag: str) -> bool:
    t = _parse_tag(tag)
    if t < _parse_tag(WP_CYCLE_START_VERSION):
        return False
    if WP_CYCLE_END_VERSION and t > _parse_tag(WP_CYCLE_END_VERSION):
        return False
    return True


def _is_post_beta_1(tag: str) -> bool:
    if not WP_CYCLE_BETA_1_VERSION:
        return False
    return _parse_tag(tag) >= _parse_tag(WP_CYCLE_BETA_1_VERSION)


def _backport_filter(tag: str, labels: list[str]) -> tuple[bool, str | None]:
    """Return (included, excluded_reason)."""
    has_backport = BACKPORT_LABEL in labels
    if _is_post_beta_1(tag):
        if has_backport:
            return True, None
        return False, "post-Beta-1 non-backport (heading to next WP cycle)"
    else:
        if has_backport:
            return False, "pre-Beta-1 backport (shipped via previous WP cycle)"
        return True, None


@dataclass
class CachedRelease:
    version: str
    published_at: str
    prs: list[dict]

    def included_prs(self) -> list[dict]:
        return [p for p in self.prs if p.get("included")]


def list_cycle_releases() -> list[dict]:
    """List all GB releases (raw JSON) whose tag belongs to this cycle, newest first.

    Skips prereleases (RCs).
    """
    page = 1
    out: list[dict] = []
    while True:
        items = github_api.get(
            f"/repos/{GITHUB_REPO}/releases",
            params={"per_page": 100, "page": page},
        )
        if not items:
            break
        out.extend(items)
        if len(items) < 100:
            break
        page += 1
        # Early stop: if all items on this page are older than START, no need to keep paging
        start = _parse_tag(WP_CYCLE_START_VERSION)
        if all(_parse_tag(r["tag_name"]) < start for r in items):
            break

    return [
        r for r in out
        if _in_cycle(r["tag_name"]) and not r.get("prerelease")
    ]


def _cache_path(tag: str) -> Path:
    return VERSIONS_DIR / f"{tag}.json"


def _fetch_pr(number: int) -> dict:
    data = github_api.get(f"/repos/{GITHUB_REPO}/pulls/{number}")
    labels = [lbl["name"] for lbl in data.get("labels", [])]
    return {
        "number": number,
        "title": data.get("title", ""),
        "url": data.get("html_url", ""),
        "labels": labels,
    }


def fetch_and_cache(release: dict) -> CachedRelease:
    """Fetch + cache one release's user-facing PRs with labels."""
    tag = release["tag_name"]
    cache = _cache_path(tag)
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

    enhancements = parse_enhancements(release.get("body", ""))

    # Collect unique PR numbers from enhancements (paired with bullet context)
    pr_to_context: dict[int, dict] = {}
    for e in enhancements:
        for n in e.pr_numbers:
            # Keep the first context we see (PRs occasionally appear in multiple bullets)
            pr_to_context.setdefault(n, {"subsection": e.subsection, "text": e.text})

    prs: list[dict] = []
    print(f"  Fetching {len(pr_to_context)} PR(s) for {tag}…")
    for number, ctx in pr_to_context.items():
        try:
            pr = _fetch_pr(number)
        except FileNotFoundError:
            print(f"    ⚠️  PR #{number} not found, skipping")
            continue
        included, reason = _backport_filter(tag, pr["labels"])
        pr.update(
            subsection=ctx["subsection"],
            text=ctx["text"],
            included=included,
            excluded_reason=reason,
        )
        prs.append(pr)

    payload = {
        "version": tag,
        "tag": tag,
        "published_at": release.get("published_at", ""),
        "prerelease": release.get("prerelease", False),
        "prs": prs,
    }
    cache.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return CachedRelease(version=tag, published_at=payload["published_at"], prs=prs)


def load_cached(tag: str) -> CachedRelease | None:
    p = _cache_path(tag)
    if not p.exists():
        return None
    data = json.loads(p.read_text())
    return CachedRelease(version=data["version"], published_at=data["published_at"], prs=data["prs"])


def ensure_cached(release: dict, *, force_refresh: bool = False) -> CachedRelease:
    """Return cached release; fetch if missing or `force_refresh`."""
    tag = release["tag_name"]
    if not force_refresh:
        cached = load_cached(tag)
        if cached is not None:
            return cached
    return fetch_and_cache(release)
