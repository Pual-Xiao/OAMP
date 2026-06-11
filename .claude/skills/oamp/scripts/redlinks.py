"""Scan a room for redlinks — [[wikilinks]] that don't resolve to existing notes.

Redlinks are the expansion engine. Each is an encoded but unrealized intent —
a concept the author knew belonged in the network but hasn't written yet.

Usage:
  python3 scripts/redlinks.py --vault <vault> --room <room> [--json] [--min-refs N]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

WIKILINK_RE = re.compile(r'\[\[([^]#|]+)(?:[#|][^]]*)?\]\]')
EXCLUDE_DIRS = {".obsidian", ".trash", ".git", "__pycache__", "node_modules"}


def _extract_stems(filepath: Path) -> set[str]:
    stems: set[str] = set()
    try:
        for m in WIKILINK_RE.finditer(filepath.read_text()):
            raw = m.group(1).strip()
            if not raw or raw.endswith("/") or raw.startswith(".."):
                continue
            raw = raw.rstrip("\\")
            if "/" in raw:
                raw = raw.rsplit("/", 1)[-1]
            if raw:
                stems.add(raw)
    except Exception:
        pass
    return stems


def _find_md(vault_root: Path, stem: str) -> Path | None:
    for root, dirs, files in os.walk(vault_root, followlinks=True):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if f"{stem}.md" in files:
            return Path(root) / f"{stem}.md"
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Scan room for redlinks (expansion candidates)")
    parser.add_argument("--vault", required=True, help="Vault root path")
    parser.add_argument("--room", required=True, help="Room path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--bare", action="store_true",
                        help="Bare output — one redlink per line")
    parser.add_argument("--min-refs", type=int, default=1,
                        help="Minimum reference count (default: 1)")
    args = parser.parse_args()

    vault = Path(args.vault)
    room = Path(args.room)
    if not room.is_absolute():
        room = vault / args.room
    if not room.is_dir():
        print(f"ERROR: room not found: {room}")
        sys.exit(1)

    # Collect all wikilink references in the room
    all_links: dict[str, list[str]] = defaultdict(list)
    for f in sorted(room.rglob("*.md")):
        parts = set(f.relative_to(room).parts)
        if parts & EXCLUDE_DIRS:
            continue
        rel = str(f.relative_to(vault))
        try:
            for stem in _extract_stems(f):
                all_links[stem].append(rel)
        except Exception:
            continue

    # Filter to redlinks only — targets with no .md file
    redlinks: dict[str, list[str]] = {}
    for stem, refs in sorted(all_links.items()):
        if _find_md(vault, stem) is not None:
            continue
        if len(refs) >= args.min_refs:
            redlinks[stem] = refs

    if args.bare:
        for stem in sorted(redlinks):
            print(stem)
        return

    if args.json:
        output = {
            "room": str(room.relative_to(vault)),
            "total_redlinks": len(redlinks),
            "candidates": [
                {"name": stem, "refs": len(refs), "referenced_by": refs}
                for stem, refs in sorted(redlinks.items(), key=lambda x: -len(x[1]))
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if not redlinks:
        print("No redlinks found. Room may be mature.")
        return

    print(f"=== REDLINKS ({len(redlinks)} expansion candidates) ===\n")
    for stem, refs in sorted(redlinks.items(), key=lambda x: -len(x[1])):
        short = [r.rsplit("/", 1)[-1].replace(".md", "") for r in refs[:5]]
        ref_str = ", ".join(short)
        if len(refs) > 5:
            ref_str += f", ... (+{len(refs) - 5} more)"
        print(f"  [[{stem}]]  <- {len(refs)} ref(s): {ref_str}")


if __name__ == "__main__":
    main()
