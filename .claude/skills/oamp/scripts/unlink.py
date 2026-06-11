"""Batch-delete vault notes and replace [[wikilink]] references with plain text.

Handles aliased links ([[target|display]]) and anchored links ([[target#section]]).

Usage:
  python3 scripts/unlink.py --vault <path> --targets "Note A" "Note B" --dry-run
  python3 scripts/unlink.py --vault <path> --targets "Note A" "Note B"
"""

from __future__ import annotations

import argparse
import os
import re
import sys

# Matches [[target]], [[target|display]], [[target#section]], [[target#section|display]]
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]')


def _replace_wikilink(match: re.Match, target: str) -> str:
    """Replace a wikilink match with plain text. Returns the display text
    if aliased, otherwise the target name."""
    link_target = match.group(1)
    display = match.group(2)
    if link_target != target:
        return match.group(0)  # not our target, leave unchanged
    return display if display else target


def _find_target_paths(vault: str, targets: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    remaining = set(targets)
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for t in list(remaining):
            if f"{t}.md" in files:
                result[t] = os.path.join(root, f"{t}.md")
                remaining.remove(t)
        if not remaining:
            break
    return result


def main():
    parser = argparse.ArgumentParser(description="Delete notes and replace wikilinks")
    parser.add_argument("--vault", required=True, help="Vault root path")
    parser.add_argument("--targets", nargs="+", required=True,
                        help="Note names to delete (without .md extension)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without modifying files")
    args = parser.parse_args()

    targets = args.targets
    target_paths = _find_target_paths(args.vault, targets)

    not_found = [t for t in targets if t not in target_paths]
    if not_found:
        print(f"WARNING: {len(not_found)} target(s) not found: {not_found}")

    deleted: list[str] = []
    modified: list[str] = []

    # Delete target .md files
    for t, full_path in target_paths.items():
        if not args.dry_run:
            os.remove(full_path)
        deleted.append(full_path)

    # Replace [[wikilinks]] with plain text in all vault .md files
    for root, dirs, files in os.walk(args.vault):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, encoding="utf-8") as fh:
                content = fh.read()

            new_content = content
            changed = False
            for t in targets:
                pattern = re.compile(
                    rf'\[\[{re.escape(t)}(?:\#[^\]|]*)?(?:\|[^\]]*)?\]\]')
                new_content, n = pattern.subn(t, new_content)
                if n > 0:
                    changed = True

            if changed:
                if not args.dry_run:
                    with open(fpath, "w", encoding="utf-8") as fh:
                        fh.write(new_content)
                modified.append(os.path.relpath(fpath, args.vault))

    # Report
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}Deleted: {len(deleted)} file(s)")
    for d in deleted:
        print(f"  {os.path.relpath(d, args.vault)}")
    print(f"{prefix}Modified: {len(modified)} file(s)")
    for m in modified:
        print(f"  {m}")


if __name__ == "__main__":
    main()
