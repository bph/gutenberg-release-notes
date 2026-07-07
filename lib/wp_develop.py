"""
Fetch and cache WordPress/wordpress-develop PR metadata, including any
core.trac.wordpress.org ticket numbers referenced in the PR body.

Cache: data/wp_develop/<pr_number>.json
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, asdict, field
from pathlib import Path

from config import DATA_DIR


WP_DEVELOP_CACHE_DIR = Path(DATA_DIR) / "wp_develop"

# Trac ticket refs. Supports:
#   https://core.trac.wordpress.org/ticket/12345
#   [12345] Trac-style bracket refs (rare in modern PR bodies)
TRAC_URL_RE = re.compile(r"core\.trac\.wordpress\.org/ticket/(\d{3,6})", re.IGNORECASE)
# "#12345" plain hash refs — only accept 5+ digit numbers to avoid picking up
# arbitrary PR/issue refs. Trac ticket numbers are 5-6 digits (currently ~64k+).
TRAC_HASH_RE = re.compile(r"(?<![A-Za-z0-9/])#(\d{5,6})(?!\d)")


@dataclass
class WpDevelopRef:
    number: int
    title: str
    url: str
    state: str  # "OPEN" | "CLOSED" | "MERGED"
    trac_tickets: list[int] = field(default_factory=list)


def _cache_path(number: int) -> Path:
    return WP_DEVELOP_CACHE_DIR / f"{number}.json"


def _extract_trac_tickets(body: str) -> list[int]:
    seen: set[int] = set()
    for m in TRAC_URL_RE.finditer(body or ""):
        seen.add(int(m.group(1)))
    # Hash refs alone are ambiguous; only accept them if the PR body also
    # mentions "trac" somewhere, to reduce false positives from PR/issue refs.
    if body and re.search(r"\btrac\b", body, re.IGNORECASE):
        for m in TRAC_HASH_RE.finditer(body):
            seen.add(int(m.group(1)))
    return sorted(seen)


def _fetch_via_gh(number: int) -> dict:
    """Return {number, title, url, state, body} for a wp-develop PR via gh."""
    result = subprocess.run(
        [
            "gh", "pr", "view", str(number),
            "--repo", "WordPress/wordpress-develop",
            "--json", "number,title,url,state,body",
        ],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def fetch(number: int, *, use_cache: bool = True) -> WpDevelopRef:
    """Return a WpDevelopRef for a wp-develop PR, using disk cache when present."""
    cache = _cache_path(number)
    if use_cache and cache.exists():
        data = json.loads(cache.read_text())
        return WpDevelopRef(**data)

    raw = _fetch_via_gh(number)
    ref = WpDevelopRef(
        number=raw["number"],
        title=raw["title"],
        url=raw["url"],
        state=raw.get("state", ""),
        trac_tickets=_extract_trac_tickets(raw.get("body", "")),
    )
    WP_DEVELOP_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(asdict(ref), indent=2))
    return ref


def fetch_many(numbers: list[int], *, use_cache: bool = True) -> list[WpDevelopRef]:
    refs: list[WpDevelopRef] = []
    for n in numbers:
        try:
            refs.append(fetch(n, use_cache=use_cache))
        except subprocess.CalledProcessError as e:
            print(f"    ⚠️  could not fetch wp-develop PR #{n}: {e.stderr.strip()[:200]}")
    return refs
