# Gutenberg Release Notes Punch-List

A small tool that watches each new Gutenberg plugin release, cross-references the shipped PRs against the WordPress release cycle's roadmap and the in-progress Source of Truth (SOT) Google Doc, and writes a feature-clustered punch-list back to a dedicated tab in the doc. Designed for a smooth, ongoing process of writing the SOT instead of a manual batch job.

## What it does, in one diagram

```
┌────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ Roadmap post       │  │ Gutenberg releases  │  │ Google Doc          │
│ (make.wp.org)      │  │ (GitHub API)        │  │ "Draft wip" tab     │
└────────┬───────────┘  └──────────┬──────────┘  └──────────┬──────────┘
         │                         │                         │
         ▼                         ▼                         ▼
   roadmap items          shipped PRs (filtered)       cited PR numbers
   + tracking issues      by cycle phase & backport     (= ✅ covered)
         │                         │                         │
         └────────┬────────────────┴────────────┬────────────┘
                  ▼                             ▼
            roadmap matcher              coverage check
       (tracking-issue → PRs,         (Draft wip ∪ Handled)
        Claude fuzzy fallback)
                  │
                  ▼
         Backlog tab in same doc:
         feature-clustered punch-list with ✅ / 🔲 / ⏳ markers
```

## Status semantics

Per-roadmap-item:

| Marker | Meaning |
|---|---|
| ⏳ | No matching PRs shipped yet |
| 🚧 | PRs shipped, none cited in Draft wip |
| 🟡 | Some PRs cited, some still 🔲 |
| ✅ | All matched PRs cited |

Per-PR:

| Marker | Meaning |
|---|---|
| ✅ | PR number appears in Draft wip OR Handled tab |
| 🔲 | PR not yet cited |
| 🆕 | New since the previous run (one cycle only) |
| ⚠️ | Low-confidence fuzzy match — eyeball this one |

## Tabs in the SOT Google Doc

- **Draft wip** — your prose. Read-only to the script. Cite every PR you write up (`[#NNNNN](...)`) — preferably as a trailing link list per feature section.
- **Handled** — user-edited list of PR numbers you've dealt with by means *other than* a direct citation. Use it for: features covered in prose without explicit cites, intentional skips, or genuine false positives. One-line notes alongside each number are encouraged.
- **Backlog** — script-managed. Rewritten each run, except for the `📝 Notes` block at the top guarded by `<!-- your notes below survive rewrites -->`.

> **Important**: Google Docs API does not yet support programmatic tab creation. Before the first run, **create both `Handled` and `Backlog` tabs manually** in your SOT Google Doc (right-click any tab → "New tab"). The script will fail with a clear error if either is missing.

## One-time setup

### 1. Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Google Cloud OAuth (for Docs API)

1. Visit https://console.cloud.google.com → create project `gutenberg-release-notes` (or reuse one)
2. **APIs & Services → Library** → enable **Google Docs API**
3. **APIs & Services → OAuth consent screen** → External → add your email as a test user
4. **APIs & Services → Credentials → Create credentials → OAuth client ID → Desktop app** → download `credentials.json`
5. Place the file at `~/.config/gutenberg-release-notes/credentials.json`
6. First script run will open a browser for consent; the resulting `token.json` is cached alongside `credentials.json` and refreshed automatically.

### 3. Anthropic API key

Set `ANTHROPIC_API_KEY` in `.env` (the repo already has a `.env.example`).

### 4. GitHub auth

The script uses your existing `gh` CLI auth (`gh auth login`). No extra setup if `gh auth status` is green.

## Running

```bash
# Normal run after a new GB plugin release
python gutenberg_release_notes.py

# Force re-fetch and re-parse the roadmap post
python gutenberg_release_notes.py --refresh-roadmap

# Local-only: skip Google Doc read/write (useful for testing or no-auth runs)
python gutenberg_release_notes.py --skip-gdoc

# Re-fetch all releases from GitHub (ignore per-version cache)
python gutenberg_release_notes.py --force-refresh
```

A typical run takes ~30 seconds for an active cycle.

## Cycle configuration

In `config.py`:

```python
WP_CYCLE = "7.1"
WP_CYCLE_START_VERSION = "v22.7.0"      # first GB version in this cycle
WP_CYCLE_BETA_1_VERSION = None           # set when WP Beta 1 is announced
WP_CYCLE_END_VERSION = None              # set when WP GA ships

SOT_DOC_ID = "12Kns...."                 # Google Doc ID
SOT_DRAFT_TAB_ID = "t.ap1297to0djs"      # the "Draft wip" tab
ROADMAP_URL = "https://make.wordpress.org/core/2026/06/19/roadmap-to-7-1/"
```

Backport filtering is **phase-aware** based on `WP_CYCLE_BETA_1_VERSION`:

| Phase | Non-backport PR | Backport-labeled PR |
|---|---|---|
| Pre-Beta-1 (default) | ✅ include | ❌ exclude (→ previous WP) |
| Post-Beta-1 | ❌ exclude (→ next WP) | ✅ include (→ this cycle) |

Schedule: run manually after each Gutenberg plugin release (every ~2 weeks). RCs are skipped automatically.

## Repo layout

```
gutenberg-release-notes/
├── config.py
├── gutenberg_release_notes.py    # entrypoint
├── lib/
│   ├── parse.py                  # release body → enhancement bullets
│   ├── github_api.py             # auth + REST helper
│   ├── github_releases.py        # discovery, PR labels, backport filter
│   ├── tracking.py               # roadmap tracking-issue → PR set
│   ├── roadmap.py                # fetch + Claude-parse roadmap post
│   ├── gdoc.py                   # Google Docs OAuth + tab read/write
│   ├── match.py                  # roadmap-PR matching (deterministic + fuzzy)
│   ├── cluster.py                # cluster leftover PRs (Claude, anchored)
│   ├── punchlist.py              # render markdown punch-list
│   └── state.py                  # JSON state on disk
├── data/                         # version caches, tracking caches, state, clusters
├── punchlist/                    # local markdown mirror of each run
└── archive/                      # prior cycles' outputs (read-only history)
```

## Troubleshooting

- **`gh: command not found`** — install GitHub CLI (`brew install gh`), then `gh auth login`.
- **Browser doesn't open for Google consent** — first run needs interactive consent; subsequent runs use the cached refresh token in `~/.config/gutenberg-release-notes/token.json`.
- **Backport label changes name on `WordPress/gutenberg`** — update `BACKPORT_LABEL` in `config.py`.
- **Roadmap items with low-confidence parse** — hand-edit `data/roadmap_wp-<cycle>.json` and re-run; the cached file is the source of truth for the matcher.

## License

MIT.
