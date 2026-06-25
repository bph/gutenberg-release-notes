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
    doc = _get_document(include_tabs=False)
    return _flatten_tabs(doc.get("tabs", []))


def find_tab(*, tab_id: str | None = None, title: str | None = None) -> TabInfo | None:
    for t in list_tabs():
        if tab_id and t.tab_id == tab_id:
            return t
        if title and t.title == title:
            return t
    return None


def ensure_tab(title: str) -> TabInfo:
    """Find a tab by title, or create one. Returns the (possibly new) tab info."""
    existing = find_tab(title=title)
    if existing:
        return existing

    requests = [
        {
            "createDocumentTab": {
                "tabProperties": {"title": title}
            }
        }
    ]
    _service().documents().batchUpdate(
        documentId=SOT_DOC_ID, body={"requests": requests}
    ).execute()

    found = find_tab(title=title)
    if not found:
        raise RuntimeError(f"Created tab '{title}' but couldn't find it on re-read.")
    return found


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


def replace_tab_content(tab_id: str, body_markdown: str, *, preserved_notes: str = "") -> None:
    """Rewrite the entire tab content. Inserts a Notes section + the body."""
    doc, tab = _read_tab_doc(tab_id)
    body = tab.get("documentTab", {}).get("body", {})
    content = body.get("content", [])

    # Compute the deletion range. Content always ends with a trailing newline
    # whose end index is the tab's end. Docs requires us to leave the final
    # newline alone — delete from index 1 up to (end - 1).
    if not content:
        return
    end_index = content[-1].get("endIndex", 1)
    delete_end = max(1, end_index - 1)

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

    # Build the full insertion text
    notes_section = (
        f"{NOTES_HEADER}\n"
        f"{NOTES_MARKER}\n"
        f"{preserved_notes}\n\n"
    )
    full_text = notes_section + body_markdown
    if not full_text.endswith("\n"):
        full_text += "\n"

    requests.append({
        "insertText": {
            "location": {"tabId": tab_id, "index": 1},
            "text": full_text,
        }
    })

    _service().documents().batchUpdate(
        documentId=SOT_DOC_ID, body={"requests": requests}
    ).execute()
