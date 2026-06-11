"""oamp perception layer — check room freshness via file hashing.

Detects changes by comparing SHA-256 hashes of all room files against
a stored snapshot. No git dependency, no Obsidian plugin required.

Usage:
  python3 freshness.py                    # all registered rooms
  python3 freshness.py --room <name>      # single room
  python3 freshness.py --json             # stdout instead of files
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FRESHNESS_DIR = Path.cwd() / ".oamp" / "freshness"

EXCLUDE_DIRS = {".obsidian", ".git", ".trash", ".oamp", "__pycache__", "node_modules"}
EXCLUDE_FILES = {".DS_Store"}


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _scan_room(room_path: Path) -> dict[str, str]:
    """Return {relative_path: sha256} for all files in room."""
    room = room_path.resolve()
    if not room.is_dir():
        return {}
    hashes: dict[str, str] = {}
    for f in room.rglob("*"):
        if not f.is_file():
            continue
        if f.name in EXCLUDE_FILES:
            continue
        parts = set(f.relative_to(room).parts)
        if parts & EXCLUDE_DIRS:
            continue
        hashes[str(f.relative_to(room))] = _hash_file(f)
    return hashes


def check_room(name: str, room_path: Path) -> dict:
    current = _scan_room(room_path)
    hash_file = FRESHNESS_DIR / f"{name}_hashes.json"

    previous: dict[str, str] = {}
    if hash_file.exists():
        try:
            previous = json.loads(hash_file.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    current_set = set(current.keys())
    previous_set = set(previous.keys())

    changes: list[dict] = []
    for f in sorted(current_set - previous_set):
        changes.append({"file": f, "status": "??", "status_label": "new"})
    for f in sorted(previous_set - current_set):
        changes.append({"file": f, "status": " D", "status_label": "deleted"})
    for f in sorted(current_set & previous_set):
        if current[f] != previous[f]:
            changes.append({"file": f, "status": " M", "status_label": "modified"})

    hash_file.parent.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n")

    return {
        "room": name,
        "room_path": str(room_path),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total_changes": len(changes),
        "changes": changes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="oamp freshness — perception layer")
    parser.add_argument("--room", help="Check a single room by name")
    parser.add_argument("--json", action="store_true",
                        help="Print JSON to stdout instead of writing files")
    parser.add_argument("--output-dir",
                        help=f"Override output directory (default: {FRESHNESS_DIR})")
    args = parser.parse_args()

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from room_registry import load_rooms  # noqa: E402

    rooms = load_rooms()
    if not rooms:
        print("No rooms registered. Use scaffold.py --register to add rooms.",
              file=sys.stderr)
        sys.exit(1)

    if args.room:
        if args.room not in rooms:
            print(f"Room '{args.room}' not registered.", file=sys.stderr)
            sys.exit(1)
        to_check = {args.room: rooms[args.room]["path"]}
    else:
        to_check = {n: r["path"] for n, r in rooms.items()}

    results = {}
    for name, rpath in to_check.items():
        results[name] = check_room(name, rpath)

    if args.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    out_dir = Path(args.output_dir) if args.output_dir else FRESHNESS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    cwd = Path.cwd()
    written: list[str] = []
    for name, data in results.items():
        fpath = out_dir / f"{name}.json"
        fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        try:
            written.append(str(fpath.relative_to(cwd)))
        except ValueError:
            written.append(str(fpath))

    total = sum(r["total_changes"] for r in results.values())
    print(f"freshness: {total} change(s) over {len(written)} room(s)")
    for p in written:
        print(f"  {p}")


if __name__ == "__main__":
    main()
