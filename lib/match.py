"""
Match shipped PRs to roadmap items.

Tier 1: deterministic via tracking-issue resolution.
Tier 2: Claude fuzzy matching for roadmap items without a tracking issue.
        Low-confidence matches are flagged AND remain visible in the leftover
        bucket (so wrong matches stay discoverable).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict, field

from dotenv import load_dotenv
from anthropic import Anthropic

from config import CLAUDE_MAX_TOKENS, CLAUDE_MODEL
from lib import tracking
from lib.roadmap import RoadmapItem


@dataclass
class MatchedPR:
    number: int
    title: str
    url: str
    version: str
    source: str          # "tracking" | "fuzzy"
    confidence: str | None = None  # only set for fuzzy: "high"|"medium"|"low"


@dataclass
class MatchedRoadmapItem:
    title: str
    summary: str
    tracking_issue: int | None
    tracking_title: str = ""
    tracking_url: str = ""
    matched_prs: list[MatchedPR] = field(default_factory=list)


@dataclass
class MatchResult:
    items: list[MatchedRoadmapItem]
    leftover_prs: list[dict]  # PRs not assigned to any roadmap item


def _pr_brief(pr: dict, version: str) -> dict:
    return {
        "number": pr["number"],
        "title": pr["title"],
        "url": pr["url"],
        "version": version,
    }


def match(
    roadmap: list[RoadmapItem],
    shipped_prs_by_version: dict[str, list[dict]],
) -> MatchResult:
    """
    `shipped_prs_by_version`: {"v22.7.0": [{number,title,url,...}, ...], ...}
    Only PRs marked `included=True` (post-backport-filter) should be passed in.
    """
    # Flatten to {pr_number: pr_dict with version}
    all_prs: dict[int, dict] = {}
    for version, prs in shipped_prs_by_version.items():
        for pr in prs:
            all_prs[pr["number"]] = {**pr, "version": version}

    items: list[MatchedRoadmapItem] = []
    assigned: set[int] = set()

    # Tier 1: tracking-issue resolution
    for ri in roadmap:
        m = MatchedRoadmapItem(
            title=ri.title,
            summary=ri.summary,
            tracking_issue=ri.tracking_issue,
        )
        if ri.tracking_issue:
            tr = tracking.resolve(ri.tracking_issue, use_cache=False)
            m.tracking_title = tr.title
            m.tracking_url = tr.url
            tracked = set(tr.pr_numbers)
            for n in tracked:
                if n in all_prs and n not in assigned:
                    pr = all_prs[n]
                    m.matched_prs.append(
                        MatchedPR(
                            number=n,
                            title=pr["title"],
                            url=pr["url"],
                            version=pr["version"],
                            source="tracking",
                        )
                    )
                    assigned.add(n)
        items.append(m)

    # Tier 2: Claude fuzzy matching against ALL roadmap items (not just those
    # without a tracking issue). This lets a roadmap item with a tracking issue
    # also absorb related PRs that the tracking issue didn't explicitly list —
    # avoiding the "DataViews roadmap item is empty while a DataViews cluster
    # sits in Additional features" duplication.
    unassigned = [pr for n, pr in all_prs.items() if n not in assigned]

    if items and unassigned:
        fuzzy = _fuzzy_match_with_claude(items, unassigned)
        for assignment in fuzzy:
            n = assignment["pr_number"]
            title = assignment["roadmap_title"]
            conf = assignment.get("confidence", "low")
            target = next((m for m in items if m.title == title), None)
            if not target or n not in all_prs:
                continue
            if n in assigned:
                continue
            pr = all_prs[n]
            target.matched_prs.append(
                MatchedPR(
                    number=n,
                    title=pr["title"],
                    url=pr["url"],
                    version=pr["version"],
                    source="fuzzy",
                    confidence=conf,
                )
            )
            # High/medium confidence claim the PR exclusively; low keeps it visible in leftovers too
            if conf in ("high", "medium"):
                assigned.add(n)

    leftover_prs = [pr for n, pr in all_prs.items() if n not in assigned]
    return MatchResult(items=items, leftover_prs=leftover_prs)


def _fuzzy_match_with_claude(
    items: list[MatchedRoadmapItem],
    unassigned: list[dict],
) -> list[dict]:
    load_dotenv()
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    roadmap_brief = [
        {
            "title": it.title,
            "summary": it.summary,
            "already_assigned_pr_count": len(it.matched_prs),
        }
        for it in items
    ]
    pr_brief = [{"number": pr["number"], "title": pr["title"]} for pr in unassigned]

    prompt = f"""Match shipped Gutenberg PRs to WordPress roadmap items.

Roadmap items (some already have PRs from their tracking issues — you can add
MORE PRs to any of them if a leftover clearly belongs to that area):
{json.dumps(roadmap_brief, indent=2)}

Leftover PRs (not yet assigned to any roadmap item):
{json.dumps(pr_brief, indent=2)}

For each PR that clearly belongs to one of the roadmap items, return an assignment.
A roadmap item like "DataViews and DataForms improvements" SHOULD absorb related
DataViews/DataForms PRs even if the tracking issue didn't explicitly list them.

PRs that don't fit ANY roadmap item should be omitted — they will appear
under "Additional shipped features" instead.

Confidence:
- "high": PR title/topic unambiguously matches the roadmap item
- "medium": plausible match, some interpretation involved
- "low": speculative match — only assert this if you think it's worth flagging

Return ONLY a JSON array, no prose:
[
  {{"pr_number": 12345, "roadmap_title": "Tabs Block polish", "confidence": "high"}},
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
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"  ⚠️  Could not parse fuzzy-match JSON; raw output:\n{raw[:500]}")
        return []


def to_jsonable(result: MatchResult) -> dict:
    return {
        "items": [
            {
                **asdict(m),
                "matched_prs": [asdict(p) for p in m.matched_prs],
            }
            for m in result.items
        ],
        "leftover_prs": result.leftover_prs,
    }
