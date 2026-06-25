"""State persistence for the punch-list orchestrator."""

from __future__ import annotations

import json
from pathlib import Path

from config import DATA_DIR, WP_CYCLE


def state_path() -> Path:
    return Path(DATA_DIR) / f"state_wp-{WP_CYCLE}.json"


def load() -> dict:
    p = state_path()
    if not p.exists():
        return {
            "wp_cycle": WP_CYCLE,
            "processed_versions": [],
            "backlog_tab_id": None,
            "handled_tab_id": None,
            "roadmap_fetched_at": None,
            "last_prs": [],  # for 🆕 marker
        }
    return json.loads(p.read_text())


def save(state: dict) -> None:
    p = state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, sort_keys=True))
