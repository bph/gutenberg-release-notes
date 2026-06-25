"""
Render the punch-list:

1. As markdown → `punchlist/wp-<cycle>.md` (local mirror / debug artifact)
2. As text for the Backlog tab — gdoc handles the actual Docs API write

Per-roadmap-item status:
- ⏳ pending:     0 matched PRs
- 🚧 shipped:     >0 PRs, none covered
- 🟡 partial:     some covered, some not
- ✅ done:        all matched PRs covered

Per-PR markers:
- ✅ if PR number is in covered set (Draft wip ∪ Handled)
- 🔲 otherwise
- 🆕 added inline if PR is new since last run
- ⚠️ added inline if fuzzy match confidence is low
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from config import (
    PUNCHLIST_DIR,
    ROADMAP_URL,
    SOT_DOC_ID,
    WP_CYCLE,
)
from lib.cluster import Cluster
from lib.match import MatchedPR, MatchedRoadmapItem, MatchResult


PUNCHLIST_PATH = Path(PUNCHLIST_DIR) / f"wp-{WP_CYCLE}.md"


def _item_status(item: MatchedRoadmapItem, covered: set[int]) -> str:
    if not item.matched_prs:
        return "⏳"
    covered_count = sum(1 for p in item.matched_prs if p.number in covered)
    if covered_count == 0:
        return "🚧"
    if covered_count == len(item.matched_prs):
        return "✅"
    return "🟡"


def _pr_line(pr: MatchedPR | dict, covered: set[int], new_prs: set[int]) -> str:
    if isinstance(pr, MatchedPR):
        number = pr.number
        title = pr.title
        url = pr.url
        version = pr.version
        warn = " ⚠️" if pr.source == "fuzzy" and pr.confidence == "low" else ""
    else:
        number = pr["number"]
        title = pr["title"]
        url = pr["url"]
        version = pr["version"]
        warn = ""
    mark = "✅" if number in covered else "🔲"
    new = " 🆕" if number in new_prs else ""
    return f"- {mark} {title} [#{number}]({url}) _{version}_{warn}{new}"


def render_markdown(
    result: MatchResult,
    clusters: list[Cluster],
    covered: set[int],
    new_prs: set[int],
    versions_covered: list[str],
) -> str:
    lines: list[str] = []
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    doc_url = f"https://docs.google.com/document/d/{SOT_DOC_ID}/edit"

    lines.append(f"# WP {WP_CYCLE} SOT Backlog")
    lines.append("")
    lines.append(f"_Last updated: {updated}_")
    lines.append(f"_Roadmap: [Roadmap to {WP_CYCLE}]({ROADMAP_URL})_")
    lines.append(f"_Source of Truth doc: [open]({doc_url})_")
    if versions_covered:
        lines.append(f"_Versions covered: {versions_covered[0]} – {versions_covered[-1]}_")
    lines.append("_⏳ pending · 🚧 shipped, not in draft · 🟡 partial · ✅ done · 🔲 PR not yet cited · 🆕 new this run · ⚠️ low-confidence match_")
    lines.append("")

    # ---- Roadmap items ----
    lines.append("## Roadmap items")
    lines.append("")
    if not result.items:
        lines.append("_No roadmap items parsed yet._")
        lines.append("")
    else:
        # Sort: items with matches first, then pending
        ordered = sorted(
            result.items,
            key=lambda it: (0 if it.matched_prs else 1, it.title.lower()),
        )
        for item in ordered:
            status = _item_status(item, covered)
            lines.append(f"### {status} {item.title}")
            if item.summary:
                lines.append(item.summary)
            if item.tracking_issue:
                label = item.tracking_title or f"Tracking issue #{item.tracking_issue}"
                url = item.tracking_url or f"https://github.com/WordPress/gutenberg/issues/{item.tracking_issue}"
                lines.append(f"Tracking: [{label}]({url}) (#{item.tracking_issue})")
            lines.append("")
            for pr in item.matched_prs:
                lines.append(_pr_line(pr, covered, new_prs))
            lines.append("")

    # ---- Additional features (clusters from leftovers) ----
    lines.append("## Additional shipped features")
    lines.append("_(PRs not tied to a roadmap item)_")
    lines.append("")
    if not clusters:
        lines.append("_None._")
        lines.append("")
    else:
        for c in clusters:
            lines.append(f"### {c.title}")
            if c.summary:
                lines.append(c.summary)
            lines.append("")
            for p in c.prs:
                lines.append(_pr_line(
                    {"number": p.number, "title": p.title, "url": p.url, "version": p.version},
                    covered, new_prs,
                ))
            lines.append("")

    # ---- Summary ----
    total_roadmap_prs = sum(len(it.matched_prs) for it in result.items)
    covered_roadmap = sum(1 for it in result.items for p in it.matched_prs if p.number in covered)
    cluster_prs = sum(len(c.prs) for c in clusters)
    covered_cluster = sum(1 for c in clusters for p in c.prs if p.number in covered)
    todo = (total_roadmap_prs - covered_roadmap) + (cluster_prs - covered_cluster)

    done_items = sum(1 for it in result.items if _item_status(it, covered) == "✅")
    partial = sum(1 for it in result.items if _item_status(it, covered) == "🟡")
    shipped_not = sum(1 for it in result.items if _item_status(it, covered) == "🚧")
    pending = sum(1 for it in result.items if _item_status(it, covered) == "⏳")

    lines.append("---")
    lines.append(
        f"**Summary:** {len(result.items)} roadmap items "
        f"({done_items} done · {partial} partial · {shipped_not} shipped not written · {pending} pending) "
        f"· {len(clusters)} additional clusters · **{todo} PR{'s' if todo != 1 else ''} still to cite**"
    )
    lines.append("")
    return "\n".join(lines)


def write_local_mirror(body: str) -> Path:
    PUNCHLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUNCHLIST_PATH.write_text(body)
    return PUNCHLIST_PATH
