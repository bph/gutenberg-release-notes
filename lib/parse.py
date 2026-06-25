"""
Parse GitHub release bodies and free text for Gutenberg user-facing enhancements.

Extracted from the original gutenberg_release_notes.py with no behavior change
beyond returning richer per-bullet records (text + PR numbers + subsection).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from config import DEVELOPER_KEYWORDS, DEVELOPER_SUBSECTIONS


# PR numbers appear as `#NNNNN` (in prose) or as bare numbers inside
# Markdown link references like `[NNNNN](https://github.com/.../pull/NNNNN)`.
# We capture both, but only accept link-style numbers that point at a PR URL.
PR_HASH_RE = re.compile(r"#(\d+)")
PR_LINK_RE = re.compile(r"\[(\d+)\]\(https?://github\.com/[^/]+/[^/]+/pull/(\d+)\)")


@dataclass
class Enhancement:
    text: str
    subsection: str | None
    pr_numbers: list[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "subsection": self.subsection,
            "pr_numbers": self.pr_numbers,
        }


def extract_pr_numbers(text: str) -> list[int]:
    """Return all PR numbers in declaration order, de-duplicated.

    Recognizes `#NNNNN` in prose and `[NNNNN](https://.../pull/NNNNN)` link refs.
    """
    seen: set[int] = set()
    out: list[int] = []
    for m in PR_LINK_RE.finditer(text):
        n = int(m.group(2))  # Use the URL number; it's authoritative
        if n not in seen:
            seen.add(n)
            out.append(n)
    for m in PR_HASH_RE.finditer(text):
        n = int(m.group(1))
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def _is_user_facing(text: str) -> bool:
    lower = text.lower()
    return not any(kw in lower for kw in DEVELOPER_KEYWORDS)


def parse_enhancements(release_body: str) -> list[Enhancement]:
    """
    Extract user-facing enhancement bullets from a release body.

    Filters out developer-only subsections (Data Layer, Code Quality, etc.)
    and developer-keyword bullets.
    """
    body = release_body.replace("\r\n", "\n").replace("\r", "\n")

    # Find the Enhancements section (### or ## level)
    pattern = r"###\s*Enhancements\s*(.*?)(?=\n###(?!#)|\n##(?!#)|\Z)"
    match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if not match:
        pattern = r"##\s*Enhancements\s*(.*?)(?=\n##(?!#)|\Z)"
        match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if not match:
        return []

    section = match.group(1)

    out: list[Enhancement] = []
    current_subsection: str | None = None

    for line in section.split("\n"):
        sub = re.match(r"^\s*####\s+(.+)$", line)
        if sub:
            current_subsection = sub.group(1).strip()
            continue

        bullet = re.match(r"^[\s]*[-*]\s+(.+)$", line)
        if not bullet:
            continue

        item = bullet.group(1).strip()

        if current_subsection:
            sub_lower = current_subsection.lower()
            if any(dev in sub_lower for dev in DEVELOPER_SUBSECTIONS):
                continue

        if not _is_user_facing(item):
            continue

        out.append(
            Enhancement(
                text=item,
                subsection=current_subsection,
                pr_numbers=extract_pr_numbers(item),
            )
        )

    return out
