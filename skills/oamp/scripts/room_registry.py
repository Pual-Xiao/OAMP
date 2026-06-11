"""Shared room registry — locate and manage rooms.yml.

Resolution order:
1. OBSIDIAN_AUTOMATION_CONFIG env var
2. ./.oamp/rooms.yml (current working directory)
"""

from __future__ import annotations

import os
from pathlib import Path


def resolve_rooms_yml() -> Path:
    env = os.environ.get("OBSIDIAN_AUTOMATION_CONFIG")
    if env:
        p = Path(env)
        if p.exists():
            return p.resolve()

    return Path.cwd() / ".oamp" / "rooms.yml"


def load_rooms(config_path: str | Path | None = None) -> dict[str, dict]:
    """Return {room_name: {path, type, ...}} for all registered rooms."""
    import yaml

    if config_path is None:
        config_path = resolve_rooms_yml()
    try:
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}
    rooms = data.get("rooms") or {}
    for name, room in rooms.items():
        raw = str(room.get("path", ""))
        if raw.startswith("~"):
            room["path"] = Path(raw).expanduser().resolve()
        else:
            room["path"] = Path(raw).resolve()
    return rooms


def rooms_by_type(*types: str, config_path: str | Path | None = None) -> dict[str, Path]:
    """Return {room_name: resolved_path} for rooms matching given type(s)."""
    all_rooms = load_rooms(config_path)
    if not types:
        return {name: r["path"] for name, r in all_rooms.items()}
    return {
        name: r["path"]
        for name, r in all_rooms.items()
        if r.get("type") in types
    }
