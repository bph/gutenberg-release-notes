"""
Fetch and parse the WP cycle roadmap post into structured items.

Items: {title, summary, tracking_issue|None, confidence: high|medium|low}
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

import requests

from config import (
    CLAUDE_MAX_TOKENS,
    CLAUDE_MODEL,
    DATA_DIR,
    ROADMAP_URL,
    WP_CYCLE,
)
from lib import state


ROADMAP_JSON = Path(DATA_DIR) / f"roadmap_wp-{WP_CYCLE}.json"
ROADMAP_MD = Path(DATA_DIR) / f"roadmap_wp-{WP_CYCLE}.md"


@dataclass
class RoadmapItem:
    title: str
    summary: str
    tracking_issue: int | None
    confidence: str  # "high" | "medium" | "low"
    # WordPress/wordpress-develop PR numbers referenced from the roadmap post.
    # Optional / defaults to empty for backward-compat with older cached JSON.
    wp_develop_prs: list[int] = field(default_factory=list)


def fetch_html(url: str = ROADMAP_URL) -> str:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text


def _html_to_text(html: str) -> str:
    """Crude HTML → text. Keep links as 'text (url)' so issue refs survive."""
    # Replace anchor tags with "text (href)"
    html = re.sub(
        r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        r"\2 (\1)",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Block-level → newline
    html = re.sub(r"<(?:br|/p|/div|/li|/h\d|/section|/article)[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Strip remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Decode the few entities we care about
    for entity, char in (("&amp;", "&"), ("&nbsp;", " "), ("&#8217;", "'"), ("&#8211;", "—"), ("&lt;", "<"), ("&gt;", ">")):
        html = html.replace(entity, char)
    # Collapse whitespace
    lines = [ln.strip() for ln in html.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def _extract_article(html: str) -> str:
    """Pull the post body out of the WP page HTML."""
    # WordPress posts: <article> ... <div class="entry-content"> ... </div> ... </article>
    m = re.search(r'<div class="entry-content"[^>]*>(.*?)</div>\s*<footer', html, re.DOTALL | re.IGNORECASE)
    if not m:
        # Fallback: try just the article tag
        m = re.search(r"<article[^>]*>(.*?)</article>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    return html


def parse_with_claude(text: str) -> list[RoadmapItem]:
    """Ask Claude to structure the roadmap post."""
    from anthropic import Anthropic
    import os
    from dotenv import load_dotenv

    load_dotenv()
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""You are parsing a WordPress core roadmap blog post for the
audience of WordPress users and content editors (not core developers).

Extract every distinct feature or work-item the roadmap mentions. For each, return:
- title: short feature name (3-7 words), as users would recognize it
- summary: a 2-4 sentence paragraph that:
    1. Explains in plain language WHAT the feature is and how it shows up in the UI
       (avoid jargon like "block supports", "data layer" — translate to user-visible terms)
    2. Explains WHY it matters for users — what problem it solves, what new thing it
       enables, or how it improves the editing/site-building experience
  Pull details from the post where available; otherwise infer from the title and
  context. Keep the tone friendly and concrete.
- tracking_issue: GitHub issue number (integer, NO leading #) if the item links to
  a tracking issue in WordPress/gutenberg. Look for URLs like
  https://github.com/WordPress/gutenberg/issues/12345. Use null if none.
- wp_develop_prs: array of PR numbers (integers, NO leading #) referenced from
  WordPress/wordpress-develop. Look for URLs like
  https://github.com/WordPress/wordpress-develop/pull/12345. Empty array if none.
  Include EVERY wp-develop PR mentioned in the roadmap post, even if the item
  primarily lives in the Gutenberg plugin.
- confidence: "high" if the item is clearly a discrete feature with explicit title
  or link; "medium" if you had to interpret somewhat; "low" if you're guessing

Return ONLY a JSON array, no prose. Example:
[
  {{
    "title": "Tabs Block stabilization",
    "summary": "The Tabs block, which lets you split content into separately-clickable tabbed sections, graduates from experimental status to a stable, fully-supported core block. This cycle adds polish around keyboard navigation (arrow keys to move between tabs), color and typography controls per tab, and improved accessibility for screen readers. For editors, it means you can now confidently use tabs in published content without worrying about future breakage, and visitors get a more navigable, accessible experience.",
    "tracking_issue": 62345,
    "wp_develop_prs": [10123, 11501],
    "confidence": "high"
  }},
  ...
]

The post text:
---
{text}
---"""

    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    # Trim possible code fences
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL)
    data = json.loads(raw)
    items: list[RoadmapItem] = []
    for it in data:
        items.append(
            RoadmapItem(
                title=it["title"],
                summary=it.get("summary", ""),
                tracking_issue=it.get("tracking_issue"),
                confidence=it.get("confidence", "medium"),
                wp_develop_prs=[int(n) for n in (it.get("wp_develop_prs") or [])],
            )
        )
    return items


def _write_md(items: list[RoadmapItem]) -> None:
    lines = [f"# WP {WP_CYCLE} Roadmap (parsed)", ""]
    lines.append(f"_Source: {ROADMAP_URL}_")
    lines.append("")
    for it in items:
        marker = {"high": "", "medium": "", "low": " ⚠️"}.get(it.confidence, "")
        tracking = f" — tracking #{it.tracking_issue}" if it.tracking_issue else ""
        lines.append(f"## {it.title}{tracking}{marker}")
        lines.append(it.summary)
        lines.append("")
    ROADMAP_MD.parent.mkdir(parents=True, exist_ok=True)
    ROADMAP_MD.write_text("\n".join(lines))


def refresh() -> list[RoadmapItem]:
    """Fetch the roadmap post and re-parse it. Overwrites cached files."""
    print(f"  Fetching roadmap from {ROADMAP_URL}…")
    html = fetch_html()
    article = _extract_article(html)
    text = _html_to_text(article)
    items = parse_with_claude(text)

    ROADMAP_JSON.parent.mkdir(parents=True, exist_ok=True)
    ROADMAP_JSON.write_text(json.dumps([asdict(i) for i in items], indent=2))
    _write_md(items)

    s = state.load()
    s["roadmap_fetched_at"] = datetime.now(timezone.utc).isoformat()
    state.save(s)

    print(f"  Parsed {len(items)} roadmap items.")
    return items


def load() -> list[RoadmapItem]:
    """Load cached roadmap items; refresh if missing."""
    if not ROADMAP_JSON.exists():
        return refresh()
    data = json.loads(ROADMAP_JSON.read_text())
    return [RoadmapItem(**it) for it in data]
