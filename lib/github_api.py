"""
Thin wrapper around the GitHub REST API with `gh` CLI auth fallback.

We use `gh` for authentication (the user already has `gh auth login` set up).
Token is read once from `GH_TOKEN` env var or `gh auth token`.
"""

from __future__ import annotations

import os
import subprocess
import time
from functools import lru_cache

import requests


GITHUB_API = "https://api.github.com"


@lru_cache(maxsize=1)
def _token() -> str | None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        out = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        return out.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def _headers(accept: str = "application/vnd.github+json") -> dict:
    h = {
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    t = _token()
    if t:
        h["Authorization"] = f"Bearer {t}"
    return h


def get(path: str, *, accept: str = "application/vnd.github+json", params: dict | None = None) -> dict | list:
    """GET an arbitrary GitHub API path with auth + simple rate-limit backoff."""
    url = f"{GITHUB_API}{path}" if path.startswith("/") else path
    for attempt in range(3):
        r = requests.get(url, headers=_headers(accept), params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = int(r.headers.get("X-RateLimit-Reset", "0"))
            wait = max(1, reset - int(time.time()))
            print(f"  ⚠️  rate-limited; sleeping {wait}s before retry")
            time.sleep(min(wait, 60))
            continue
        if r.status_code == 404:
            raise FileNotFoundError(f"GitHub 404 for {url}")
        r.raise_for_status()
    r.raise_for_status()
    return {}  # unreachable
