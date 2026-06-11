---
name: oamp
description: |
  oamp — Obsidian Automated Memory Palace. Use to build an Obsidian knowledge base, create a memory palace room, scaffold a vault, structure notes, or turn conversations/research into an organized vault.
  Trigger on: 知识库, 记忆宫殿, 房间, 结构化, 搭建, 整理笔记, oamp, organize knowledge in Obsidian.
  Even a 1% chance of relevance means invoke this skill.
  
  Follow below rules, any action follow below principle:
  
  1. Compare fragments by design problem, not surface features. Ask: what constraint was each designed to solve? Ignore era, geography, scale, style.
  2. Distill core interest to one sentence. If longer, not done. Every downstream decision must trace back to this sentence.
  3. Do not use the thing's name as its folder. File it once in its best-fit folder. Reach it from everywhere else via wikilink.
  4. Design 3-5 dimensions. Before finalizing, ask: do two track the same thing? Does each have its own narrative arc? Does removing one kill a query?
  5. Folder numbers tell a causal story. 01-0N = dimensions. 0N+1 = their intersection. 0N+2+ = outward radiation. Wrong order breaks the narrative.
  6. Do not design folder structure after thinking. The folder structure IS the thinking. If reordering doesn't change the thought, it's just filing.
  7. Do not copy template files between rooms. Principles and methodology are the real template. Template files are the output, not the source.
  8. Every template field must trace to a core-interest keyword. No trace = delete the field. Do not inherit fields from other rooms.
  9. Every wiki entry gets 2-3 redlinks. Each redlink must be a question, not a noun. A link to nothing is not a bug — it is a future expansion seed.
  10. Exploratory notes: do not try to be correct. Write to discover what you care about. Re-read all notes after writing — patterns surface from what you actually wrote.
  11. Write notes → leave redlinks → scan unfilled links → fill them → repeat. Stop only when two consecutive scans find zero new meaningful redlinks.
  12. Before any room operation, run freshness.py. Never operate on stale state.
allowed-tools: "Bash(python3 *) Bash(find *) Bash(ls *) Bash(mkdir *) Bash(cp *) Bash(grep *)"
---

# oamp — Main Router

Turn unstructured content into structured Obsidian knowledge base. This file = execution flow. References = knowledge base (read on demand).

Three paths:
- **Structure-First** — structure before content (S1-S5)
- **Exploration-First** — content before structure (E1-E4)
- **User-Material** — external material conversion (U1-U5)

## Step 0: Initialization

Do these in order. Stop on first failure.

1. `python3 --version` — fail → report "Python 3 not found"
2. `ls .oamp/rooms.yml` — missing → create empty file
3. Print: "oamp ready."
4. Go to R1.

---

## R1: Destination Classification

Classify before any content processing. You classify. One sentence unclear → ask user.

| Classification | Condition | Next step |
|---------------|-----------|-----------|
| **Existing room** | Content fits scope of registered room | Fill content, or fragment first |
| **New room** | Independent domain, no existing room fits | R2 → route |
| **Raw idea** | Unstructured, user cannot define scope | R2 → internal fork at R3 |
| **Source material** | User provides files for conversion | R2 → user-material path |

## R2: Fragment Collection

For each fragment: extract its design question. Design question = what constraint does this fragment answer? Do not categorize.

**Method**: M1. Extract Design Question

1. Ask: "Why is the same person drawn to all these at once?"
2. Ask: "Anything you think you should like but don't?" (counterexample)
3. Uncertain → keep probing. Do not skip.

**Blocking**: see `quality-gates.md` R2.

## R3: Route Determination

| Condition | Route |
|-----------|-------|
| Fragments ≥ 6 AND user can describe relationships | **Structure-First** (S1-S5) |
| Fragments < 6 OR user still exploring | **Exploration-First** (E1-E4) |
| User provides existing material | **User-Material** (U1-U5) |

### Internal Fork: Raw Idea → Input Type

Only when R1 = Raw idea. Judge by input signature:

| Input type | Signature | Route |
|-----------|-----------|-------|
| **Conversation fragments** | Scattered preferences, aversions, questions. No headings, no paragraphs, no logical connectors. | Exploration-First |
| **Existing document** | Has headings, paragraphs, logical connectors. .pages/.docx/.md/text. | User-Material |

LLM judges signature. If document structure present → Existing document.

---

# Structure-First Path

Trigger: fragments ≥ 6, user describes relationships.

## S1: Core Interest Synthesis

**Method**: M2.

1. Compare fragments by design question — not surface features
2. Extract 2-4 shared judgment criteria
3. Compress to one sentence: preference for "[what]", particularly "[which aspect]"
4. Rule: more than one sentence = not done

**Blocking**: see `quality-gates.md` S1.

## S2: Dimension Derivation

**Methods**: M3, M4.

For each keyword in core interest: reverse-derive what dimension tracks it.

Four checks (all must pass):
- Orthogonal — dimensions track different things
- Independently navigable — each dimension alone has a narrative arc
- Complete coverage — every keyword has a dimension
- Irreducible — remove it and a query becomes impossible

Target: 3-5 dimensions.

Rule: instance ≠ dimension. Instance = intersection of dimensions. Store one file, link via `[[]]` from multiple places.

## S3: Folder Structure Design

**Method**: M5.

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

Rules: two-digit IDs (`00`-`0N`), zero-pad single digits. Causal chain explicit before creation.

Forbidden: alphabetical order, popularity order, entry-count order.

Full rules: `tech-rules.md` folder naming + `metrology.md` M5.

## S4: Template Design

**Method**: M6.

One template per entity type. Every field traces to a core-interest keyword. Cannot trace → delete.

Field rules: `template-protocol.md`.

## S5: Room Output Assembly

Output the room design. Must include:
1. Core interest definition (from S1)
2. Dimension list (from S2)
3. Folder structure (from S3)
4. Templates (from S4)
5. Initial wiki entries — 1-3 per entity type, each with 2-3 redlinks
6. SCHEMA.md — room data contract, placed at `<vault>/<room>/00-入口/SCHEMA.md`

→ Then R4: Room Assembly.

---

# Exploration-First Path

Trigger: fragments < 6, or user still exploring.

## E1: Deep Probing

**Method**: M8.

For each R2 fragment, three probes:
1. Design question: "What constraint was X designed to solve?"
2. Opposite: "Is there an anti-X you dislike?"
3. Co-occurrence: "Why is the same person drawn to both?"

3 deep fragments beat 10 shallow ones. Uncertain → keep probing.

**Blocking**: see `quality-gates.md` E1.

## E2: Discovery Notes

Create folder: `<vault>/<room>/discovery/`. Only folder initially.

Write 5-10 notes. One fragment per note. Title = fragment name.

Each note structure (three sections):
- **What it is**
- **Why I care**
- **What it leads to** (1-3 `[[wikilinks]]`)

Rules during E2:
- No classification. No dimensions. No templates.
- No YAML frontmatter.
- Just write.

After last note: re-read all discovery notes.

## E3: Pattern Emergence

**Methods**: M9, M2.

1. Re-read all note bodies. Find recurring words, contrasts, judgment criteria.
2. List patterns.
3. Present: "I notice [A], [B], [C]... what matters to you is [X] — correct?"
4. Confirm → distill core interest (M2b).

Rules:
- < 5 notes → do not force patterns
- User hesitates → not confirmed. "yeah..." ≠ yes.
- Patterns emerge. Do not design them.

## E4: Structure Design

**Methods**: M3, M4, M5.

Same as S2-S5:
1. Derive dimensions from core interest (S2)
2. Design folder structure (S3)
3. Design templates (S4)
4. Output room design (S5)

### Phase 5X: Structural Adjustment

Move discovery notes into dimension folders:

1. Run `scaffold` (generates room skeleton)
2. Move notes from `discovery/` to dimension folders
3. Add YAML frontmatter to each note (match template fields)
4. Update wikilink references
5. Delete empty `discovery/`

→ Then R4: Room Assembly.

---

# User-Material Path

Trigger: user provides existing material.

## U1: Input Classification

| Input type | Signature | Route |
|-----------|-----------|-------|
| **Complete document** | Has narrative structure, headings, conclusions | U2 → U3 |
| **Daily notes** | Scattered .md, journal entries. No structure. | Skip to U4 |

### Non-plaintext files

`.pages`, `.docx`, `.pdf`, `.html` → extract text with `strings` or `textutil`.

Full rules: `tech-rules.md` non-text file processing.

## U2: Document Deconstruction

**Method**: M10.

1. Extract narrative skeleton
2. Separate: judgments (probe-able) vs facts (verifiable)
3. Mark open questions
4. Map logic flow

**Blocking**: see `quality-gates.md` U2.

## U3: Structured Restructuring

**Method**: M10 restructure step.

For each document:
1. Reorder by causality/hierarchy — not original sequence
2. Surface implicit assumptions → `> [!question]`
3. Diagram flow → Mermaid or structured list
4. Insert probing redlinks (each a question, not a noun)
5. Mark replicability bottlenecks → `> [!warning]`
6. Add frontmatter → ≥ 3 domain tags

**Quality gates (4 items)**: see `quality-gates.md` U3. Missing any → U3 not done.

## U4: Pattern Emergence

**Methods**: M9, M2.

Same as E3.

Daily notes special case: process 2-3 as examples first. Observe latent dimensions. Return to U1.

Scalability: one batch may yield 1-3 room candidates. Process each independently.

## U5: Structure Design

**Methods**: M3, M4, M5.

Same as S2-S5. Multiple room candidates → record each independently.

→ Then R4: Room Assembly.

---

## Redlink Rules

Redlink = `[[wikilink]]` where target `.md` does not exist. Not a bug. Expansion seed.

1. Every wiki entry: 2-3 redlinks minimum
2. Redlink = question, not noun. Strip `[[]]` → complete question. `[[why did X decline]]` not `[[X]]`
3. Redlink = intent trace. Marker: "worth investigating here"
4. Create redlinks at any phase

Write/Scan/Decide: `metrology.md` M7.
Expansion: `expansion-engine.md`.

---

## SCHEMA.md

Room data contract. Generate after wiki entries drafted. Path: `<vault>/<room>/00-入口/SCHEMA.md`.

4-step protocol (Collect → Compare → Decide → Write): `tech-rules.md` SCHEMA generation.

---

## File Operation Rules

- JSON/Canvas: MUST `json.dump`. Never hand-write.
- Before room operations: run `freshness.py` — perceive before act
- Template fields: traceable to core interest (`template-protocol.md`)
- Same-name fields: identical across all templates

Full rules + CLI parameters: `tech-rules.md`.

---

## R4: Room Assembly

### Step 1: Ask vault path

Ask every time. Never store default.

### Step 2: Scaffold

```bash
python3 <skill-dir>/scripts/scaffold.py --name "<room>" --vault <path> \
  --dimensions <dim1> <dim2> ... \
  --entry-name 入口 --instance 实例 \
  --suffix-folders 交叉专题 跨界连接 产出+资料 \
  --register
```

Derive dimensions from existing room: `--from-room <source-room-path>`. Only use for structurally similar domains.

### Step 3: Design templates

Default: design templates from this room's own dimensions via M6. Every field traces to a core-interest keyword.

If user explicitly asks to reuse templates from an existing room: ask which room, read its templates, adapt fields to the new room's dimensions. Do not copy verbatim.

Write to `<skill-dir>/examples/<room>/templates/`. Templates are project-side, not in vault.

### Step 4: Write wiki entries

Each `.md` under `<vault>/<room>/` in correct folder. Must have:
- Frontmatter matching its template
- Body with 2-3 redlinks

SCHEMA.md → `<vault>/<room>/00-入口/SCHEMA.md`.
Source materials → `<vault>/<room>/<NN>-产出+资料/`.

### Step 5: Export example (optional)

Ask: "Export this room as an example?"

Structure + command: `tech-rules.md` Example export.

---

## Phase 7: Iterative Expansion

Starts after R4.

Loop:
1. Scan redlinks: `python3 <skill-dir>/scripts/redlinks.py --vault <vault> --room <room>`
2. Decide per redlink: fill / describe / skip
3. Fill → create `.md` with template, body contains new redlinks
4. Return to step 1

Stop: two consecutive scans produce zero new meaningful redlinks → room mature.

Mature ≠ complete. New input → resume from step 1.

Full procedure: `expansion-engine.md`.

---

## References

Read on demand. Not loaded until referenced.

- `references/principles.md` — 13 design principles (full explanations)
- `references/metrology.md` — M0-M11 derivation methods (steps, I/O, blocking conditions)
- `references/tech-rules.md` — YAML/JSON/Canvas/Mermaid syntax, folder naming, non-text files, Obsidian runtime, CLI commands, SCHEMA protocol, Example export
- `references/template-protocol.md` — field traceability, same-name identity, enum values, tag hierarchy, Base sync, wikilink quoting
- `references/quality-gates.md` — blocking conditions per phase + validation checklist
- `references/expansion-engine.md` — Phase 7 loop: scan, decide, create, prune, stop

## Scripts

Location: `<skill-dir>/scripts/`. Invoke: `python3 <skill-dir>/scripts/<name>.py <args>`.

| Script | Function |
|--------|----------|
| `freshness.py` | Perceive before act. Run before room ops. Writes per-room JSON. |
| `scaffold.py` | Create folder skeleton + entry MOC + register room. |
| `migrate.py` | Phase 5X: Move discovery notes to dimension folders, clean up. |
| `validate.py` | YAML validation, blank note detection, field listing. |
| `wikilinks.py` | Link reachability, redlink scan, orphan detection. |
| `redlinks.py` | Redlink scan for expansion engine. |
| `unlink.py` | Batch delete notes, replace `[[]]` with plain text. |
| `example_builder.py` | Export room as example. |
