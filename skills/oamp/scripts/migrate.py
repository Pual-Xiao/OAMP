"""Phase 5X: migrate discovery notes to dimension folders.

After LLM determines which dimension each discovery note belongs to,
this script executes the file moves and cleans up empty discovery/.

Usage:
  python3 migrate.py --room <path> --mapping '<json>' [--dry-run]

Mapping format (JSON):
  {"note_basename": "target_folder", ...}

  - note_basename: .md filename without extension
  - target_folder: dimension folder name (e.g., "01-设计师")

Example:
  python3 migrate.py --room ~/vault/my-room \
      --mapping '{"note-a": "01-设计师", "note-b": "02-方法"}'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def migrate(room: Path, mapping: dict[str, str], *, dry_run: bool = False):
    """Move discovery notes to dimension folders. Delete empty discovery/."""

    discovery = room / "discovery"
    if not discovery.is_dir():
        print(f"No discovery/ folder in {room}")
        return 0

    moved = 0
    not_found: list[str] = []
    errors: list[str] = []

    for basename, target_folder in mapping.items():
        src = discovery / f"{basename}.md"
        target_dir = room / target_folder

        if not src.exists():
            not_found.append(basename)
            continue

        if not target_dir.is_dir():
            errors.append(f"target folder not found: {target_folder}")
            continue

        dst = target_dir / f"{basename}.md"
        if dst.exists():
            errors.append(f"destination already exists: {dst.relative_to(room)}")
            continue

        if dry_run:
            print(f"[DRY RUN] {src.relative_to(room)} → {dst.relative_to(room)}")
        else:
            src.rename(dst)
            print(f"  {basename}.md → {target_folder}/")

        moved += 1

    # Clean up empty discovery/
    if not dry_run:
        remaining = list(discovery.iterdir()) if discovery.is_dir() else []
        if not remaining:
            discovery.rmdir()
            print(f"  Removed empty discovery/")
        else:
            print(f"  discovery/ not empty — {len(remaining)} file(s) remain, skipping removal")

    if not_found:
        print(f"\nWARNING: {len(not_found)} note(s) not found in discovery/:")
        for n in not_found:
            print(f"  - {n}.md")

    if errors:
        print(f"\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return moved

    return moved


def main():
    parser = argparse.ArgumentParser(
        description="Phase 5X — migrate discovery notes to dimension folders")
    parser.add_argument("--room", required=True, help="Room path")
    parser.add_argument("--mapping", help="JSON mapping: {basename: target_folder}")
    parser.add_argument("--mapping-file", help="Path to JSON mapping file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without moving files")
    args = parser.parse_args()

    room = Path(args.room).expanduser().resolve()
    if not room.is_dir():
        print(f"ERROR: room not found: {room}")
        sys.exit(1)

    if args.mapping_file:
        mapping = json.loads(Path(args.mapping_file).read_text())
    elif args.mapping:
        mapping = json.loads(args.mapping)
    else:
        print("ERROR: --mapping or --mapping-file required")
        sys.exit(1)

    if not isinstance(mapping, dict):
        print("ERROR: mapping must be a JSON object")
        sys.exit(1)

    moved = migrate(room, mapping, dry_run=args.dry_run)
    print(f"\nMigrated {moved}/{len(mapping)} note(s).")


if __name__ == "__main__":
    main()
