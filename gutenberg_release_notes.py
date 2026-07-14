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
import time

from config import (
    SOT_BACKLOG_TAB_TITLE,
    SOT_DRAFT_TAB_TITLE,
    SOT_HANDLED_TAB_TITLE,
    WP_CYCLE,
    WP_CYCLE_PENDING_MILESTONE,
    WP_CYCLE_PENDING_VERSION,
)
from lib import (
    cluster,
    gdoc,
    github_releases,
    match,
    pending_release,
    punchlist,
    roadmap,
    state,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-roadmap", action="store_true",
                        help="Re-fetch and re-parse the roadmap post")
    parser.add_argument("--skip-gdoc", action="store_true",
                        help="Skip Google Doc read/write; only update local mirror")
    parser.add_argument("--force-refresh", action="store_true",
                        help="Re-fetch every release from GitHub (ignore version cache)")
    parser.add_argument("--refresh-clusters", action="store_true",
                        help="Delete the cluster cache to force a fresh clustering pass")
    parser.add_argument("--refresh-pending", action="store_true",
                        help="Force re-fetch of the pending-milestone PR cache")
    args = parser.parse_args(argv)

    print(f"Punch-list run for WP {WP_CYCLE}")
    print("=" * 60)

    st = state.load()

    # ---- 1. Google Doc auth + read coverage (eager, so browser opens FIRST) ----
    covered: set[int] = set()
    backlog_tab_id: str | None = st.get("backlog_tab_id")
    preserved_notes = ""

    if not args.skip_gdoc:
        print("\n[1/7] Authenticating to Google Docs + reading coverage")
        print("  (first run will open a browser for consent)")
        print(f"  Required tabs in the doc: '{SOT_DRAFT_TAB_TITLE}', "
              f"'{SOT_HANDLED_TAB_TITLE}', '{SOT_BACKLOG_TAB_TITLE}' "
              f"— create these manually if missing (case-sensitive).")
        draft_tab = gdoc.ensure_tab(SOT_DRAFT_TAB_TITLE)
        draft_prs = gdoc.read_pr_set(tab_id=draft_tab.tab_id)
        print(f"  {SOT_DRAFT_TAB_TITLE}: {len(draft_prs)} PR number(s) cited")

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
            if preserved_notes:
                print(f"  📝 Preserved {len(preserved_notes.splitlines())} lines of notes")
        except Exception as e:
            print(f"  (no prior notes to preserve: {e})")
    else:
        print("\n[1/7] Skipping Google Doc (--skip-gdoc); everything will appear as 🔲")

    # ---- 2. Roadmap ----
    if args.refresh_roadmap or not roadmap.ROADMAP_JSON.exists():
        print("\n[2/7] Refreshing roadmap (calling Claude to parse)…")
        t = time.time()
        roadmap_items = roadmap.refresh()
        print(f"  parsed {len(roadmap_items)} items in {time.time() - t:.1f}s")
    else:
        print("\n[2/7] Loading cached roadmap")
        roadmap_items = roadmap.load()
        print(f"  {len(roadmap_items)} items")

    # ---- 3. Discover and cache GB releases ----
    print("\n[3/7] Discovering Gutenberg releases in cycle")
    releases = github_releases.list_cycle_releases()
    print(f"  {len(releases)} release(s) in cycle: {', '.join(r['tag_name'] for r in releases) or '(none)'}")

    cached_releases = []
    for r in releases:
        print(f"  • {r['tag_name']}", flush=True)
        cached_releases.append(github_releases.ensure_cached(r, force_refresh=args.force_refresh))

    if WP_CYCLE_PENDING_MILESTONE:
        try:
            pending = pending_release.ensure_pending(
                WP_CYCLE_PENDING_MILESTONE,
                WP_CYCLE_PENDING_VERSION,
                force_refresh=args.refresh_pending,
            )
            included = len(pending.included_prs())
            print(f"  • {WP_CYCLE_PENDING_VERSION} ({included} included / {len(pending.prs)} total PRs, pending)")
            cached_releases.insert(0, pending)
        except Exception as e:  # noqa: BLE001 — pending fetch is best-effort
            print(f"  ⚠️  pending milestone fetch failed: {e}")

    # ---- 4. Match PRs to roadmap items ----
    print("\n[4/7] Matching PRs to roadmap items")
    shipped_by_version = {
        cr.version: cr.included_prs() for cr in cached_releases
    }
    n_included = sum(len(v) for v in shipped_by_version.values())
    print(f"  {n_included} included PR(s) across {len(shipped_by_version)} release(s)")
    print("  resolving tracking issues + fuzzy-matching…", flush=True)

    t = time.time()
    match_result = match.match(roadmap_items, shipped_by_version)
    print(f"  {sum(len(it.matched_prs) for it in match_result.items)} matched to roadmap; "
          f"{len(match_result.leftover_prs)} leftover ({time.time() - t:.1f}s)")

    # ---- 5. Cluster leftovers ----
    if args.refresh_clusters and cluster.CLUSTERS_PATH.exists():
        cluster.CLUSTERS_PATH.unlink()
        print("\n  (cluster cache cleared by --refresh-clusters)")
    print(f"\n[5/7] Clustering {len(match_result.leftover_prs)} leftover PRs (Claude, ~30-90s)…", flush=True)
    t = time.time()
    clusters = cluster.cluster_leftovers(match_result.leftover_prs)
    print(f"  {len(clusters)} cluster(s) in {time.time() - t:.1f}s")

    # ---- 6. Render ----
    print("\n[6/7] Rendering punch-list")
    def _version_key(v: str) -> tuple[int, ...]:
        # Strip a possible "-pending" (or other) suffix from the final segment
        # so v23.6.0-pending still sorts as (23, 6, 0).
        parts = v.lstrip("v").split(".")
        parts[-1] = parts[-1].split("-", 1)[0]
        return tuple(int(p) for p in parts)
    versions = sorted({cr.version for cr in cached_releases}, key=_version_key)
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
        print("\n[7/7] Writing Backlog tab…", flush=True)
        gdoc.replace_tab_content(backlog_tab_id, body, preserved_notes=preserved_notes)
        print("  done")
    else:
        print("\n[7/7] Skipped Google Doc write")

    # ---- Persist state ----
    st["processed_versions"] = versions
    st["last_prs"] = sorted(current_prs)
    state.save(st)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
