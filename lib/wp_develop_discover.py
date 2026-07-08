"""
Discover WordPress/wordpress-develop PRs that likely implement roadmap items.

For roadmap items that don't already have wp-develop PRs inlined from the
roadmap post, search wordpress-develop by a Claude-generated keyword query,
then use Claude to filter the candidates down to plausible matches.

Runs once during ``roadmap.refresh()``; results persist in the roadmap JSON,
so subsequent plain runs skip the work.
"""

from __future__ import annotations

import json
import os
import re
import subprocess

from anthropic import Anthropic
from dotenv import load_dotenv

from config import CLAUDE_MAX_TOKENS, CLAUDE_MODEL, WP_CYCLE_SEARCH_START_DATE

MAX_CANDIDATES_PER_ITEM = 15


def _gh_search(query: str, limit: int = MAX_CANDIDATES_PER_ITEM) -> list[dict]:
    """Run a GitHub search/issues query, return lightweight candidates."""
    result = subprocess.run(
        [
            "gh", "api", "-X", "GET", "search/issues",
            "-f", f"q={query}",
            "--jq", '.items[] | {number, title, url: .html_url, state}',
        ],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return []
    items: list[dict] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return items[:limit]


def _batch_generate_queries(items: list, client: Anthropic) -> dict[str, str]:
    """Ask Claude for a short search query per roadmap item."""
    labeled = [{"title": it.title, "summary": it.summary[:300]} for it in items]
    prompt = f"""For each WordPress roadmap item below, produce a short (2-4
word) GitHub search query that would find PRs implementing it in
WordPress/wordpress-develop. Prefer concrete nouns over verbs, and drop
generic filler words like 'improvements', 'update', 'polish', 'expansion',
'support'.

Return a JSON object mapping each item title verbatim to its query string.
If an item is clearly Gutenberg-only (block editor, site editor, dataviews,
theme.json, block library) and unlikely to have wp-develop PRs, use an empty
string as its query to skip it.

Items:
{json.dumps(labeled, indent=2)}

Return ONLY the JSON object, no prose. Example:
{{
  "Speculative loading performance update": "speculative loading eagerness",
  "On This Day dashboard widget": "on this day widget",
  "Tabs Block stabilization": ""
}}
"""
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", resp.content[0].text.strip(), flags=re.DOTALL)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("    ⚠️  wp-develop discovery: could not parse batch query JSON")
        return {}


def _filter_candidates(item, candidates: list[dict], client: Anthropic) -> list[int]:
    """Ask Claude which candidate PRs plausibly match the roadmap item."""
    if not candidates:
        return []
    brief = [
        {"number": c["number"], "title": c["title"], "state": c.get("state")}
        for c in candidates
    ]
    prompt = f"""Roadmap item from a WordPress core release cycle:

Title: {item.title}
Summary: {item.summary}

Candidate PRs from WordPress/wordpress-develop:
{json.dumps(brief, indent=2)}

Return a JSON array of PR numbers that plausibly implement, test, or
directly support this roadmap item. Include reasonable matches — the user
will review and prune false positives downstream, so a missed real match
costs more than an extra plausible one. Exclude candidates that clearly
belong to an unrelated feature.

Return ONLY a JSON array like [12345, 67890] — or [] if no match."""
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", resp.content[0].text.strip(), flags=re.DOTALL)
    try:
        parsed = json.loads(raw)
        return [int(n) for n in parsed] if isinstance(parsed, list) else []
    except (json.JSONDecodeError, ValueError, TypeError):
        return []


def discover(items: list, verbose: bool = True) -> None:
    """Mutate roadmap items in place, populating wp_develop_prs for empty ones."""
    empty = [it for it in items if not it.wp_develop_prs]
    if not empty:
        return

    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        if verbose:
            print("    ⚠️  ANTHROPIC_API_KEY not set; skipping wp-develop discovery")
        return
    client = Anthropic(api_key=api_key)

    if verbose:
        print(f"  Discovering wp-develop PRs for {len(empty)} item(s)…", flush=True)

    queries = _batch_generate_queries(empty, client)

    found = 0
    for item in empty:
        q = (queries.get(item.title) or "").strip()
        if not q:
            continue
        gh_query = (
            f"repo:WordPress/wordpress-develop is:pr {q} "
            f"created:>={WP_CYCLE_SEARCH_START_DATE}"
        )
        candidates = _gh_search(gh_query, limit=MAX_CANDIDATES_PER_ITEM)
        if not candidates:
            continue
        matched = _filter_candidates(item, candidates, client)
        if matched:
            item.wp_develop_prs = matched
            found += len(matched)
            if verbose:
                print(f"    🔎 {item.title}: {matched}", flush=True)

    if verbose:
        print(f"  wp-develop discovery: {found} PR(s) added across {len(empty)} item(s)")
