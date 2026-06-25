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
    """
    if not leftover_prs:
        _save([])
        return []

    prior = _load_prior()

    load_dotenv()
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    pr_brief = [
        {
            "number": pr["number"],
            "title": pr["title"],
            "version": pr["version"],
            "url": pr["url"],
        }
        for pr in leftover_prs
    ]

    prompt = f"""Group these shipped Gutenberg PRs into 5–12 feature clusters
for a WordPress release-cycle changelog.

PRIOR run's clusters (use as anchors — keep names stable, place new PRs into
existing clusters when they fit; create new clusters only when a PR doesn't fit):
{json.dumps(prior, indent=2) if prior else "[]"}

NEW set of PRs to cluster (this run):
{json.dumps(pr_brief, indent=2)}

Rules:
- Reuse the prior cluster TITLES verbatim when a new PR fits them.
- Create new clusters only for PRs that don't fit any existing cluster.
- Drop prior clusters whose PRs are all gone (none reappear this run).
- Each cluster: short title (3-7 words), one-sentence summary, and the list
  of PRs assigned to it. Every PR in the input MUST appear in exactly one
  cluster output — none get dropped.

Return ONLY a JSON array (no prose):
[
  {{
    "title": "Tabs Block polish",
    "summary": "Continued Tabs block refinements after the 7.0 stabilization.",
    "prs": [
      {{"number": 75890, "title": "...", "url": "...", "version": "v22.7.0"}}
    ]
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
    data = json.loads(raw)
    clusters = [_to_cluster(c) for c in data]
    _save(clusters)
    return clusters
