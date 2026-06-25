"""
Cluster leftover (non-roadmap-matched) PRs into feature groups for the
"Additional shipped features" section.

Anchored on the prior run's clusters in `data/clusters_wp-<cycle>.json` so
cluster names stay stable across runs.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

from config import CLAUDE_MAX_TOKENS, CLAUDE_MODEL, DATA_DIR, WP_CYCLE


CLUSTERS_PATH = Path(DATA_DIR) / f"clusters_wp-{WP_CYCLE}.json"


@dataclass
class ClusterPR:
    number: int
    title: str
    url: str
    version: str


@dataclass
class Cluster:
    title: str
    summary: str
    prs: list[ClusterPR] = field(default_factory=list)


def _load_prior() -> list[dict]:
    if not CLUSTERS_PATH.exists():
        return []
    return json.loads(CLUSTERS_PATH.read_text())


def _save(clusters: list[Cluster]) -> None:
    CLUSTERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLUSTERS_PATH.write_text(
        json.dumps(
            [
                {
                    "title": c.title,
                    "summary": c.summary,
                    "prs": [asdict(p) for p in c.prs],
                }
                for c in clusters
            ],
            indent=2,
        )
    )


def _to_cluster(raw: dict) -> Cluster:
    return Cluster(
        title=raw["title"],
        summary=raw.get("summary", ""),
        prs=[ClusterPR(**p) for p in raw.get("prs", [])],
    )


def cluster_leftovers(leftover_prs: list[dict]) -> list[Cluster]:
    """
    Cluster PRs into feature groups, reusing prior cluster shape when possible.
    Returns the new full set of clusters, also persists to `clusters_wp-<cycle>.json`.

    Claude only emits PR numbers per cluster (small payload, hard to truncate).
    We reconstruct the full PR objects locally from `leftover_prs`.
    """
    if not leftover_prs:
        _save([])
        return []

    prior = _load_prior()
    by_number = {pr["number"]: pr for pr in leftover_prs}

    load_dotenv()
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Compact PR brief for the prompt
    pr_brief = [
        f"#{pr['number']} ({pr['version']}): {pr['title']}"
        for pr in leftover_prs
    ]

    prior_brief = (
        [
            {"title": c["title"], "pr_numbers": [p["number"] for p in c.get("prs", [])]}
            for c in prior
        ]
        if prior
        else []
    )

    prompt = f"""Group these shipped Gutenberg PRs into 5–15 feature clusters
for a WordPress release-cycle changelog aimed at WordPress users and content
editors (not core developers).

PRIOR run's clusters (use as anchors — keep titles stable, place new PRs into
existing clusters when they fit; create new clusters only when a PR doesn't fit;
drop a prior cluster only if none of its PRs reappear in this run):
{json.dumps(prior_brief, indent=2)}

PRs to cluster (one per line, format `#number (version): title`):
{chr(10).join(pr_brief)}

Rules:
- Every PR number above MUST appear in exactly one cluster's `pr_numbers` array.
- Reuse prior cluster titles verbatim when applicable.
- Cluster `title`: 3-7 words, recognizable to users.
- Cluster TITLES must be specific, descriptive feature areas. DO NOT use generic
  catch-alls like "Miscellaneous", "Other", "Unclustered", "Misc Improvements",
  "Various Changes" etc. If a few PRs don't fit anywhere, put them in the
  closest reasonable cluster or create a small, specifically-named cluster
  (e.g. "Storybook configuration", not "Misc tooling").
- Cluster `summary`: a 2-4 sentence paragraph that:
    1. Explains WHAT the cluster of PRs adds or improves, in plain language users
       would recognize. Avoid developer jargon — say "list view" not "List View
       store actions", "block toolbar" not "BlockControls slot."
    2. Explains WHY it matters — what becomes easier, faster, more reliable, or
       newly possible for someone editing a site.
  If the PRs share a clear theme, name it. If they're a grab-bag of polish in one
  area, say that honestly.

Return ONLY a JSON array, nothing else:
[
  {{
    "title": "Tabs Block polish",
    "summary": "Continued refinements to the Tabs block following its stabilization in 7.0. This batch adds vertical orientation as a layout option, lets you set distinct colors per tab, and tightens up keyboard navigation so screen-reader and keyboard-only users can move between tabs cleanly. For editors, it means the Tabs block is more flexible visually and more accessible by default.",
    "pr_numbers": [76055, 76087, 76101]
  }},
  ...
]"""

    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        debug_path = CLUSTERS_PATH.parent / f"clusters_wp-{WP_CYCLE}.raw.txt"
        debug_path.write_text(raw)
        print(f"  ⚠️  Cluster JSON parse failed: {e}; raw saved to {debug_path}")
        raise

    clusters: list[Cluster] = []
    by_title: dict[str, Cluster] = {}
    seen: set[int] = set()
    for c in data:
        title = c["title"].strip()
        summary = c.get("summary", "")
        cluster = by_title.get(title)
        if cluster is None:
            cluster = Cluster(title=title, summary=summary, prs=[])
            by_title[title] = cluster
            clusters.append(cluster)
        elif summary and not cluster.summary:
            cluster.summary = summary
        for n in c.get("pr_numbers", []):
            pr = by_number.get(int(n))
            if not pr or int(n) in seen:
                continue
            seen.add(int(n))
            cluster.prs.append(ClusterPR(
                number=pr["number"], title=pr["title"],
                url=pr["url"], version=pr["version"],
            ))

    # Catch any PRs the LLM forgot to place — fold into the catch-all bucket
    # if one already exists, otherwise create it.
    missing = [pr for n, pr in by_number.items() if n not in seen]
    if missing:
        catchall_title = "Other shipped improvements"
        cluster = by_title.get(catchall_title)
        if cluster is None:
            cluster = Cluster(
                title=catchall_title,
                summary="PRs that didn't fit any of the named feature clusters.",
                prs=[],
            )
            by_title[catchall_title] = cluster
            clusters.append(cluster)
        for pr in missing:
            cluster.prs.append(ClusterPR(
                number=pr["number"], title=pr["title"],
                url=pr["url"], version=pr["version"],
            ))

    # Drop empty clusters that may have been carried over from prior cache
    clusters = [c for c in clusters if c.prs]

    _save(clusters)
    return clusters
