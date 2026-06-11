"""Wikilink verification and orphan detection.

Subcommands:
  check    Verify all [[wikilink]] targets resolve to existing .md files
  orphans  Find .md files with zero inbound links

Usage:
  python3 scripts/wikilinks.py check <vault-path>
  python3 scripts/wikilinks.py orphans <room-path>
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

WIKILINK_RE = re.compile(r'\[\[([^]#|]+)(?:[#|][^]]*)?\]\]')
EXCLUDE_DIRS = {".obsidian", ".trash", ".git", "__pycache__", "node_modules"}
ASSET_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".webp", ".mp4", ".mp3"}


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


def _collect_all_stems(vault: Path) -> set[str]:
    stems: set[str] = set()
    for f in vault.rglob("*.md"):
        parts = set(f.relative_to(vault).parts)
        if parts & EXCLUDE_DIRS:
            continue
        stems.add(f.stem)
    return stems


# ── check ─────────────────────────────────────────────────────────────

def cmd_check(vault_path: Path):
    if not vault_path.is_dir():
        print(f"ERROR: vault not found: {vault_path}")
        sys.exit(1)

    all_stems = _collect_all_stems(vault_path)
    broken_by_file: dict[str, list[tuple[str, int]]] = {}
    total_links = 0
    broken_count = 0

    for f in sorted(vault_path.rglob("*.md")):
        parts = set(f.relative_to(vault_path).parts)
        if parts & EXCLUDE_DIRS:
            continue
        try:
            lines = f.read_text().splitlines()
        except Exception:
            continue
        file_broken: list[tuple[str, int]] = []
        for i, line in enumerate(lines, 1):
            for m in WIKILINK_RE.finditer(line):
                total_links += 1
                target = m.group(1).strip().rstrip("\\/ ")
                if target.endswith("/") or target.endswith(tuple(ASSET_EXTS)):
                    continue
                stem = target.rsplit("/", 1)[-1] if "/" in target else target
                if stem not in all_stems:
                    file_broken.append((target, i))
                    broken_count += 1
        if file_broken:
            broken_by_file[str(f.relative_to(vault_path))] = file_broken

    if not broken_by_file:
        print("All wikilinks resolve.")
        return

    print(f"Notes: {len(all_stems)}")
    print(f"Total links: {total_links}")
    print(f"Broken: {broken_count}\n")

    by_target: dict[str, list[str]] = defaultdict(list)
    for filepath, links in broken_by_file.items():
        for target, _ in links:
            by_target[target].append(filepath)

    for target in sorted(by_target):
        sources = by_target[target]
        print(f"### [[{target}]]")
        print(f"Referenced by {len(sources)} file(s):")
        for s in sources[:5]:
            print(f"  - {s}")
        if len(sources) > 5:
            print(f"  - ... and {len(sources) - 5} more")
        print()


# ── orphans ───────────────────────────────────────────────────────────

def cmd_orphans(room_path: Path):
    if not room_path.is_dir():
        print(f"ERROR: room not found: {room_path}")
        sys.exit(1)

    notes: dict[str, Path] = {}
    for f in room_path.rglob("*.md"):
        parts = set(f.relative_to(room_path).parts)
        if parts & EXCLUDE_DIRS:
            continue
        notes[f.stem] = f.relative_to(room_path)

    counts: dict[str, int] = defaultdict(int)
    for f in room_path.rglob("*.md"):
        parts = set(f.relative_to(room_path).parts)
        if parts & EXCLUDE_DIRS:
            continue
        try:
            for target in _extract_stems(f):
                counts[target] += 1
        except Exception:
            pass

    def _is_entry(rel: Path) -> bool:
        return rel.parts[0].startswith("00-") if rel.parts else False

    orphans = sorted(n for n in notes if counts.get(n, 0) == 0 and not _is_entry(notes[n]))
    near = sorted(n for n in notes if counts.get(n, 0) == 1 and not _is_entry(notes[n]))

    if not orphans and not near:
        total = len([n for n in notes if not _is_entry(notes[n])])
        print(f"All {total} notes have >= 2 inbound links. Graph healthy.")
        return

    total = len([n for n in notes if not _is_entry(notes[n])])
    print(f"Notes: {total} (excluding entry folder)")

    if orphans:
        print(f"\n### Orphans (0 inlinks): {len(orphans)}")
        for o in orphans:
            note_path = room_path / notes[o]
            out_stems: set[str] = set()
            try:
                out_stems = _extract_stems(note_path) & set(notes)
            except Exception:
                pass
            out_str = f"  -> {', '.join(sorted(out_stems)[:5])}" if out_stems else "  (no outlinks)"
            if len(out_stems) > 5:
                out_str += f" ... +{len(out_stems) - 5}"
            print(f"  {notes[o]}{out_str}")

    if near:
        print(f"\n### Near-orphans (1 inlink): {len(near)}")
        for n in near:
            print(f"  {notes[n]}")


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sub = sys.argv[1]
    args = sys.argv[2:]

    if sub == "check":
        if not args:
            print("Usage: wikilinks check <vault-path>")
            sys.exit(1)
        cmd_check(Path(args[0]))

    elif sub == "orphans":
        if not args:
            print("Usage: wikilinks orphans <room-path>")
            sys.exit(1)
        cmd_orphans(Path(args[0]))

    else:
        print(f"Unknown subcommand: {sub}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
