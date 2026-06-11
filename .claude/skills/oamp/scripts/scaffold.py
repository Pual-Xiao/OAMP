"""Scaffold a new memory palace room — folders, entry MOC, optional registration.

Usage:
  python3 scripts/scaffold.py --name "industrial-design" --vault ~/vault \\
      --dimensions designer style material --instance product

  python3 scripts/scaffold.py --name "industrial-design" --vault ~/vault \\
      --from-room ~/vault/architecture

  python3 scripts/scaffold.py --name "industrial-design" --vault ~/vault \\
      --dimensions designer style material --register
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Folder names follow M5 numbering template language (Chinese).
# LLM overrides these via CLI args when vault language differs.
SUFFIX_FOLDERS = ["交叉专题", "跨界连接", "产出+资料"]
DEFAULT_INSTANCE = "实例"
DEFAULT_ENTRY = "入口"

MOC_TEMPLATE = """\
---
type: index
room: {room_name}
---

# {room_name}

## Dimensions

{dim_links}

## Quick access

- Timeline
"""


def scaffold(vault: str, name: str, dimensions: list[str], instance: str,
             entry_name: str, suffix_folders: list[str],
             *, dry_run: bool = False):
    """Create folder structure and entry MOC for a new room."""
    room_dir = Path(vault).expanduser().resolve() / name

    folders: list[str] = [f"00-{entry_name}"]
    for i, dim in enumerate(dimensions, 1):
        folders.append(f"{i:02d}-{dim}")
    inst_num = len(dimensions) + 1
    folders.append(f"{inst_num:02d}-{instance}")
    for i, suffix in enumerate(suffix_folders, inst_num + 1):
        folders.append(f"{i:02d}-{suffix}")

    if dry_run:
        print(f"[DRY RUN] {room_dir}")
        for f in folders:
            print(f"  mkdir {room_dir / f}/")
        return

    room_dir.mkdir(parents=True, exist_ok=True)
    for f in folders:
        (room_dir / f).mkdir(exist_ok=True)

    dim_links = "\n".join(
        f"- [[{i:02d}-{dim}/|{dim}]]" for i, dim in enumerate(dimensions, 1)
    )
    moc = room_dir / f"00-{entry_name}" / "index.md"
    moc.write_text(MOC_TEMPLATE.format(room_name=name, dim_links=dim_links))

    print(f"Room '{name}' scaffolded at {room_dir}")


def list_reference_templates(source_room: Path):
    """Print template paths for LLM to read and adapt.

    Does NOT copy files. The LLM reads these, adapts field names and
    structure to the new room's dimensions, then writes new templates.
    """
    src = source_room / "templates"
    if not src.is_dir():
        return
    templates = sorted(f for f in src.iterdir() if f.is_file())
    if not templates:
        return
    print(f"\nReference templates ({len(templates)}):")
    for t in templates:
        print(f"  {t}")
    print("Adapt these for the new room's dimensions — do not copy verbatim.\n")


def infer_dimensions(source_room: Path, suffix_folders: list[str], entry_name: str
                     ) -> tuple[list[str], str]:
    """Read numbered folders from source room, return (dimensions, instance)."""
    skip = set(suffix_folders) | {entry_name, "templates"}
    entries: list[tuple[int, str]] = []
    for entry in sorted(source_room.iterdir()):
        if not entry.is_dir():
            continue
        name = entry.name
        if len(name) >= 3 and name[:2].isdigit() and name[2] == '-':
            label = name[3:]
            if label in skip:
                continue
            entries.append((int(name[:2]), label))

    if len(entries) >= 2:
        entries.sort(key=lambda x: x[0])
        return [name for _, name in entries[:-1]], entries[-1][1]
    if entries:
        return [entries[0][1]], DEFAULT_INSTANCE
    return [], DEFAULT_INSTANCE


def register(name: str, vault: str, room_type: str = "foundation", role: str = ""):
    """Append room entry to rooms.yml."""
    import yaml

    from room_registry import resolve_rooms_yml

    config_path = resolve_rooms_yml()
    if config_path.exists():
        data = yaml.safe_load(open(config_path)) or {}
    else:
        data = {}

    rooms = data.get("rooms") or {}
    if name in rooms:
        print(f"Room '{name}' already registered — skipping")
        return

    rooms[name] = {
        "path": str(Path(vault).expanduser().resolve() / name),
        "type": room_type,
        "role": role or f"Core interest room for '{name}'",
    }
    data["rooms"] = rooms

    config_path.parent.mkdir(parents=True, exist_ok=True)
    yaml.dump(data, open(config_path, "w"), allow_unicode=True,
              default_flow_style=False, sort_keys=False)
    print(f"Registered '{name}' in {config_path}")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a memory palace room")
    parser.add_argument("--name", required=True, help="Room name")
    parser.add_argument("--vault", required=True, help="Vault root path")
    parser.add_argument("--dimensions", nargs="+",
                        help="Dimension names in causal order")
    parser.add_argument("--instance", default=DEFAULT_INSTANCE,
                        help=f"Instance folder name (default: {DEFAULT_INSTANCE})")
    parser.add_argument("--entry-name", default=DEFAULT_ENTRY,
                        help=f"Entry folder name (default: {DEFAULT_ENTRY})")
    parser.add_argument("--suffix-folders", nargs="+", default=SUFFIX_FOLDERS,
                        help="Suffix folder names after instance")
    parser.add_argument("--from-room",
                        help="Read dimensions and list templates from existing room")
    parser.add_argument("--register", action="store_true",
                        help="Register the room in rooms.yml")
    parser.add_argument("--type", default="foundation",
                        help="Room type for registration")
    parser.add_argument("--role", default="",
                        help="Room description for registration")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without creating files")
    args = parser.parse_args()

    dimensions: list[str] = args.dimensions or []
    instance: str = args.instance
    source_room: Path | None = None

    if args.from_room:
        source_room = Path(args.from_room).expanduser().resolve()
        if not source_room.is_dir():
            print(f"ERROR: source room not found: {source_room}")
            sys.exit(1)
        if not dimensions:
            dimensions, instance = infer_dimensions(
                source_room, args.suffix_folders, args.entry_name)

    if not dimensions:
        print("ERROR: --dimensions required (or use --from-room to infer)")
        sys.exit(1)

    scaffold(args.vault, args.name, dimensions, instance,
             args.entry_name, args.suffix_folders, dry_run=args.dry_run)

    if source_room and not args.dry_run:
        list_reference_templates(source_room)

    if args.register and not args.dry_run:
        register(args.name, args.vault, args.type, args.role)


if __name__ == "__main__":
    main()
