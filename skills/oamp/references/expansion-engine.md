# Expansion Engine

Mechanism for growing a room from skeleton to dense knowledge network.

## Trigger

Initial notes filled. Base structure navigable.

## Expansion Loop

### 1. Scan redlinks

```bash
python3 <skill-dir>/scripts/redlinks.py --vault <vault> --room <room>
```

Finds all `[[wikilink]]` where target `.md` does not exist. Groups by dimension. Sorts by reference count.

### 2. Decide

Per redlink candidate:

| Decision | Condition | Action |
|----------|-----------|--------|
| **Fill** | Redlink directly serves core interest | Create `.md` with matching template, fill content |
| **Describe** | Concept too common for standalone entry | Remove `[[]]`, keep as plain text |
| **Skip** | Uncertain | Keep redlink, re-evaluate next scan |

### 3. Create notes

For each Fill candidate: select matching template → fill frontmatter → write body (with 2-3 new redlinks) → validate.

### 4. New notes introduce new redlinks

When writing body for new notes: actively insert `[[wikilinks]]` for concepts you know belong in this network but don't have notes yet. Return to step 1.

### 5. Prune

Remove unwanted nodes:

```bash
python3 <skill-dir>/scripts/unlink.py --vault <vault> --targets "<note-name>"
```

Deletes `.md` and replaces all `[[references]]` with plain text.

Orphan detection:

```bash
python3 <skill-dir>/scripts/wikilinks.py orphans <room>
```

## Cross-Dimensional Timing

After ~30+ instances accumulate, cross-dimensional patterns surface naturally. At this point: create cross-cutting notes and cross-boundary notes.

Patterns emerge. Do not design them. Do not force when < 30 instances.

## Stop Condition

Two consecutive scans yield zero new meaningful redlinks → room mature.

Mature ≠ complete. New input → resume from step 1.

## Quick Reference

| Action | Command |
|--------|---------|
| Scan redlinks | `python3 scripts/redlinks.py --vault <v> --room <r>` |
| Delete + clean refs | `python3 scripts/unlink.py --vault <v> --targets "<name>"` |
| Detect orphans | `python3 scripts/wikilinks.py orphans <room>` |
| Validate | `python3 scripts/validate.py --all` |
