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
for a WordPress release-cycle changelog.

PRIOR run's clusters (use as anchors — keep titles stable, place new PRs into
existing clusters when they fit; create new clusters only when a PR doesn't fit;
drop a prior cluster only if none of its PRs reappear in this run):
{json.dumps(prior_brief, indent=2)}

PRs to cluster (one per line, format `#number (version): title`):
{chr(10).join(pr_brief)}

Rules:
- Every PR number above MUST appear in exactly one cluster's `pr_numbers` array.
- Cluster title: 3-7 words; summary: one sentence.
- Reuse prior cluster titles verbatim when applicable.

Return ONLY a JSON array, nothing else:
[
  {{"title": "...", "summary": "...", "pr_numbers": [12345, 12346]}},
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
    seen: set[int] = set()
    for c in data:
        prs: list[ClusterPR] = []
        for n in c.get("pr_numbers", []):
            pr = by_number.get(int(n))
            if not pr or int(n) in seen:
                continue
            seen.add(int(n))
            prs.append(ClusterPR(
                number=pr["number"], title=pr["title"],
                url=pr["url"], version=pr["version"],
            ))
        if prs:
            clusters.append(Cluster(title=c["title"], summary=c.get("summary", ""), prs=prs))

    # Catch any PRs the LLM forgot to place
    missing = [pr for n, pr in by_number.items() if n not in seen]
    if missing:
        clusters.append(Cluster(
            title="Unclustered",
            summary="PRs the clusterer didn't assign to a feature group.",
            prs=[ClusterPR(
                number=pr["number"], title=pr["title"],
                url=pr["url"], version=pr["version"],
            ) for pr in missing],
        ))

    _save(clusters)
    return clusters
