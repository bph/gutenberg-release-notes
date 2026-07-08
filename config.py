"""
Configuration for the Gutenberg release-notes punch-list generator.

One WP cycle is "live" at a time. To start the next cycle, update these values
and commit; the previous cycle's Backlog tab in its Google Doc remains as a
frozen historical record.
"""

# ---------------------------------------------------------------------------
# WordPress release cycle
# ---------------------------------------------------------------------------
WP_CYCLE = "7.1"

# First Gutenberg plugin release that belongs to this WP cycle.
WP_CYCLE_START_VERSION = "v22.7.0"

# GB version aligned with WP cycle's Beta 1. Set when known.
# - None / unset: pre-Beta-1 mode (include non-backport PRs, exclude backports)
# - Set: post-Beta-1 mode for releases >= this version (include backports, exclude non-backports)
WP_CYCLE_BETA_1_VERSION = None

# Last GB version that belongs to this cycle. Set when WP GA ships; until then,
# new GB releases continue to be processed.
WP_CYCLE_END_VERSION = None

# Earliest merge/creation date for wp-develop PRs considered for this cycle
# during automatic discovery. Roughly matches WP_CYCLE_START_VERSION's
# release date, with a small buffer.
WP_CYCLE_SEARCH_START_DATE = "2026-03-01"

# ---------------------------------------------------------------------------
# Source of Truth Google Doc
# ---------------------------------------------------------------------------
SOT_DOC_ID = "12KnsxlgMkNSzXN_otRHELBwYmnD-G5U4gZ-XpQciYmc"
# All tabs are looked up by exact title (case + punctuation matters).
# Rename here if you rename a tab in the doc.
SOT_DRAFT_TAB_TITLE = "Draft [WIP]"   # read-only, ✅ source
SOT_HANDLED_TAB_TITLE = "Handled"     # user-edited, also counts as ✅
SOT_BACKLOG_TAB_TITLE = "Backlog"     # script-managed, rewritten each run

# ---------------------------------------------------------------------------
# Roadmap source
# ---------------------------------------------------------------------------
ROADMAP_URL = "https://make.wordpress.org/core/2026/06/19/roadmap-to-7-1/"

# ---------------------------------------------------------------------------
# GitHub
# ---------------------------------------------------------------------------
GITHUB_REPO = "WordPress/gutenberg"
BACKPORT_LABEL = "Backported to WP Core"

# ---------------------------------------------------------------------------
# Enhancement filtering (carried over from prior version)
# ---------------------------------------------------------------------------
DEVELOPER_SUBSECTIONS = [
    "data layer", "code quality", "build tooling", "testing",
    "documentation", "tools", "packages", "tooling",
]

DEVELOPER_KEYWORDS = [
    "api", "hook", "filter", "deprecat", "refactor",
    "internal", "unit test", "e2e test", "test coverage",
    "code quality", "technical debt", "types", "typescript",
]

# ---------------------------------------------------------------------------
# Claude API
# ---------------------------------------------------------------------------
CLAUDE_MODEL = "claude-sonnet-4-5"
CLAUDE_MAX_TOKENS = 16000

# ---------------------------------------------------------------------------
# Paths (relative to repo root)
# ---------------------------------------------------------------------------
DATA_DIR = "data"
PUNCHLIST_DIR = "punchlist"
USER_CONFIG_DIR = "~/.config/gutenberg-release-notes"  # OAuth credentials live here
