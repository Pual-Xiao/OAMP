"""Validate vault .md files — YAML frontmatter and empty/stub notes.

Usage:
  python3 scripts/validate.py <path>       # validate a directory or file
  python3 scripts/validate.py --all        # validate all registered rooms
  python3 scripts/validate.py --all --empty  # also detect empty/stub notes

Exit 0 if all checks pass, 1 if any file fails.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from room_registry import load_rooms

EXCLUDE_DIRS = {".obsidian", ".trash", ".git", "__pycache__", "templates"}
WIKILINK_RE = re.compile(r'\[\[([^]#|]+)(?:[#|][^]]*)?\]\]')


# ── YAML frontmatter ──────────────────────────────────────────────────

def parse_frontmatter(path: Path) -> tuple[dict | None, str | None]:
    try:
        raw = path.read_text()
    except Exception as e:
        return None, f"cannot read file: {e}"
    if not raw.startswith("---"):
        return None, "missing frontmatter"
    end = raw.find("---", 3)
    if end == -1:
        return None, "unclosed frontmatter"
    try:
        import yaml
        fm = yaml.safe_load(raw[3:end])
    except Exception as e:
        return None, f"YAML parse error: {e}"
    if not isinstance(fm, dict):
        return None, f"frontmatter is not a dict (got {type(fm).__name__})"
    return fm, None


def validate_frontmatter(path: Path) -> list[str]:
    errors: list[str] = []
    if path.is_file():
        _, err = parse_frontmatter(path)
        if err:
            errors.append(f"{path}: {err}")
        return errors
    if not path.is_dir():
        return [f"{path}: directory not found"]
    for f in sorted(path.rglob("*.md")):
        parts = set(f.relative_to(path).parts)
        if parts & EXCLUDE_DIRS:
            continue
        _, err = parse_frontmatter(f)
        if err:
            errors.append(f"{f}: {err}")
    return errors


# ── Empty/stub notes ──────────────────────────────────────────────────

def body_after_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text.strip()
    end = text.find("---", 3)
    return "" if end == -1 else text[end + 3:].strip()


def extract_targets(text: str) -> set[str]:
    targets: set[str] = set()
    for m in WIKILINK_RE.finditer(text):
        t = m.group(1).strip().rstrip("\\/")
        if t and not t.endswith("/"):
            if "/" in t:
                t = t.rsplit("/", 1)[-1]
            targets.add(t)
    return targets


def build_inlinks(room: Path) -> dict[str, set[str]]:
    links: dict[str, set[str]] = {}
    for f in room.rglob("*.md"):
        parts = set(f.relative_to(room).parts)
        if parts & EXCLUDE_DIRS:
            continue
        try:
            src = str(f.relative_to(room))
            for target in extract_targets(f.read_text()):
                links.setdefault(target, set()).add(src)
        except Exception:
            pass
    return links


def detect_empty_notes(room_path: Path) -> list[str]:
    if not room_path.is_dir():
        return [f"{room_path}: directory not found"]
    inlinks = build_inlinks(room_path)
    results: list[str] = []
    for f in sorted(room_path.rglob("*.md")):
        parts = set(f.relative_to(room_path).parts)
        if parts & EXCLUDE_DIRS:
            continue
        try:
            raw = f.read_text()
        except Exception:
            continue
        body = body_after_frontmatter(raw)
        rel = str(f.relative_to(room_path))
        if not body:
            il = inlinks.get(f.stem, set())
            il_str = f", {len(il)} inlinks" if il else "zero inlinks"
            results.append(f"{rel}: completely empty ({il_str})")
        elif len(body) < 20:
            il = inlinks.get(f.stem, set())
            il_str = f", {len(il)} inlinks" if il else "zero inlinks"
            results.append(f"{rel}: stub ({len(body)} chars body{il_str})")
    return results


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Validate vault .md files")
    p.add_argument("path", nargs="?", help="Directory or file to validate")
    p.add_argument("--all", action="store_true",
                   help="Validate all rooms in rooms.yml")
    p.add_argument("--empty", action="store_true",
                   help="Also detect empty/stub notes")
    args = p.parse_args()

    rooms: dict[str, Path] = {}

    if args.all:
        try:
            loaded = load_rooms()
        except Exception as e:
            print(f"ERROR: cannot load room registry: {e}")
            sys.exit(1)
        if not loaded:
            print("No rooms registered in rooms.yml.")
            sys.exit(0)
        for name, info in loaded.items():
            if isinstance(info, dict):
                room_path = info.get("path")
                if room_path:
                    rooms[name] = Path(room_path)
            else:
                rooms[name] = Path(str(info))
    elif args.path:
        p = Path(args.path).resolve()
        rooms = {p.name: p}
    else:
        p.print_usage()
        sys.exit(1)

    total_fm = 0
    total_empty = 0

    for name, room_path in sorted(rooms.items()):
        if not room_path.is_dir():
            print(f"  {name}: SKIP (directory not found: {room_path})")
            continue

        fm_errors = validate_frontmatter(room_path)
        if fm_errors:
            print(f"\n## {name} — frontmatter errors ({len(fm_errors)})")
            for e in fm_errors:
                print(f"  {e}")
            total_fm += len(fm_errors)
        else:
            print(f"  {name}: frontmatter OK")

        if args.empty:
            empty_results = detect_empty_notes(room_path)
            if empty_results:
                print(f"\n## {name} — empty/stub notes ({len(empty_results)})")
                for e in empty_results:
                    print(f"  {e}")
                total_empty += len(empty_results)
            else:
                print(f"  {name}: empty notes OK")

    total_issues = total_fm + total_empty
    if total_issues:
        parts = []
        if total_fm:
            parts.append(f"{total_fm} frontmatter")
        if total_empty:
            parts.append(f"{total_empty} empty")
        print(f"\n{', '.join(parts)} issue(s) found.")
        sys.exit(1)

    print("\nAll checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
