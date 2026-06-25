"""
Google Docs client: OAuth, tab reading/discovery, and Backlog tab rewrite.

The doc has multiple tabs (a newer Docs feature). Tabs nest under
`document.tabs[*].documentTab.body.content` and may have child tabs in
`document.tabs[*].childTabs`. We flatten the tree and look up by title or ID.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import SOT_DOC_ID, USER_CONFIG_DIR


SCOPES = ["https://www.googleapis.com/auth/documents"]
# In the SOT doc, users typically write `#NNNNN` or paste `pull/NNNNN` URLs.
PR_HASH_RE = re.compile(r"#(\d+)")
PR_URL_RE = re.compile(r"https?://github\.com/[^/]+/[^/]+/pull/(\d+)")

# Markdown inline patterns
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MD_BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")
MD_ITALIC_RE = re.compile(r"_([^_\n]+)_")


def _utf16_len(s: str) -> int:
    """Length of `s` in UTF-16 code units — what Google Docs uses for indices."""
    return len(s.encode("utf-16-le")) // 2


def _process_inline(text: str, cursor_utf16: int) -> tuple[str, list[dict]]:
    """Strip inline markdown (links, bold, italic). Return (plain_text, style_ops).

    style_ops items: {"start", "end", "link"|"bold"|"italic", ...}
    """
    out_parts: list[str] = []
    ops: list[dict] = []
    i = 0
    pos = cursor_utf16
    while i < len(text):
        m = MD_LINK_RE.match(text, i)
        if m:
            label = m.group(1)
            url = m.group(2)
            start = pos
            end = pos + _utf16_len(label)
            out_parts.append(label)
            ops.append({"start": start, "end": end, "link": url})
            pos = end
            i = m.end()
            continue

        m = MD_BOLD_RE.match(text, i)
        if m:
            inner = m.group(1)
            start = pos
            end = pos + _utf16_len(inner)
            out_parts.append(inner)
            ops.append({"start": start, "end": end, "bold": True})
            pos = end
            i = m.end()
            continue

        m = MD_ITALIC_RE.match(text, i)
        if m:
            inner = m.group(1)
            start = pos
            end = pos + _utf16_len(inner)
            out_parts.append(inner)
            ops.append({"start": start, "end": end, "italic": True})
            pos = end
            i = m.end()
            continue

        ch = text[i]
        out_parts.append(ch)
        pos += _utf16_len(ch)
        i += 1
    return "".join(out_parts), ops


def markdown_to_docs_ops(md: str) -> tuple[str, list[dict]]:
    """Convert markdown to (plain_text, ops).

    ops items:
        {"kind": "paragraph_style", "start": int, "end": int, "style": "HEADING_1"|...}
        {"kind": "bullets", "start": int, "end": int}
        {"kind": "text_style", "start": int, "end": int, "link"?: str, "bold"?: bool, "italic"?: bool}
    Indices are UTF-16 offsets within the returned plain_text.
    """
    plain_parts: list[str] = []
    ops: list[dict] = []
    cursor = 0  # UTF-16 position

    bullet_block_start: int | None = None

    def close_bullet_block(end: int) -> None:
        nonlocal bullet_block_start
        if bullet_block_start is not None:
            ops.append({"kind": "bullets", "start": bullet_block_start, "end": end})
            bullet_block_start = None

    lines = md.split("\n")
    for raw_line in lines:
        line = raw_line.rstrip("\r")
        paragraph_start = cursor
        style: str | None = None
        is_bullet = False
        body = line

        if line.startswith("# "):
            style = "HEADING_1"
            body = line[2:]
        elif line.startswith("## "):
            style = "HEADING_2"
            body = line[3:]
        elif line.startswith("### "):
            style = "HEADING_3"
            body = line[4:]
        elif line.startswith("- ") or line.startswith("* "):
            is_bullet = True
            body = line[2:]
        elif line.strip() == "---":
            # Render horizontal rules as a blank line.
            body = ""

        if not is_bullet:
            close_bullet_block(cursor)

        plain_line, inline_ops = _process_inline(body, cursor)
        plain_parts.append(plain_line)
        cursor += _utf16_len(plain_line)

        for op in inline_ops:
            ops.append({"kind": "text_style", **op})

        # Append newline to terminate the paragraph
        plain_parts.append("\n")
        cursor += 1

        # Paragraph-level styles cover the line INCLUDING the trailing \n,
        # so the style is applied to that paragraph only and the next one
        # starts fresh (NORMAL by default).
        if style:
            ops.append({"kind": "paragraph_style", "start": paragraph_start, "end": cursor, "style": style})
        elif is_bullet:
            if bullet_block_start is None:
                bullet_block_start = paragraph_start
        else:
            # Normal paragraph; close any open bullet block now (was already closed above
            # if non-bullet, but a defensive close is harmless).
            pass

    close_bullet_block(cursor)
    return "".join(plain_parts), ops


def _config_dir() -> Path:
    return Path(os.path.expanduser(USER_CONFIG_DIR))


def _credentials_path() -> Path:
    return _config_dir() / "credentials.json"


def _token_path() -> Path:
    return _config_dir() / "token.json"


def _get_credentials() -> Credentials:
    cfg = _config_dir()
    cfg.mkdir(parents=True, exist_ok=True)

    cred_path = _credentials_path()
    if not cred_path.exists():
        raise FileNotFoundError(
            f"Missing {cred_path}. Create a Google Cloud OAuth client (Desktop app), "
            f"enable the Google Docs API, and place credentials.json there. "
            f"See README for step-by-step."
        )

    creds: Credentials | None = None
    tok = _token_path()
    if tok.exists():
        creds = Credentials.from_authorized_user_file(str(tok), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_path), SCOPES)
            creds = flow.run_local_server(port=0)
        tok.write_text(creds.to_json())

    return creds


def _service():
    return build("docs", "v1", credentials=_get_credentials(), cache_discovery=False)


# ---------------------------------------------------------------------------
# Tab tree handling
# ---------------------------------------------------------------------------


@dataclass
class TabInfo:
    tab_id: str
    title: str
    index: int  # order within the doc (for new-tab insertion)


def _flatten_tabs(tabs: list, *, depth: int = 0, counter: list[int] | None = None) -> list[TabInfo]:
    """Flatten the Docs tab tree into a list, preserving order."""
    if counter is None:
        counter = [0]
    out: list[TabInfo] = []
    for tab in tabs or []:
        props = tab.get("tabProperties", {})
        out.append(
            TabInfo(
                tab_id=props.get("tabId", ""),
                title=props.get("title", ""),
                index=counter[0],
            )
        )
        counter[0] += 1
        children = tab.get("childTabs") or []
        out.extend(_flatten_tabs(children, depth=depth + 1, counter=counter))
    return out


def _get_document(*, include_tabs: bool = True) -> dict:
    return (
        _service()
        .documents()
        .get(documentId=SOT_DOC_ID, includeTabsContent=include_tabs)
        .execute()
    )


def list_tabs() -> list[TabInfo]:
    # `includeTabsContent=true` is required to get the `tabs` field at all,
    # not just to populate tab body content.
    doc = _get_document(include_tabs=True)
    return _flatten_tabs(doc.get("tabs", []))


def find_tab(*, tab_id: str | None = None, title: str | None = None) -> TabInfo | None:
    for t in list_tabs():
        if tab_id and t.tab_id == tab_id:
            return t
        if title and t.title == title:
            return t
    return None


def ensure_tab(title: str) -> TabInfo:
    """Find a tab by title. Raises if missing — the Docs API does not (yet)
    support programmatic tab creation, so the user has to create it manually
    in Google Docs."""
    existing = find_tab(title=title)
    if existing:
        return existing
    raise RuntimeError(
        f"Tab '{title}' not found in the SOT doc.\n"
        f"  → Open the doc in Google Docs and create a tab named exactly '{title}', "
        f"then re-run.\n"
        f"  (The Google Docs API does not yet support programmatic tab creation.)"
    )


# ---------------------------------------------------------------------------
# Reading tab text
# ---------------------------------------------------------------------------


def _walk_text(elements: list) -> str:
    """Concatenate text out of a document-content structural element list."""
    parts: list[str] = []
    for el in elements or []:
        if "paragraph" in el:
            for run in el["paragraph"].get("elements", []):
                tr = run.get("textRun") or {}
                content = tr.get("content")
                if content:
                    parts.append(content)
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    parts.append(_walk_text(cell.get("content", [])))
        elif "sectionBreak" in el:
            parts.append("\n")
    return "".join(parts)


def _find_tab_in_tree(tabs: list, tab_id: str) -> dict | None:
    for t in tabs or []:
        if t.get("tabProperties", {}).get("tabId") == tab_id:
            return t
        nested = _find_tab_in_tree(t.get("childTabs", []), tab_id)
        if nested:
            return nested
    return None


def read_tab_text(*, tab_id: str | None = None, title: str | None = None) -> str:
    """Return the plain text of a tab. Raises if not found."""
    info = find_tab(tab_id=tab_id, title=title)
    if not info:
        raise ValueError(f"Tab not found: tab_id={tab_id} title={title}")

    doc = _get_document(include_tabs=True)
    tab = _find_tab_in_tree(doc.get("tabs", []), info.tab_id)
    if not tab:
        return ""
    body = tab.get("documentTab", {}).get("body", {})
    return _walk_text(body.get("content", []))


def read_pr_set(*, tab_id: str | None = None, title: str | None = None) -> set[int]:
    """Extract all #NNNNN PR numbers from a tab."""
    try:
        text = read_tab_text(tab_id=tab_id, title=title)
    except ValueError:
        return set()
    return (
        {int(m.group(1)) for m in PR_HASH_RE.finditer(text)}
        | {int(m.group(1)) for m in PR_URL_RE.finditer(text)}
    )


# ---------------------------------------------------------------------------
# Writing the Backlog tab
# ---------------------------------------------------------------------------


NOTES_HEADER = "📝 Notes"
NOTES_MARKER = "<!-- your notes below survive rewrites -->"


def extract_notes_block(tab_text: str) -> str:
    """Return the user-notes block from a previous Backlog render, or empty.

    The block is the text between the NOTES_MARKER line and the first '# '
    H1 heading (start of the generated body).
    """
    if NOTES_MARKER not in tab_text:
        return ""
    after_marker = tab_text.split(NOTES_MARKER, 1)[1]
    # Stop at first '# ' at the start of a line (H1)
    m = re.search(r"\n# ", after_marker)
    notes = after_marker[: m.start()] if m else after_marker
    return notes.strip("\n")


def _read_tab_doc(tab_id: str) -> tuple[dict, dict]:
    """Return (full_document, tab_node) for batchUpdate targeting."""
    doc = _get_document(include_tabs=True)
    tab = _find_tab_in_tree(doc.get("tabs", []), tab_id)
    if not tab:
        raise RuntimeError(f"Tab {tab_id} disappeared from doc")
    return doc, tab


def _doc_requests_for_body(
    tab_id: str, body_markdown: str, *, base_index: int, offset_utf16: int
) -> tuple[str, list[dict]]:
    """Build the requests to render `body_markdown` as styled Docs content.

    `base_index + offset_utf16` is the index where the body's plain text will
    begin in the doc (i.e. after the notes section). Returns (plain_body_text,
    requests_after_insert).
    """
    plain, ops = markdown_to_docs_ops(body_markdown)

    def doc_index(utf16_pos: int) -> int:
        return base_index + offset_utf16 + utf16_pos

    requests: list[dict] = []

    # Paragraph styles
    for op in ops:
        if op["kind"] != "paragraph_style":
            continue
        requests.append({
            "updateParagraphStyle": {
                "range": {
                    "tabId": tab_id,
                    "startIndex": doc_index(op["start"]),
                    "endIndex": doc_index(op["end"]),
                },
                "paragraphStyle": {"namedStyleType": op["style"]},
                "fields": "namedStyleType",
            }
        })

    # Bullets — one createParagraphBullets per contiguous block
    for op in ops:
        if op["kind"] != "bullets":
            continue
        requests.append({
            "createParagraphBullets": {
                "range": {
                    "tabId": tab_id,
                    "startIndex": doc_index(op["start"]),
                    "endIndex": doc_index(op["end"]),
                },
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        })

    # Inline text styles
    for op in ops:
        if op["kind"] != "text_style":
            continue
        text_style: dict = {}
        fields: list[str] = []
        if "link" in op:
            text_style["link"] = {"url": op["link"]}
            text_style["foregroundColor"] = {
                "color": {"rgbColor": {"red": 0.067, "green": 0.333, "blue": 0.8}}
            }
            text_style["underline"] = True
            fields += ["link", "foregroundColor", "underline"]
        if op.get("bold"):
            text_style["bold"] = True
            fields.append("bold")
        if op.get("italic"):
            text_style["italic"] = True
            fields.append("italic")
        if not fields:
            continue
        requests.append({
            "updateTextStyle": {
                "range": {
                    "tabId": tab_id,
                    "startIndex": doc_index(op["start"]),
                    "endIndex": doc_index(op["end"]),
                },
                "textStyle": text_style,
                "fields": ",".join(fields),
            }
        })

    return plain, requests


def replace_tab_content(tab_id: str, body_markdown: str, *, preserved_notes: str = "") -> None:
    """Rewrite the entire tab content. Inserts a Notes section + a styled body.

    Markdown structure is converted to real Docs styling:
        # ## ###       → HEADING_1/2/3 paragraph styles
        - item         → bulleted list
        _italic_       → italic
        **bold**       → bold
        [text](url)    → hyperlink
    """
    doc, tab = _read_tab_doc(tab_id)
    body = tab.get("documentTab", {}).get("body", {})
    content = body.get("content", [])

    if not content:
        return
    end_index = content[-1].get("endIndex", 1)
    delete_end = max(1, end_index - 1)

    notes_section = (
        f"{NOTES_HEADER}\n"
        f"{NOTES_MARKER}\n"
        f"{preserved_notes}\n\n"
    )

    notes_offset = _utf16_len(notes_section)
    plain_body, body_style_requests = _doc_requests_for_body(
        tab_id, body_markdown,
        base_index=1, offset_utf16=notes_offset,
    )

    full_text = notes_section + plain_body
    if not full_text.endswith("\n"):
        full_text += "\n"

    requests: list[dict] = []
    if delete_end > 1:
        requests.append({
            "deleteContentRange": {
                "range": {
                    "tabId": tab_id,
                    "startIndex": 1,
                    "endIndex": delete_end,
                }
            }
        })

    # 1) Insert the full text
    requests.append({
        "insertText": {
            "location": {"tabId": tab_id, "index": 1},
            "text": full_text,
        }
    })

    # 2) Reset the body region's paragraphs to NORMAL_TEXT (so any inherited
    #    styles from before deletion are cleared), then apply our paragraph
    #    styles on top.
    plain_body_len = _utf16_len(plain_body)
    if plain_body_len > 0:
        requests.append({
            "updateParagraphStyle": {
                "range": {
                    "tabId": tab_id,
                    "startIndex": 1 + notes_offset,
                    "endIndex": 1 + notes_offset + plain_body_len,
                },
                "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                "fields": "namedStyleType",
            }
        })

    # 3) Apply markdown-derived styles
    requests.extend(body_style_requests)

    _service().documents().batchUpdate(
        documentId=SOT_DOC_ID, body={"requests": requests}
    ).execute()
