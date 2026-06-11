# Technical Rules & Reference

Code generation, file operations, command parameters. Complete technical specification.

---

## YAML Frontmatter

### Three quoting modes — failure boundaries

| Mode | Syntax | Fails when | Use for |
|------|--------|-----------|---------|
| Double-quoted `"value"` | `field: "text"` | Value contains ASCII `"` (U+0022) | Never use for content with punctuation |
| Single-quoted `'value'` | `field: 'text'` | Never fails (all chars literal) | Values with `[[]]`, `:`, `#` — YAML special chars |
| Plain scalar | `field: text` | Value contains `[[wikilink]]` → YAML parses as flow sequence | Plain text, no YAML special sequences |

### Rules

1. Value contains `[[wikilink]]` → MUST single-quote: `field: '[[link]], other text'`
2. Value contains ASCII `"` → prefer plain scalar (remove outer quotes), fallback: single-quote
3. Never use double-quotes for content with punctuation
4. Validate after write. Never assume "should be fine."

### Diagnostic commands

```bash
# Check all double-quote Unicode codepoints in file
python3 -c "
with open('file.md') as f:
    for i, line in enumerate(f, 1):
        for j, ch in enumerate(line):
            if ord(ch) in [0x22, 0x201c, 0x201d, 0xff02]:
                print(f'L{i}:{j} U+{ord(ch):04X} {repr(ch)}')
"

# Validate single file YAML frontmatter
python3 -c "
import yaml
with open('file.md') as f:
    content = f.read()
end = content.find('---\n', 4)
yaml.safe_load(content[4:end])
print('OK')
"

# Batch scan all .md in vault (replace <vault> with actual path)
find <vault> -name '*.md' | while read f; do
  python3 -c "
import yaml
with open('$f') as fh:
    c = fh.read()
    if not c.startswith('---'): 
        exit()
    end = c.find('---\n', 4)
    if end == -1: 
        exit()
    yaml.safe_load(c[4:end])
" 2>&1 || echo "FAIL: $f"
done
```

---

## Base (.base)

### Three common failure modes

1. **Formula quoting**: formula contains double-quotes → use single-quote wrapper. `'if(done, "Yes", "No")'` correct. `"if(done, \"Yes\", \"No\")"` wrong.
2. **Duration is not a number**: date subtraction returns Duration type. `.days.round(0)` correct. `.round(0)` wrong.
3. **Null guard**: wrap nullable properties in `if()`. `if(due_date, (date(due_date) - today()).days, "")`

### Validation command

```bash
python3 -c "
import yaml
with open('file.base') as f:
    yaml.safe_load(f)
print('OK')
"
```

---

## Mermaid Syntax

### Failure modes

1. Node text contains `[`, `]`, `|`, `"`, `(`, `)` without double-quote wrapping → parse failure, blank diagram
2. `A["text"]` with `\n` → no line break. `\n` only works in `A[text]`. Inside `["text"]` must use `<br/>`
3. Node contains `[[wikilink]]` → Mermaid does not render, shows raw text
4. `graph` has fewer features than `flowchart`. Always prefer `flowchart`.

### Rules

1. Wrap all node text in double-quotes: `A["text"]` not `A[text]`
2. Line breaks use `<br/>`: `A["line1<br/>line2"]`
3. No `[[wikilink]]` inside Mermaid nodes. Use plain text. Link with `[[]]` outside the Mermaid block.
4. Use `flowchart` not `graph`: `flowchart TD` / `flowchart LR`
5. Direction: hierarchy = `TD`, sequence = `LR`

### Validation

```bash
grep -rl '```mermaid' <vault>
# Manually inspect each file found.
```

---

## Canvas (.canvas)

Generate with `json.dump`. Never hand-write.

Node layout encodes causality/sequence:
- Causal chain → left to right
- Hierarchy → top to bottom
- Same-dimension nodes → same column or row

---

## Folder Naming Convention

```
00-入口/              ← index, seen first
01-{dim-1}/           ← causal origin
...
0N-{dim-N}/           ← causal terminus
0N+1-实例/            ← intersection product: dimensions interweave to form this
0N+2-交叉专题/        ← cross-dimensional themes
0N+3-跨界连接/        ← beyond domain boundary
0N+4-产出+资料/       ← output + source materials
```

Causal narrative: dimensions (01-0N) interweave → instance (0N+1) is their product → instance radiates influence outward (0N+2+). The numbering IS the narrative. Changing the order breaks the narrative.

### Rules

- Two-digit IDs: `00`, `01`...`0N`. Zero-pad single digits.
- Causal order must be explicit before creation. Uncertain → return to core interest.

### Forbidden

Alphabetical order, popularity order, entry-count order. These have zero navigation semantics.

---

## Non-Text File Processing

Applies to: `.pages`, `.docx`, `.pdf`, `.html`, etc.

1. Use simplest extraction method: `strings` or `textutil`. Stop when text is readable. Do not preserve formatting.
2. Never reverse-engineer file formats. No unzipping, no protobuf/snappy parsing, no manual hex reading.
3. Never install new packages for format parsing. Try existing tools first.
4. Stop rule: extracted text sufficient to understand document structure and key concepts → stop extracting. Start writing `.md`.

---

## Obsidian Runtime Conventions

- **Obsidian running**: modify vault `.md` files via `obsidian` CLI (`obsidian create`, `obsidian read`, `obsidian property:set`). Keeps Obsidian index in sync.
- **Obsidian not running**: direct filesystem operations (`mkdir`, write files). Obsidian indexes on next launch.
- **`scripts/scaffold.py`**: always uses direct filesystem operations.

---

## CLI Command Reference

All scripts at `<skill-dir>/scripts/`. Invoke: `python3 <skill-dir>/scripts/<name>.py <args>`.

### scaffold.py — Create room skeleton

```bash
python3 scripts/scaffold.py --name "<room>" --vault <path> \
  --dimensions <dim1> <dim2> ... --instance <type> --register
```

| Flag | Effect |
|------|--------|
| `--name` | Room name |
| `--vault` | Obsidian vault path |
| `--dimensions` | Dimension name list |
| `--instance` | Instance folder name |
| `--from-room <path>` | Copy templates from existing room as starting point |
| `--register` | Register room in rooms.yml |

### validate.py — Validation

```bash
python3 scripts/validate.py --all                # Validate all registered rooms
python3 scripts/validate.py --room <path>        # Validate specific room
python3 scripts/validate.py --empty              # Detect blank notes
python3 scripts/validate.py --list-fields        # List all frontmatter fields
```

### wikilinks.py — Link checks

```bash
python3 scripts/wikilinks.py check <room>        # Reachability check
python3 scripts/wikilinks.py redlinks <room>     # Redlink scan
python3 scripts/wikilinks.py orphans <room>      # Orphan note detection
```

### redlinks.py — Expansion engine

```bash
python3 scripts/redlinks.py --vault <vault> --room <room>
```

Groups redlink candidates by dimension, sorts by reference count.

### unlink.py — Batch delete

```bash
python3 scripts/unlink.py --vault <vault> --targets "<note-name>"
```

Deletes `.md` and replaces all `[[references]]` with plain text.

### freshness.py — Perception layer

```bash
python3 scripts/freshness.py --room "<name>"
```

Run before every room operation. Writes `<cwd>/.oamp/freshness/<room>.json`. Compares SHA-256 file hashes against previous snapshot — no git dependency.

---

## Example Export

### Directory structure

```
examples/<room>/
├── raw/              ← original input (empty dir, content not committed)
├── wiki/             ← structured knowledge entries
├── README.md         ← room definition (core interest, dimensions, entity types, structure)
├── SCHEMA.md         ← entry format specification
└── templates/        ← template files (one per entity type; project-side, not in vault)
```

### Export command

```bash
python3 scripts/example_builder.py \
  --name "<room>" \
  --description "<one-line>" \
  --core-interest "<definition>" \
  --dimensions "<dim1>;;<desc>" "<dim2>;;<desc>" \
  --entity-types "<type>;;tpl-<type>.md;;<desc>" \
  --folder-structure "00-入口/" "01-<dim1>/" ...
```

### Rules

1. Create both `raw/` and `wiki/` empty directories
2. `raw/` content not committed (user original input stays out of repo)
3. `wiki/` entry notes referenced from README.md via `[[]]`
4. Template frontmatter fields must trace to core interest definition
5. When updating existing room example: preserve `raw/` and `wiki/` contents

---

## SCHEMA.md Generation Protocol

SCHEMA.md = room data contract. Generate after wiki entries drafted. Path: `<vault>/<room>/00-入口/SCHEMA.md`.

### Step 1: Collect — Extract actual usage

| Diagnostic | Method | Output |
|-----------|--------|--------|
| File naming | `find <room> -name "*.md" \| sort` | Actual naming convention |
| Frontmatter fields | Sample 5-10 files | Field existence, name consistency |
| Tag inventory | Scan all `tags:` | High-frequency tags + one-off tags |
| Wikilink patterns | `wikilinks.py redlinks <room>` | Target naming convention |
| Body structure | Sample 2-3 per type | Section heading patterns |
| Templates | Check `templates/` | Template vs. usage consistency |

### Step 2: Compare — Find inconsistencies

| Category | Check |
|----------|-------|
| Naming | Same concept, different spellings? |
| Fields | Required fields missing? Order inconsistent? |
| Format | Date format uniform? (`YYYY-MM-DD` vs `YYYY-MM`) |
| Case | camelCase vs kebab-case mixed? |
| Redundancy | Tags duplicating existing fields? |

### Step 3: Decide — Resolve conflicts

| Conflict | Default resolution |
|----------|-------------------|
| File names | English kebab-case. No number/date prefix (put in frontmatter). |
| Field order | Identity → Title → Time → Attribution → Description → Classification |
| Tag language | Match file name language |
| Date format | Always `YYYY-MM-DD` |
| Controlled vocabulary | Merge synonyms, keep more general term. Delete tags duplicating fields. |
| Body skeleton | Extract from actual high-frequency patterns. Do not design from scratch. |

### Step 4: Write — Five required sections

1. **Naming conventions** — file names, field order, date format
2. **Tag system** — controlled vocabulary, hierarchy rules
3. **Wikilink rules** — how redlinks are used in this room
4. **Frontmatter templates** — per-entity-type field order + body skeleton
5. **Validation** — commands to check compliance

After writing: correct existing inconsistencies against new schema. Update `templates/` files.

---

## File Operation Rules

- JSON/Canvas: MUST use `json.dump`. Never hand-write.
- After creating/modifying vault files: run corresponding validation command (see CLI reference above)
- Before room operations: run `freshness.py` — perceive before act
