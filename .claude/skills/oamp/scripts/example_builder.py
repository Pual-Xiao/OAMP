"""Export a room as an example — copies templates and generates README.

Usage:
  python3 scripts/example_builder.py --name "industrial-design" \\
      --room-dir ~/vault/industrial-design --output-dir ./examples \\
      --core-interest "Preference for form-follows-function"

The script discovers folder structure and templates from the room directory.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

EXCLUDE_TEMPLATES = {".obsidian", ".trash", ".git"}


def main():
    parser = argparse.ArgumentParser(description="Export a room as an example")
    parser.add_argument("--name", required=True, help="Room name")
    parser.add_argument("--room-dir", required=True, help="Path to the room in the vault")
    skill_dir = Path(__file__).resolve().parent.parent
    parser.add_argument("--output-dir", default=str(skill_dir / "examples"), help="Output directory")
    parser.add_argument("--core-interest", default="", help="One-sentence core interest")
    parser.add_argument("--description", default="", help="One-line room description")
    args = parser.parse_args()

    room = Path(args.room_dir).expanduser().resolve()
    if not room.is_dir():
        print(f"ERROR: room not found: {room}")
        sys.exit(1)

    out = Path(args.output_dir).resolve() / args.name
    out.mkdir(parents=True, exist_ok=True)

    # Discover folder structure
    folders: list[str] = []
    for entry in sorted(room.iterdir()):
        if entry.is_dir() and entry.name != "templates":
            folders.append(f"{entry.name}/")

    # Copy templates
    src_tpl = room / "templates"
    dst_tpl = out / "templates"
    template_files: list[str] = []
    if src_tpl.is_dir():
        dst_tpl.mkdir(exist_ok=True)
        for f in src_tpl.iterdir():
            if f.is_file() and f.name not in EXCLUDE_TEMPLATES:
                shutil.copy2(f, dst_tpl / f.name)
                template_files.append(f.name)

    # Generate README
    lines = [f"# {args.name}", ""]
    if args.description:
        lines.extend([f"> {args.description}", ""])
    if args.core_interest:
        lines.extend(["## Core Interest", "", args.core_interest, ""])
    if folders:
        lines.extend(["## Folder Structure", "", "```"])
        lines.extend(folders)
        lines.extend(["```", ""])
    if template_files:
        lines.extend(["## Templates", ""])
        for t in sorted(template_files):
            lines.append(f"- `{t}`")
        lines.append("")

    (out / "README.md").write_text("\n".join(lines))

    print(f"Example exported: {out}")
    print(f"  {out / 'README.md'}")
    if template_files:
        print(f"  templates/ ({len(template_files)} files)")


if __name__ == "__main__":
    main()
