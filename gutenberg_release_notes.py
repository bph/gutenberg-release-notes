#!/usr/bin/env python3
"""
Gutenberg release-notes punch-list generator.

Reads the current WP cycle's roadmap + shipped Gutenberg plugin releases,
cross-references against the SOT Google Doc's "Draft wip" tab to mark which
PRs are still to cite, and writes the resulting punch-list to the "Backlog"
tab plus a local markdown mirror.

Usage:
    python gutenberg_release_notes.py
    python gutenberg_release_notes.py --refresh-roadmap
    python gutenberg_release_notes.py --skip-gdoc            # local-only mirror
    python gutenberg_release_notes.py --force-refresh        # ignore PR cache
"""

from __future__ import annotations

import argparse
import sys

from config import (
    SOT_BACKLOG_TAB_TITLE,
    SOT_DRAFT_TAB_ID,
    SOT_HANDLED_TAB_TITLE,
    WP_CYCLE,
)
from lib import cluster, gdoc, github_releases, match, punchlist, roadmap, state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-roadmap", action="store_true",
                        help="Re-fetch and re-parse the roadmap post")
    parser.add_argument("--skip-gdoc", action="store_true",
                        help="Skip Google Doc read/write; only update local mirror")
    parser.add_argument("--force-refresh", action="store_true",
                        help="Re-fetch every release from GitHub (ignore version cache)")
    args = parser.parse_args(argv)

    print(f"Punch-list run for WP {WP_CYCLE}")
    print("=" * 60)

    st = state.load()

    # ---- 1. Roadmap ----
    if args.refresh_roadmap or not roadmap.ROADMAP_JSON.exists():
        print("\n[1/6] Refreshing roadmap")
        roadmap_items = roadmap.refresh()
    else:
        print("\n[1/6] Loading cached roadmap")
        roadmap_items = roadmap.load()
        print(f"  {len(roadmap_items)} items")

    # ---- 2. Discover and cache GB releases ----
    print("\n[2/6] Discovering Gutenberg releases in cycle")
    releases = github_releases.list_cycle_releases()
    print(f"  {len(releases)} release(s) in cycle: {', '.join(r['tag_name'] for r in releases) or '(none)'}")

    cached_releases = []
    for r in releases:
        print(f"  • {r['tag_name']}")
        cached_releases.append(github_releases.ensure_cached(r, force_refresh=args.force_refresh))

    # ---- 3. Match PRs to roadmap items ----
    print("\n[3/6] Matching PRs to roadmap items")
    shipped_by_version = {
        cr.version: cr.included_prs() for cr in cached_releases
    }
    n_included = sum(len(v) for v in shipped_by_version.values())
    print(f"  {n_included} included PR(s) across {len(shipped_by_version)} release(s)")

    match_result = match.match(roadmap_items, shipped_by_version)
    print(f"  {sum(len(it.matched_prs) for it in match_result.items)} matched to roadmap; "
          f"{len(match_result.leftover_prs)} leftover")

    # ---- 4. Cluster leftovers ----
    print("\n[4/6] Clustering leftover PRs")
    clusters = cluster.cluster_leftovers(match_result.leftover_prs)
    print(f"  {len(clusters)} cluster(s)")

    # ---- 5. Read coverage from Google Doc ----
    covered: set[int] = set()
    backlog_tab_id = st.get("backlog_tab_id")
    preserved_notes = ""

    if not args.skip_gdoc:
        print("\n[5/6] Reading coverage from Google Doc")
        draft_prs = gdoc.read_pr_set(tab_id=SOT_DRAFT_TAB_ID)
        print(f"  Draft wip: {len(draft_prs)} PR number(s) cited")

        handled_tab = gdoc.ensure_tab(SOT_HANDLED_TAB_TITLE)
        handled_prs = gdoc.read_pr_set(tab_id=handled_tab.tab_id)
        st["handled_tab_id"] = handled_tab.tab_id
        print(f"  Handled:   {len(handled_prs)} PR number(s)")

        covered = draft_prs | handled_prs

        backlog_tab = gdoc.ensure_tab(SOT_BACKLOG_TAB_TITLE)
        backlog_tab_id = backlog_tab.tab_id
        st["backlog_tab_id"] = backlog_tab_id

        try:
            existing = gdoc.read_tab_text(tab_id=backlog_tab_id)
            preserved_notes = gdoc.extract_notes_block(existing)
        except Exception as e:
            print(f"  (no prior notes to preserve: {e})")
    else:
        print("\n[5/6] Skipping Google Doc (--skip-gdoc); everything will appear as 🔲")

    # ---- 6. Render and write ----
    print("\n[6/6] Rendering punch-list")
    versions = sorted({cr.version for cr in cached_releases}, key=lambda v: tuple(int(x) for x in v.lstrip("v").split(".")))
    prior_prs = set(st.get("last_prs") or [])
    current_prs = {p.number for it in match_result.items for p in it.matched_prs} | {
        p.number for c in clusters for p in c.prs
    }
    new_prs = current_prs - prior_prs

    body = punchlist.render_markdown(
        match_result, clusters, covered, new_prs, versions
    )
    mirror_path = punchlist.write_local_mirror(body)
    print(f"  Local mirror: {mirror_path}")

    if not args.skip_gdoc and backlog_tab_id:
        print(f"  Writing Backlog tab…")
        gdoc.replace_tab_content(backlog_tab_id, body, preserved_notes=preserved_notes)

    # ---- Persist state ----
    st["processed_versions"] = versions
    st["last_prs"] = sorted(current_prs)
    state.save(st)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
